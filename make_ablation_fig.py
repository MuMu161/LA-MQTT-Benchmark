import pandas as pd, numpy as np, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from prep import ROOT
plt.rcParams.update({"font.size": 10, "font.family": "serif"})
d = pd.read_csv(ROOT / "results/tables/ablation_timestamp.csv")
m = d.groupby(["Model", "Protocol", "Features"])["Accuracy"].mean().reset_index()
models = ["CART", "Bagging", "Extra Trees", "Random Forest", "XGBoost"]
conds = [("Random 80/20 split", "All 11 features", "Random split, all features", "#c0392b"),
         ("Leave-one-loop-out", "All 11 features", "Unseen loop, all features", "#e67e22"),
         ("Random 80/20 split", "Without tcp_time_delta", "Random split, no tcp_time_delta", "#2980b9"),
         ("Leave-one-loop-out", "Without tcp_time_delta", "Unseen loop, no tcp_time_delta", "#27ae60")]
fig, ax = plt.subplots(figsize=(10, 4.8)); w = .2; x = np.arange(len(models))
for i, (pr, ft, lab, c) in enumerate(conds):
    v = [m[(m.Model == k) & (m.Protocol == pr) & (m.Features == ft)].Accuracy.iloc[0] * 100 for k in models]
    b = ax.bar(x + (i - 1.5) * w, v, w, label=lab, color=c)
    for r, val in zip(b, v): ax.text(r.get_x() + r.get_width() / 2, val + .8, f"{val:.0f}", ha="center", fontsize=7)
ax.set_xticks(x); ax.set_xticklabels(models); ax.set_ylabel("Accuracy (%)"); ax.set_ylim(0, 108)
ax.set_title("Effect of the timestamp-duplicate feature (tcp_time_delta) on accuracy", fontweight="bold")
ax.legend(fontsize=8, loc="upper center", bbox_to_anchor=(0.5, -0.08), ncol=4, frameon=False); ax.grid(axis="y", alpha=.3)
fig.tight_layout(); fig.savefig(ROOT / "results/figures/ablation_timestamp_leakage.png", dpi=300)
print("saved")
