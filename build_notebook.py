import nbformat as nbf
nb = nbf.v4.new_notebook(); C = []
md = lambda s: C.append(nbf.v4.new_markdown_cell(s)); code = lambda s: C.append(nbf.v4.new_code_cell(s))
md("""# MQTTEEB-D: Replication and Leakage Audit
Corrected, paper-aligned pipeline for *MQTTEEB-D: A high-fidelity benchmark for real-time MQTT anomaly detection using machine learning techniques* (Allaga et al., Ad Hoc Networks 181, 2026).

**How to use this notebook**
1. Keep your dataset where it already is: `data/MQTTEEB-D_Final_Dataset/Preprocessed_Data/MQTTEEB-D_cleaned_data.csv`.
2. Click **Kernel > Restart & Run All**. By default the notebook only *loads the saved results* (takes seconds).
3. To retrain everything from scratch, set `RUN_HEAVY = True` in the next cell (takes several hours on a laptop).

The same code lives in the `.py` files next to this notebook (`prep.py`, `run_*.py`); this notebook is the single place that ties them together.""")
code("""import sys, subprocess, pandas as pd, numpy as np
from pathlib import Path
from IPython.display import Image, display
pd.set_option("display.width", 200); pd.set_option("display.max_columns", 30)
ROOT = Path.cwd(); T = ROOT / "results" / "tables"; F = ROOT / "results" / "figures"
RUN_HEAVY = False   # True = retrain every experiment (slow)

def run_script(name):
    if RUN_HEAVY: subprocess.run([sys.executable, str(ROOT / name)], check=True)
def table(name, **kw): return pd.read_csv(T / name, **kw)
def fig(name, width=900): display(Image(filename=str(F / name), width=width))""")
md("## 1. Dataset and preprocessing\nSteps follow the paper: drop the 246 unlabelled rows, convert the four hexadecimal fields to integers, drop `timestamp`, stratified 80:20 split (seed 42), Z-score scaling fitted on the training set only, SMOTE on the training set only.")
code("""from prep import CSV
if CSV.exists():
    from prep import get_split, load_clean, CLASS_NAMES
    df = load_clean(); d = get_split()
    print("rows after dropping unlabelled:", len(df), "| train:", d["Xtr"].shape, "| test:", d["Xte"].shape, "| SMOTE train:", d["Xtr_s"].shape)
    print("features used:", d["cols"])
    print("\\nclass distribution (%):"); print((df.label.value_counts(normalize=True) * 100).round(2).to_string())
    same = (df.timestamp == df.tcp_time_delta).mean()
    print(f"\\nShare of rows where tcp_time_delta == timestamp: {same:.0%}")
else:
    print("Dataset not found in data/. The dataset file was not found; saved results below still load.")""")
md("**Finding:** `tcp_time_delta` is an exact copy of `timestamp`. The paper drops `timestamp` to avoid temporal leakage, but the duplicate stays in the feature set. Section 6 measures the effect.")
md("## 2. Multi-class benchmark (original vs SMOTE)\nAll classical models, with ROC-AUC and PR-AUC. PES uses the paper's Table 3 scale.")
code("""run_script("run_multiclass.py")
m = table("multiclass_corrected.csv")
m[["Model","Dataset","Accuracy","F1_weighted","MCC","ROC_AUC_macro","PR_AUC_macro","Train_s","Infer_s","PES"]].round(4)""")
md("### Comparison with the base paper")
code("""table("PAPER_VS_OURS_multiclass.csv")""")
md("*Gradient Boosting (tuned)* is not retrained here (about 30 minutes on one CPU core). Validated-tuning values from the original notebook: 0.9801 weighted F1 (original) and 0.9289 (SMOTE).")
md("## 3. Binary classification (legitimate = positive class)\nThe paper reports F1 for the minority class. Scenarios: imbalanced, SMOTE, and balanced by undersampling.")
code("""run_script("run_binary.py")
b = table("binary_corrected.csv")
b.pivot(index="Model", columns="Scenario", values="F1_legit").round(3)""")
code("""b[b.Scenario == "Imbalanced"][["Model","Accuracy","Precision_legit","Recall_legit","F1_legit","MCC","ROC_AUC","PR_AUC"]].round(3)""")
md("## 4. Corrected 5-fold cross-validation\nScaling and SMOTE are fitted inside each fold, in float64.")
code("""run_script("run_cv.py")
cv = table("cv5_corrected.csv")
cv.groupby(["Model","Condition"])[["Accuracy","F1_weighted","MCC","ROC_AUC_macro","PR_AUC_macro"]].agg(["mean","std"]).round(4)""")
md("## 5. Confusion matrices, ROC and PR curves")
code("""for n in ["Bagging_Original", "Random_Forest_Original", "XGBoost_Original", "Bagging_SMOTE"]:
    print(n.replace("_", " ")); fig(f"CM_{n}.png", 520); fig(f"ROC_PR_{n}.png", 900)""")
md("## 6. Ablation: the timestamp duplicate (`tcp_time_delta`)\nTwo protocols: the paper's random 80:20 split, and leave-one-loop-out (train on three capture loops, test on the fourth).")
code("""run_script("run_ablation.py")
a = table("ablation_timestamp.csv")
a.groupby(["Model","Protocol","Features"])["Accuracy"].mean().unstack("Features").round(3)""")
code("""fig("ablation_timestamp_leakage.png", 900)""")
md("## 7. t-SNE before and after preprocessing")
code("""fig("tsne_before_after.png", 1100)""")
md("## 8. Deep learning (ANN, 1D-CNN, SimpleRNN, LSTM)\nUp to 40 epochs with early stopping on validation loss. Per-epoch accuracy and loss are shown below.")
code("""run_script("run_dl_long.py")
table("dl_long_results.csv")[["Features","Model","Accuracy","F1_weighted","MCC","ROC_AUC_macro","PR_AUC_macro","Train_s","Infer_s","Epochs"]].round(3)""")
code("""fig("dl_long_epoch_curves_all.png", 1100)""")
md("## 9. Conclusions\n* Tree models reproduce the paper's results on the paper's protocol (about 0.97 to 0.99).\n* The same models fall to roughly 41 to 52% accuracy on an unseen capture loop when `tcp_time_delta` is kept, and about 71% without it.\n* Without the timestamp duplicate, Brute Force, Flood and Malformed remain detectable; DoS, SlowITe and Legitimate are confused with Malformed and Brute Force.")
nb["cells"] = C; nb["metadata"] = {"kernelspec": {"name": "python3", "display_name": "Python 3", "language": "python"}}
nbf.write(nb, "MQTTEEB-D_Final.ipynb"); print("written", len(C), "cells")
