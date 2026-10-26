"""Corrected multi-class benchmark: Original vs SMOTE, all classical models.
Adds ROC-AUC / PR-AUC, PES (both scales), saves predictions+probabilities for figures.
Resumable: skips (model, dataset) pairs already written."""
import time, sys, numpy as np, pandas as pd
from pathlib import Path
from sklearn.metrics import (accuracy_score, precision_score, recall_score, f1_score, matthews_corrcoef,
                             balanced_accuracy_score, roc_auc_score, average_precision_score)
from sklearn.preprocessing import label_binarize
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (RandomForestClassifier, BaggingClassifier, ExtraTreesClassifier,
                              GradientBoostingClassifier)
from sklearn.multiclass import OneVsRestClassifier
from sklearn.neighbors import KNeighborsClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier
from prep import get_split, ROOT

OUT = ROOT / "results" / "tables" / "multiclass_corrected.csv"
PRED = ROOT / "results" / "preds"
S = 42
MODELS = {  # fast -> slow so partial results arrive early
    "CART":             lambda: DecisionTreeClassifier(random_state=S),
    "Extra Trees":      lambda: ExtraTreesClassifier(n_estimators=100, random_state=S, n_jobs=1),
    "Bagging":          lambda: BaggingClassifier(random_state=S, n_jobs=1),
    "Random Forest":    lambda: RandomForestClassifier(n_estimators=100, random_state=S, n_jobs=1),
    "LightGBM":         lambda: LGBMClassifier(random_state=S, n_jobs=1, verbose=-1),
    "XGBoost":          lambda: XGBClassifier(random_state=S, n_jobs=1, tree_method="hist"),
    "CatBoost":         lambda: CatBoostClassifier(iterations=200, random_seed=S, verbose=0, thread_count=1, allow_writing_files=False),
    "K-NN (k=5)":       lambda: KNeighborsClassifier(n_neighbors=5),
    "OvR Random Forest":lambda: OneVsRestClassifier(RandomForestClassifier(n_estimators=100, random_state=S, n_jobs=1)),
}

def evaluate(model, Xtr, ytr, Xte, yte, repeats):
    tr_t, te_t = [], []
    for _ in range(repeats):
        m = model(); t = time.perf_counter(); m.fit(Xtr, ytr); tr_t.append(time.perf_counter() - t)
        t = time.perf_counter(); pred = m.predict(Xte); te_t.append(time.perf_counter() - t)
    proba = m.predict_proba(Xte)
    Y = label_binarize(yte, classes=list(range(6)))
    acc = accuracy_score(yte, pred); f1w = f1_score(yte, pred, average="weighted", zero_division=0)
    T = float(np.mean(te_t))
    row = dict(Accuracy=acc, Precision_w=precision_score(yte, pred, average="weighted", zero_division=0),
               Recall_w=recall_score(yte, pred, average="weighted", zero_division=0), F1_weighted=f1w,
               F1_macro=f1_score(yte, pred, average="macro", zero_division=0), MCC=matthews_corrcoef(yte, pred),
               Balanced_Acc=balanced_accuracy_score(yte, pred),
               ROC_AUC_macro=roc_auc_score(yte, proba, multi_class="ovr", average="macro"),
               PR_AUC_macro=average_precision_score(Y, proba, average="macro"),
               Train_s=float(np.mean(tr_t)), Infer_s=T, Timing_runs=repeats,
               PES=((acc + f1w) / 2) / np.log(1 + T),            # paper Table 3 scale (fractions)
               PES_pct=((acc * 100 + f1w * 100) / 2) / np.log(1 + T))  # paper Table 10 scale (percent)
    return row, pred, proba

if __name__ == "__main__":
    d = get_split(drop_cols=("timestamp",))
    done = set()
    if OUT.exists():
        prev = pd.read_csv(OUT); done = set(zip(prev.Model, prev.Dataset))
    for name, factory in MODELS.items():
        for ds, (Xtr, ytr) in {"Original": (d["Xtr"], d["ytr"]), "SMOTE": (d["Xtr_s"], d["ytr_s"])}.items():
            if (name, ds) in done: continue
            t0 = time.perf_counter()
            # time-average over 3 runs only when a single fit is cheap (<20 s); else 1 run (recorded in Timing_runs)
            probe = factory(); t = time.perf_counter(); probe.fit(Xtr, ytr); one = time.perf_counter() - t
            reps = 3 if one < 20 else 1
            row, pred, proba = evaluate(factory, Xtr, ytr, d["Xte"], d["yte"], reps)
            row = dict(Model=name, Dataset=ds, **row)
            pd.DataFrame([row]).to_csv(OUT, mode="a", header=not OUT.exists(), index=False)
            np.savez_compressed(PRED / f"{name.replace(' ','_').replace('(','').replace(')','').replace('=','')}_{ds}.npz",
                                y_true=d["yte"], y_pred=pred, proba=proba.astype(np.float32))
            print(f"[{time.strftime('%H:%M:%S')}] {name:28s} {ds:8s} acc={row['Accuracy']:.4f} wF1={row['F1_weighted']:.4f} "
                  f"MCC={row['MCC']:.4f} AUC={row['ROC_AUC_macro']:.4f} train={row['Train_s']:.1f}s  (total {time.perf_counter()-t0:.0f}s)", flush=True)
    print("ALL DONE", flush=True)
