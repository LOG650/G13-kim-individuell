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
