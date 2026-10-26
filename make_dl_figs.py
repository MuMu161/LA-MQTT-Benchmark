import pandas as pd, numpy as np, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from prep import ROOT
plt.rcParams.update({"font.size": 10, "font.family": "serif"})
h = pd.read_csv(ROOT / "results/tables/dl_long_epoch_history.csv")
for fs, tag in [("All 11 features", "all"), ("Without tcp_time_delta", "notime")]:
    fig, axs = plt.subplots(2, 4, figsize=(16, 6.4), sharex=True)
    for j, k in enumerate(["ANN", "1D-CNN", "SimpleRNN", "LSTM"]):
        d = h[(h.Features == fs) & (h.Model == k)]
        axs[0, j].plot(d.Epoch, d.Train_Acc * 100, "o-", ms=3, label="Train"); axs[0, j].plot(d.Epoch, d.Val_Acc * 100, "s--", ms=3, label="Validation")
        axs[1, j].plot(d.Epoch, d.Train_Loss, "o-", ms=3, label="Train"); axs[1, j].plot(d.Epoch, d.Val_Loss, "s--", ms=3, label="Validation")
        axs[0, j].set_title(k, fontweight="bold"); axs[1, j].set_xlabel("Epoch")
        for a in axs[:, j]: a.grid(alpha=.3)
    axs[0, 0].set_ylabel("Accuracy (%)"); axs[1, 0].set_ylabel("Loss"); axs[0, 0].legend(fontsize=8)
    fig.suptitle(f"Accuracy and loss per epoch ({fs})", fontweight="bold"); fig.tight_layout()
    fig.savefig(ROOT / f"results/figures/dl_long_epoch_curves_{tag}.png", dpi=300); plt.close(fig)
print("saved")
