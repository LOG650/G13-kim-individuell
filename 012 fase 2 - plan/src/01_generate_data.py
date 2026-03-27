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
