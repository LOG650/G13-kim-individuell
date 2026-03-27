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
