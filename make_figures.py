"""Publication figures from saved predictions: normalized confusion matrix, per-class ROC (with AUC), per-class PR (with AP)."""
import sys, numpy as np, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.metrics import confusion_matrix, roc_curve, auc, precision_recall_curve, average_precision_score
from sklearn.preprocessing import label_binarize
from prep import ROOT, CLASS_NAMES
PRED, FIG = ROOT / "results" / "preds", ROOT / "results" / "figures"
NICE = ["Brute Force", "DoS", "Flood", "Legitimate", "Malformed", "SlowITe"]
plt.rcParams.update({"font.size": 10, "axes.titlesize": 11, "axes.titleweight": "bold", "font.family": "serif"})

def figs_for(npz_path):
    d = np.load(npz_path); y, p, pr = d["y_true"], d["y_pred"], d["proba"]; tag = npz_path.stem
    title = tag.replace("_", " ")
    cm = confusion_matrix(y, p, normalize="true")
    fig, ax = plt.subplots(figsize=(6, 5)); im = ax.imshow(cm, cmap="Blues", vmin=0, vmax=1)
    ax.set_xticks(range(6)); ax.set_yticks(range(6)); ax.set_xticklabels(NICE, rotation=45, ha="right"); ax.set_yticklabels(NICE)
    for i in range(6):
        for j in range(6): ax.text(j, i, f"{cm[i,j]*100:.1f}", ha="center", va="center", color="white" if cm[i, j] > .5 else "black", fontsize=8)
    ax.set_xlabel("Predicted"); ax.set_ylabel("Actual"); ax.set_title(f"Confusion matrix (%): {title}"); fig.colorbar(im, fraction=.046)
    fig.tight_layout(); fig.savefig(FIG / f"CM_{tag}.png", dpi=300); plt.close(fig)
    Y = label_binarize(y, classes=range(6))
    fig, axs = plt.subplots(1, 2, figsize=(11, 4.5))
    for k in range(6):
        fpr, tpr, _ = roc_curve(Y[:, k], pr[:, k]); axs[0].plot(fpr, tpr, label=f"{NICE[k]} (AUC={auc(fpr, tpr):.3f})")
        r, pc = precision_recall_curve(Y[:, k], pr[:, k])[1::-1] if False else (None, None)
        P, R, _ = precision_recall_curve(Y[:, k], pr[:, k]); axs[1].plot(R, P, label=f"{NICE[k]} (AP={average_precision_score(Y[:, k], pr[:, k]):.3f})")
    axs[0].plot([0, 1], [0, 1], "k--", lw=.8); axs[0].set(xlabel="False positive rate", ylabel="True positive rate", title=f"ROC: {title}")
    axs[1].set(xlabel="Recall", ylabel="Precision", title=f"Precision-Recall: {title}", ylim=(0, 1.02))
    for a in axs: a.legend(fontsize=7, loc="lower right" if a is axs[0] else "lower left"); a.grid(alpha=.3)
    fig.tight_layout(); fig.savefig(FIG / f"ROC_PR_{tag}.png", dpi=300); plt.close(fig)

if __name__ == "__main__":
    targets = sys.argv[1:] or [str(p) for p in sorted(PRED.glob("*.npz"))]
    for t in targets:
        figs_for(Path(t)); print("figures:", Path(t).stem, flush=True)
