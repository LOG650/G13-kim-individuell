"""
LOG650 G13 - Kim-Ove Hagerup
Mannsverk Gård - Besøksprognoser med maskinlæring

Komplett pipeline:
  1. Simulering av ukentlige besøkstall 2022-2025
  2. EDA og figurer
  3. Sesongnaiv referansemodell
  4. Random Forest (ML-modell)
  5. Evaluering: MAE, RMSE, residualer, variabelviktighet

Krav:
  pip install pandas numpy scikit-learn matplotlib

Kjøring:
  python simulate_and_model.py

Output:
  data/mannsverk_weekly.csv        - simulert datasett
  figures/01_dataset_overview.png  - hele tidsserien med strukturelle skift
  figures/02_seasonal_profile.png  - gjennomsnittlig årssyklus
  figures/03_predictions.png       - prediksjon vs faktisk for begge modeller
  figures/04_residuals.png         - residualer og fordeling
  figures/05_feature_importance.png - permutasjonsbasert variabelviktighet
  results/metrics.csv              - MAE og RMSE for begge modeller
"""

from __future__ import annotations
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import YearLocator, DateFormatter
from sklearn.ensemble import RandomForestRegressor
from sklearn.inspection import permutation_importance
from sklearn.metrics import mean_absolute_error, mean_squared_error

# =============================================================================
# Konfigurasjon - alle parametere samlet her for transparens og reproduserbarhet
# =============================================================================
SEED = 42
START_DATE = "2022-01-03"   # mandag i ISO-uke 1, 2022
END_DATE   = "2025-12-29"   # mandag i ISO-uke 1, 2026 (eksklusiv)

# Baseline besøkstall (gjennomsnitt per uke i 2022, før gårdsbutikk og café åpnet)
BASELINE = 25.0

# Strukturelle skift (åpning av nye tilbud)
SHOP_OPEN_DATE  = "2024-11-01"   # gårdsbutikk åpnet november 2024
CAFE_OPEN_DATE  = "2025-06-01"   # gårdscafé åpnet sommeren 2025
SHOP_EFFECT     = 35.0           # gjennomsnittlig økning per uke etter butikk-åpning
CAFE_EFFECT     = 60.0           # ytterligere økning per uke etter café-åpning

# Trendvekst (lineær drift i baseline gjennom hele perioden)
TREND_PER_WEEK  = 0.15           # mild oppdrift i besøk

# Sesongmønster - amplitudene gir Nord-Norge-typisk profil
ANNUAL_AMPLITUDE = 28.0          # hovedsesong: sommer (jordbær, café)
SEMI_ANNUAL_AMP  = 6.0           # mindre sekundærtopp om vinteren (jul, gårdsbutikk)
SEASONAL_PEAK_WEEK = 28          # uke 28 = midten av juli

# Helligdager / spesielle uker (uke nr → multiplikator/additiv)
HOLIDAY_WEEKS = {
    15: 1.25,  # påskeuken (typisk uke 14-15)
    51: 1.30,  # jul/førjul
    52: 1.30,  # romjul
    27: 1.20,  # midtsommer / jordbærhøsting
    28: 1.25,
    29: 1.20,
}

# Event-uker (planlagte arrangementer fra og med 2024) → additivt antall besøkende
EVENT_BOOST = {
    "2024-08-12": 40,  # arrangement
    "2024-10-14": 25,
    "2025-05-19": 30,
    "2025-08-11": 55,
    "2025-09-22": 30,
}

# Støy (normalfordelt, gaussisk)
NOISE_SD = 7.0

# Modellparametere
TEST_FRACTION = 0.20             # kronologisk siste 20% til test
RF_N_ESTIMATORS = 500
RF_MAX_DEPTH = None
RF_MIN_SAMPLES_LEAF = 2
RF_RANDOM_STATE = SEED


# =============================================================================
# Steg 1: Simulering av datasettet
# =============================================================================
def simulate_weekly_data() -> pd.DataFrame:
    """
    Genererer en ukentlig tidsserie med strukturerte komponenter:
        y_t = baseline + trend_t + season_t + holiday_t + event_t + shift_t + noise_t

    Returnerer DataFrame med kolonner: date, week, year, visitors, og indikatorer.
    """
    rng = np.random.default_rng(SEED)

    # Ukentlig indeks (mandager)
    dates = pd.date_range(start=START_DATE, end=END_DATE, freq="W-MON")
    n = len(dates)
    df = pd.DataFrame({"date": dates})
    df["week"] = df["date"].dt.isocalendar().week.astype(int)
    df["year"] = df["date"].dt.isocalendar().year.astype(int)
    df["t"]    = np.arange(n)

    # Baseline + trend
    baseline = BASELINE + TREND_PER_WEEK * df["t"]

    # Sesong (årlig + semi-årlig harmoniske)
    phase = 2 * np.pi * (df["week"] - SEASONAL_PEAK_WEEK) / 52.0
    season = ANNUAL_AMPLITUDE * np.cos(phase) + SEMI_ANNUAL_AMP * np.cos(2 * phase)

    # Helligdager (multiplikative justeringer på (baseline + season) – fanges som økning)
    holiday_mult = df["week"].map(HOLIDAY_WEEKS).fillna(1.0).astype(float)
    df["is_holiday"] = (holiday_mult != 1.0).astype(int)

    # Events (additivt, koblet til konkrete datoer)
    event_boost = pd.Series(0.0, index=df.index)
    df["is_event"] = 0
    for d_str, boost in EVENT_BOOST.items():
        d = pd.Timestamp(d_str)
        # finn nærmeste ukestart
        idx = (df["date"] - d).abs().idxmin()
        event_boost.iloc[idx] = boost
        df.loc[idx, "is_event"] = 1

    # Strukturelle skift (gårdsbutikk og gårdscafé)
    df["shop_open"] = (df["date"] >= pd.Timestamp(SHOP_OPEN_DATE)).astype(int)
    df["cafe_open"] = (df["date"] >= pd.Timestamp(CAFE_OPEN_DATE)).astype(int)
    shift = SHOP_EFFECT * df["shop_open"] + CAFE_EFFECT * df["cafe_open"]

    # Sammensatt: kombiner ledd, multiplikativ helligdag, additiv event og skift
    core = (baseline + season) * holiday_mult
    visitors_clean = core + event_boost + shift

    # Støy
    noise = rng.normal(0, NOISE_SD, size=n)
    visitors = visitors_clean + noise
    # Sikre ikke-negative og runde
    visitors = np.maximum(0, np.round(visitors)).astype(int)

    df["visitors"] = visitors
    return df


# =============================================================================
# Steg 2: Feature engineering
# =============================================================================
def add_features(df: pd.DataFrame) -> pd.DataFrame:
    """Lager forklaringsvariabler til ML-modellen."""
    out = df.copy()

    # Trigonometriske sesongvariabler
    out["sin_week"] = np.sin(2 * np.pi * out["week"] / 52.0)
    out["cos_week"] = np.cos(2 * np.pi * out["week"] / 52.0)

    # Sommerflagg (uke 24-34)
    out["is_summer"] = ((out["week"] >= 24) & (out["week"] <= 34)).astype(int)
    # Vinterferie / jul (uke 50-52, 1-2)
    out["is_winter_break"] = ((out["week"] >= 50) | (out["week"] <= 2)).astype(int)

    # Lag-variabler (forrige uke, forrige år samme uke)
    out["lag_1"]  = out["visitors"].shift(1)
    out["lag_52"] = out["visitors"].shift(52)

    # Glidende gjennomsnitt (4 uker, kun historikk)
    out["rolling_mean_4"] = out["visitors"].shift(1).rolling(window=4, min_periods=1).mean()

    return out


# =============================================================================
# Steg 3: Modeller
# =============================================================================
def seasonal_naive_forecast(train: pd.Series, test_index_len: int, season_length: int = 52) -> np.ndarray:
    """
    Sesongnaiv: y_hat_t = y_{t - season_length}
    Krever at train har minst season_length observasjoner.
    """
    history = train.values.copy()
    preds = []
    for i in range(test_index_len):
        # Bruk verdien fra 52 uker tidligere i historikken (rullerende)
        preds.append(history[-season_length])
        # Forskyv historikken (her bruker vi den faktiske verdien som etter hvert kommer inn)
        # Men i ren forecast-modus, uten lekkasje, ruller vi prediksjonene:
        history = np.append(history, history[-season_length])
    return np.array(preds)


def train_random_forest(X_train: pd.DataFrame, y_train: pd.Series) -> RandomForestRegressor:
    """Trener Random Forest med definerte hyperparametere."""
    model = RandomForestRegressor(
        n_estimators=RF_N_ESTIMATORS,
        max_depth=RF_MAX_DEPTH,
        min_samples_leaf=RF_MIN_SAMPLES_LEAF,
        random_state=RF_RANDOM_STATE,
        n_jobs=-1,
    )
    model.fit(X_train, y_train)
    return model


# =============================================================================
# Steg 4: Evaluering og figurer
# =============================================================================
def evaluate(y_true: np.ndarray, y_pred: np.ndarray, label: str) -> dict:
    mae  = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    return {"model": label, "MAE": round(mae, 2), "RMSE": round(rmse, 2)}


def make_figures(df: pd.DataFrame, df_feat: pd.DataFrame, split_idx: int,
                 y_test: pd.Series, naive_pred: np.ndarray, rf_pred: np.ndarray,
                 rf_model, feat_names: list[str], out_dir: str) -> None:
    os.makedirs(out_dir, exist_ok=True)

    # --- Figur 1: Hele datasettet over tid med strukturelle skift markert ---
    fig, ax = plt.subplots(figsize=(11, 4.5))
    ax.plot(df["date"], df["visitors"], color="#1f4e78", linewidth=1.2, label="Ukentlige besøkstall")
    ax.axvline(pd.Timestamp(SHOP_OPEN_DATE), color="#c00000", linestyle="--", linewidth=1.2, label="Gårdsbutikk åpner (nov 2024)")
    ax.axvline(pd.Timestamp(CAFE_OPEN_DATE), color="#2e7d32", linestyle="--", linewidth=1.2, label="Gårdscafé åpner (juni 2025)")
    ax.set_title("Ukentlige besøkstall ved Mannsverk Gård (simulert, 2022–2025)")
    ax.set_xlabel("Dato")
    ax.set_ylabel("Antall besøkende")
    ax.xaxis.set_major_locator(YearLocator())
    ax.xaxis.set_major_formatter(DateFormatter("%Y"))
    ax.legend(loc="upper left", frameon=False)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(f"{out_dir}/01_dataset_overview.png", dpi=150)
    plt.close(fig)

    # --- Figur 2: Gjennomsnittlig årssyklus per uke ---
    weekly = df.groupby("week")["visitors"].mean()
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.bar(weekly.index, weekly.values, color="#2e75b6")
    ax.set_title("Gjennomsnittlig besøk per ISO-uke (2022–2025)")
    ax.set_xlabel("Uke")
    ax.set_ylabel("Gjennomsnittlig antall besøkende")
    ax.grid(alpha=0.3, axis="y")
    fig.tight_layout()
    fig.savefig(f"{out_dir}/02_seasonal_profile.png", dpi=150)
    plt.close(fig)

    # --- Figur 3: Prediksjoner vs faktisk på testsett ---
    test_dates = df_feat.loc[split_idx:, "date"].values
    fig, ax = plt.subplots(figsize=(11, 4.5))
    ax.plot(test_dates, y_test.values, color="black", linewidth=1.4, label="Faktisk (test)")
    ax.plot(test_dates, naive_pred, color="#c00000", linewidth=1.2, linestyle="--", label="Sesongnaiv prediksjon")
    ax.plot(test_dates, rf_pred,    color="#2e7d32", linewidth=1.4, label="Random Forest prediksjon")
    ax.set_title("Modellprediksjoner mot faktiske besøkstall (testperiode)")
    ax.set_xlabel("Dato")
    ax.set_ylabel("Antall besøkende")
    ax.legend(loc="upper left", frameon=False)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(f"{out_dir}/03_predictions.png", dpi=150)
    plt.close(fig)

    # --- Figur 4: Residualer ---
    naive_res = y_test.values - naive_pred
    rf_res    = y_test.values - rf_pred
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    axes[0].plot(test_dates, naive_res, color="#c00000", label="Sesongnaiv", linewidth=1.2)
    axes[0].plot(test_dates, rf_res,    color="#2e7d32", label="Random Forest", linewidth=1.2)
    axes[0].axhline(0, color="black", linewidth=0.8)
    axes[0].set_title("Residualer over tid")
    axes[0].set_xlabel("Dato")
    axes[0].set_ylabel("Residual (faktisk - prediksjon)")
    axes[0].legend(frameon=False)
    axes[0].grid(alpha=0.3)

    axes[1].hist(naive_res, bins=15, alpha=0.6, color="#c00000", label="Sesongnaiv")
    axes[1].hist(rf_res,    bins=15, alpha=0.6, color="#2e7d32", label="Random Forest")
    axes[1].axvline(0, color="black", linewidth=0.8)
    axes[1].set_title("Fordeling av prognosefeil")
    axes[1].set_xlabel("Residual")
    axes[1].set_ylabel("Antall observasjoner")
    axes[1].legend(frameon=False)
    axes[1].grid(alpha=0.3, axis="y")
    fig.tight_layout()
    fig.savefig(f"{out_dir}/04_residuals.png", dpi=150)
    plt.close(fig)

    # --- Figur 5: Variabelviktighet (permutasjonsbasert) ---
    X_test = df_feat.loc[split_idx:, feat_names]
    y_test_ = df_feat.loc[split_idx:, "visitors"]
    result = permutation_importance(rf_model, X_test, y_test_, n_repeats=20,
                                    random_state=RF_RANDOM_STATE, n_jobs=-1)
    importances = pd.Series(result.importances_mean, index=feat_names).sort_values()
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(importances.index, importances.values, color="#2e75b6")
    ax.set_title("Permutasjonsbasert variabelviktighet — Random Forest")
    ax.set_xlabel("Reduksjon i R² ved permutering")
    ax.grid(alpha=0.3, axis="x")
    fig.tight_layout()
    fig.savefig(f"{out_dir}/05_feature_importance.png", dpi=150)
    plt.close(fig)


# =============================================================================
# Main pipeline
# =============================================================================
def main():
    os.makedirs("data", exist_ok=True)
    os.makedirs("figures", exist_ok=True)
    os.makedirs("results", exist_ok=True)

    print("=" * 70)
    print("LOG650 G13 - Mannsverk Gård: Forecasting pipeline")
    print("=" * 70)

    # 1. Simulering
    df = simulate_weekly_data()
    print(f"\n[1] Datasett generert: {len(df)} ukentlige observasjoner")
    print(f"    Periode: {df['date'].iloc[0].date()} – {df['date'].iloc[-1].date()}")
    print(f"    Min/snitt/maks besøk: {df['visitors'].min()} / "
          f"{df['visitors'].mean():.1f} / {df['visitors'].max()}")
    df.to_csv("data/mannsverk_weekly.csv", index=False)

    # 2. Feature engineering
    df_feat = add_features(df)
    df_feat = df_feat.dropna().reset_index(drop=True)
    print(f"[2] Etter feature engineering og dropna: {len(df_feat)} observasjoner")

    # Definer features og target
    feat_names = [
        "t", "week", "sin_week", "cos_week",
        "is_summer", "is_winter_break", "is_holiday", "is_event",
        "shop_open", "cafe_open",
        "lag_1", "lag_52", "rolling_mean_4",
    ]
    X = df_feat[feat_names]
    y = df_feat["visitors"]

    # 3. Kronologisk 80/20-splitt
    split_idx = int(len(df_feat) * (1 - TEST_FRACTION))
    X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
    y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]
    print(f"[3] Splitt: trening {len(X_train)}, test {len(X_test)} observasjoner")

    # 4. Sesongnaiv referansemodell
    naive_pred = seasonal_naive_forecast(y_train, len(y_test), season_length=52)
    naive_metrics = evaluate(y_test.values, naive_pred, "Sesongnaiv")
    print(f"[4] Sesongnaiv: MAE={naive_metrics['MAE']:.2f}, RMSE={naive_metrics['RMSE']:.2f}")

    # 5. Random Forest
    rf_model = train_random_forest(X_train, y_train)
    rf_pred  = rf_model.predict(X_test)
    rf_metrics = evaluate(y_test.values, rf_pred, "Random Forest")
    print(f"[5] Random Forest: MAE={rf_metrics['MAE']:.2f}, RMSE={rf_metrics['RMSE']:.2f}")

    # 6. Lagre resultater
    results = pd.DataFrame([naive_metrics, rf_metrics])
    mae_improve_pct  = (1 - rf_metrics["MAE"]  / naive_metrics["MAE"])  * 100
    rmse_improve_pct = (1 - rf_metrics["RMSE"] / naive_metrics["RMSE"]) * 100
    results.loc[len(results)] = {
        "model": "Forbedring RF vs sesongnaiv (%)",
        "MAE":  round(mae_improve_pct, 1),
        "RMSE": round(rmse_improve_pct, 1),
    }
    results.to_csv("results/metrics.csv", index=False)
    print(f"\n[6] Forbedring RF vs sesongnaiv:")
    print(f"    MAE  reduksjon: {mae_improve_pct:+.1f} %")
    print(f"    RMSE reduksjon: {rmse_improve_pct:+.1f} %")

    # 7. Figurer
    make_figures(df, df_feat, split_idx, y_test, naive_pred, rf_pred,
                 rf_model, feat_names, out_dir="figures")
    print("[7] Figurer lagret i figures/")

    print("\n" + "=" * 70)
    print("FERDIG. Se data/, figures/ og results/ for output.")
    print("=" * 70)


if __name__ == "__main__":
    main()
