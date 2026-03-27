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
