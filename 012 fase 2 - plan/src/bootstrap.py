"""
bootstrap.py
Kjoer denne filen i src-mappen for aa opprette alle LOG650-script.
Bruk: python bootstrap.py
"""
from pathlib import Path

BASE = Path(__file__).parent
print(f"Oppretter filer i: {BASE}\n")

scripts = {}

scripts["00_setup_project.py"] = """\
from pathlib import Path
FOLDERS = ["data/raw","data/processed","models","results","plots","reports"]
def setup():
    base = Path(__file__).parent
    for f in FOLDERS:
        (base/f).mkdir(parents=True, exist_ok=True)
        print(f"  OK: {f}/")
    print("Mappestruktur klar!")
if __name__ == "__main__": setup()
"""

scripts["01_generate_data.py"] = """\
import numpy as np, pandas as pd
from pathlib import Path
OUT = Path(__file__).parent / "data/raw/inventory_volume_raw.csv"
def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(42)
    dates = pd.date_range("2022-01-03", periods=156, freq="W-MON")
    t = np.arange(156)
    trend = 500 + 0.8 * t
    season = 60 * np.sin(2 * np.pi * (dates.isocalendar().week.values.astype(float) - 10) / 52)
    camp = np.zeros(156)
    camp[rng.choice(156, 8, replace=False)] = rng.uniform(80, 200, 8)
    noise = rng.normal(0, 25, 156)
    vol = np.maximum(0, np.round(trend + season + camp + noise)).astype(int)
    df = pd.DataFrame({
        "date": dates, "week": dates.isocalendar().week.values,
        "year": dates.year, "volume": vol,
        "is_campaign": (camp > 0).astype(int)
    })
    df.to_csv(OUT, index=False)
    print(f"Radata lagret: {len(df)} rader, snitt volum={vol.mean():.0f}")
if __name__ == "__main__": main()
"""

scripts["02_preprocess_data.py"] = """\
import pandas as pd
from pathlib import Path
IN  = Path(__file__).parent / "data/raw/inventory_volume_raw.csv"
OUT = Path(__file__).parent / "data/processed/inventory_volume_features.csv"
def main():
    df = pd.read_csv(IN, parse_dates=["date"]).sort_values("date").reset_index(drop=True)
    for lag in [1, 2, 3, 4]:
        df[f"lag_{lag}"] = df["volume"].shift(lag)
    df["rolling_mean_4"] = df["volume"].shift(1).rolling(4).mean()
    df["rolling_mean_8"] = df["volume"].shift(1).rolling(8).mean()
    df["rolling_std_4"]  = df["volume"].shift(1).rolling(4).std()
    df = df.dropna().reset_index(drop=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT, index=False)
    print(f"Features lagret: {len(df)} rader, {len(df.columns)} kolonner")
if __name__ == "__main__": main()
"""

scripts["03_baseline_model.py"] = """\
import pandas as pd, numpy as np
from pathlib import Path
IN  = Path(__file__).parent / "data/processed/inventory_volume_features.csv"
OUT = Path(__file__).parent / "results/baseline_predictions.csv"
MET = Path(__file__).parent / "results/metrics_summary.csv"
def main():
    df   = pd.read_csv(IN, parse_dates=["date"])
    test = df.iloc[int(len(df)*0.8):].copy()
    test["y_pred"] = test["rolling_mean_4"].round()
    mae  = np.mean(np.abs(test["volume"] - test["y_pred"]))
    rmse = np.sqrt(np.mean((test["volume"] - test["y_pred"])**2))
    print(f"Baseline  MAE={mae:.2f}  RMSE={rmse:.2f}")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    test[["date","volume","y_pred"]].to_csv(OUT, index=False)
    pd.DataFrame([{"model":"Baseline","MAE":round(mae,2),"RMSE":round(rmse,2)}]).to_csv(MET, index=False)
if __name__ == "__main__": main()
"""

scripts["04_ml_model.py"] = """\
import pandas as pd, numpy as np, pickle
from pathlib import Path
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
IN   = Path(__file__).parent / "data/processed/inventory_volume_features.csv"
OUT  = Path(__file__).parent / "results/ml_predictions.csv"
MOD  = Path(__file__).parent / "models/random_forest.pkl"
MET  = Path(__file__).parent / "results/metrics_summary.csv"
FEAT = ["lag_1","lag_2","lag_3","lag_4","rolling_mean_4","rolling_mean_8","rolling_std_4","week","is_campaign"]
def main():
    df = pd.read_csv(IN, parse_dates=["date"])
    split = int(len(df)*0.8)
    tr, te = df.iloc[:split], df.iloc[split:].copy()
    m = RandomForestRegressor(n_estimators=200, max_depth=10, min_samples_leaf=5, random_state=42, n_jobs=-1)
    m.fit(tr[FEAT], tr["volume"])
    pred = np.maximum(0, m.predict(te[FEAT])).round()
    mae  = mean_absolute_error(te["volume"], pred)
    rmse = np.sqrt(np.mean((te["volume"] - pred)**2))
    print(f"Random Forest  MAE={mae:.2f}  RMSE={rmse:.2f}")
    te["y_pred"] = pred
    OUT.parent.mkdir(parents=True, exist_ok=True)
    te[["date","volume","y_pred"]].to_csv(OUT, index=False)
    MOD.parent.mkdir(parents=True, exist_ok=True)
    pickle.dump(m, open(MOD, "wb"))
    met = pd.read_csv(MET) if MET.exists() else pd.DataFrame()
    pd.concat([met, pd.DataFrame([{"model":"Random Forest","MAE":round(mae,2),"RMSE":round(rmse,2)}])], ignore_index=True).to_csv(MET, index=False)
if __name__ == "__main__": main()
"""

scripts["05_visualize_results.py"] = """\
import pandas as pd, numpy as np, matplotlib.pyplot as plt, pickle
from pathlib import Path
B    = Path(__file__).parent
FEAT = ["lag_1","lag_2","lag_3","lag_4","rolling_mean_4","rolling_mean_8","rolling_std_4","week","is_campaign"]

def save(fig, name):
    (B/"plots").mkdir(exist_ok=True)
    fig.savefig(B/"plots"/name, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"  Lagret: {name}")

def main():
    df = pd.read_csv(B/"data/raw/inventory_volume_raw.csv", parse_dates=["date"])
    fig, ax = plt.subplots(figsize=(12,4))
    ax.plot(df["date"], df["volume"], color="#2c3e50")
    ax.set(title="Figur 1: Lagervolum", xlabel="Dato", ylabel="Volum")
    save(fig, "fig1_raw.png")

    bl = pd.read_csv(B/"results/baseline_predictions.csv", parse_dates=["date"])
    ml = pd.read_csv(B/"results/ml_predictions.csv",      parse_dates=["date"])
    for df2, title, color, fname in [
        (bl, "Baseline",      "#e74c3c", "fig2_baseline.png"),
        (ml, "Random Forest", "#27ae60", "fig3_rf.png"),
    ]:
        fig, ax = plt.subplots(figsize=(12,4))
        ax.plot(df2["date"], df2["volume"], label="Faktisk",  color="#2c3e50")
        ax.plot(df2["date"], df2["y_pred"], label=title, ls="--", color=color)
        ax.legend()
        ax.set(title=f"Figur: {title}", xlabel="Dato", ylabel="Volum")
        save(fig, fname)

    met = pd.read_csv(B/"results/metrics_summary.csv")
    fig, axes = plt.subplots(1, 2, figsize=(10,4))
    for ax, metric in zip(axes, ["MAE","RMSE"]):
        bars = ax.bar(range(len(met)), met[metric], color=["#e74c3c","#27ae60"])
        ax.set_xticks(range(len(met)))
        ax.set_xticklabels(met["model"], rotation=10, ha="right")
        ax.set_title(metric)
        for b, v in zip(bars, met[metric]):
            ax.text(b.get_x()+b.get_width()/2, b.get_height()+0.3, f"{v:.1f}", ha="center")
    fig.tight_layout()
    save(fig, "fig4_metrics.png")

    mod = pickle.load(open(B/"models/random_forest.pkl","rb"))
    fi  = pd.Series(mod.feature_importances_, index=FEAT).sort_values()
    fig, ax = plt.subplots(figsize=(8,5))
    fi.plot.barh(ax=ax, color="#27ae60")
    ax.set_title("Feature importance")
    fig.tight_layout()
    save(fig, "fig5_importance.png")
    print("Alle figurer lagret i plots/")

if __name__ == "__main__": main()
"""

scripts["run_all.py"] = """\
import subprocess, sys
from pathlib import Path
SCRIPTS = ["00_setup_project.py","01_generate_data.py","02_preprocess_data.py",
           "03_baseline_model.py","04_ml_model.py","05_visualize_results.py"]
BASE = Path(__file__).parent
print("LOG650 Pipeline starter...")
for s in SCRIPTS:
    print(f"\\n--- {s} ---")
    r = subprocess.run([sys.executable, str(BASE/s)])
    if r.returncode != 0:
        print(f"FEIL i {s}")
        sys.exit(1)
print("\\nPipeline fullfort! Sjekk results/ og plots/")
"""

for filename, content in scripts.items():
    path = BASE / filename
    path.write_text(content, encoding="utf-8")
    print(f"  OK: {filename}")

print(f"\nAlle {len(scripts)} filer klar. Kjoer: python run_all.py")
