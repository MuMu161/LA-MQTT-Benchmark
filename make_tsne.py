"""t-SNE before vs after preprocessing (raw hex-converted features vs standardised features), stratified 6,000-row sample."""
import numpy as np, pandas as pd, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from prep import load_clean, ROOT, SEED
plt.rcParams.update({"font.size": 10, "font.family": "serif"})
df = load_clean()
_, s = train_test_split(df, test_size=6000, random_state=SEED, stratify=df.label)
feats = [c for c in df.columns if c not in ("label", "timestamp")]
raw = s[feats].astype(float).fillna(0).values
# "before": raw values, only min-max scaled for display purposes is NOT applied -> raw scale (dominated by tcp_time_delta)
after = StandardScaler().fit_transform(raw)
names = {"bruteforce": "Brute Force", "dos": "DoS", "flood": "Flood", "legitimate": "Legitimate", "malformed": "Malformed", "slowite": "SlowITe"}
noT = StandardScaler().fit_transform(s[[c for c in feats if c != "tcp_time_delta"]].astype(float).fillna(0).values)
fig, axs = plt.subplots(1, 3, figsize=(17, 5.2))
for ax, X, ttl in [(axs[0], raw, "(a) Before preprocessing (raw features)"), (axs[1], after, "(b) After preprocessing (hex to int + Z-score)"), (axs[2], noT, "(c) After preprocessing, without tcp_time_delta")]:
    Z = TSNE(n_components=2, perplexity=30, init="pca", random_state=SEED).fit_transform(X)
    for lab, nm in names.items():
        m = (s.label == lab).values; ax.scatter(Z[m, 0], Z[m, 1], s=3, label=nm, alpha=.7)
    ax.set_title(ttl, fontweight="bold"); ax.set_xticks([]); ax.set_yticks([])
axs[2].legend(markerscale=4, fontsize=8, loc="best")
fig.tight_layout(); fig.savefig(ROOT / "results/figures/tsne_before_after.png", dpi=300); print("saved")
