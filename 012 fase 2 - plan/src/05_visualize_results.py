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
