"""Completes 100% of all missing models from base paper (Allaga et al., 2026):
- Multi-class (Tables 6 & 9): Gradient Boosting, OvO K-N
- Binary (Tables 5 & 8): Gradient Boosting, One-vs-Rest (OvR), One-vs-One (OvO)
Appends directly to multiclass_corrected.csv and binary_corrected.csv.
"""
import time, numpy as np, pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, label_binarize
from sklearn.metrics import (accuracy_score, precision_score, recall_score, f1_score, matthews_corrcoef,
                             balanced_accuracy_score, roc_auc_score, average_precision_score)
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.multiclass import OneVsOneClassifier, OneVsRestClassifier
from imblearn.over_sampling import SMOTE
from prep import get_split, load_clean, ROOT, SEED

MC_OUT = ROOT / "results" / "tables" / "multiclass_corrected.csv"
BIN_OUT = ROOT / "results" / "tables" / "binary_corrected.csv"

def run_multiclass_completions():
    print("=== Running Multi-Class Completions (Gradient Boosting & OvO K-N) ===", flush=True)
    d = get_split(drop_cols=("timestamp",))
    
    mc_models = {
        "Gradient Boosting": lambda: GradientBoostingClassifier(n_estimators=100, max_depth=3, random_state=SEED),
        "OvO K-N": lambda: OneVsOneClassifier(KNeighborsClassifier(n_neighbors=5), n_jobs=-1),
    }
    
    prev = pd.read_csv(MC_OUT) if MC_OUT.exists() else pd.DataFrame()
    done = set(zip(prev.Model, prev.Dataset)) if len(prev) else set()
    
    for name, factory in mc_models.items():
        for ds, (Xtr, ytr) in {"Original": (d["Xtr"], d["ytr"]), "SMOTE": (d["Xtr_s"], d["ytr_s"])}.items():
            if (name, ds) in done:
                print(f"Skipping {name} ({ds}) - already present.", flush=True)
                continue
            print(f"Training {name} on {ds} multi-class...", flush=True)
            m = factory()
            t0 = time.perf_counter()
            m.fit(Xtr, ytr)
            tr_t = time.perf_counter() - t0
            
            t0 = time.perf_counter()
            pred = m.predict(d["Xte"])
            te_t = time.perf_counter() - t0
            
            # Predict probabilities if supported
            if hasattr(m, "predict_proba"):
                proba = m.predict_proba(d["Xte"])
                Y = label_binarize(d["yte"], classes=list(range(6)))
                roc_auc = roc_auc_score(d["yte"], proba, multi_class="ovr", average="macro")
                pr_auc = average_precision_score(Y, proba, average="macro")
            else:
                roc_auc = np.nan
                pr_auc = np.nan
                
            acc = accuracy_score(d["yte"], pred)
            f1w = f1_score(d["yte"], pred, average="weighted", zero_division=0)
            T = te_t
            
            row = dict(
                Model=name, Dataset=ds, Accuracy=acc,
                Precision_w=precision_score(d["yte"], pred, average="weighted", zero_division=0),
                Recall_w=recall_score(d["yte"], pred, average="weighted", zero_division=0),
                F1_weighted=f1w,
                F1_macro=f1_score(d["yte"], pred, average="macro", zero_division=0),
                MCC=matthews_corrcoef(d["yte"], pred),
                Balanced_Acc=balanced_accuracy_score(d["yte"], pred),
                ROC_AUC_macro=roc_auc,
                PR_AUC_macro=pr_auc,
                Train_s=round(tr_t, 3),
                Infer_s=round(te_t, 3),
                Timing_runs=1,
                PES=((acc + f1w) / 2) / np.log(1 + T),
                PES_pct=((acc * 100 + f1w * 100) / 2) / np.log(1 + T)
            )
            pd.DataFrame([row]).to_csv(MC_OUT, mode="a", header=not MC_OUT.exists(), index=False)
            print(f"  Done: {name:20s} {ds:8s} | Acc: {acc:.4f} | wF1: {f1w:.4f} | MCC: {row['MCC']:.4f} | Train: {tr_t:.1f}s", flush=True)

def run_binary_completions():
    print("\n=== Running Binary Completions (Gradient Boosting, OvR, OvO) ===", flush=True)
    df = load_clean()
    y = (df.label == "legitimate").astype(int).values
    X = df.drop(columns=["label", "timestamp"])
    
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.20, random_state=SEED, stratify=y)
    sc = StandardScaler().fit(Xtr)
    Xtr_s, Xte_s = sc.transform(Xtr), sc.transform(Xte)
    Xsm, ysm = SMOTE(random_state=SEED).fit_resample(Xtr_s, ytr)
    
    # Balanced by undersampling
    leg = df[df.label == "legitimate"]
    att = df[df.label != "legitimate"]
    N = len(leg)
    samp = pd.concat([att[att.label == l].sample(n=round((att.label == l).sum() / len(att) * N), random_state=SEED) for l in sorted(att.label.unique())])
    if len(samp) > N: samp = samp.sample(n=N, random_state=SEED)
    elif len(samp) < N: samp = pd.concat([samp, att.drop(samp.index).sample(n=N - len(samp), random_state=SEED)])
    bal = pd.concat([leg, samp]).sample(frac=1, random_state=SEED)
    yb = (bal.label == "legitimate").astype(int).values
    Xb = bal.drop(columns=["label", "timestamp"])
    Xbtr, Xbte, ybtr, ybte = train_test_split(Xb, yb, test_size=0.20, random_state=SEED, stratify=yb)
    scb = StandardScaler().fit(Xbtr)
    Xbtr_s, Xbte_s = scb.transform(Xbtr), scb.transform(Xbte)
    
    bin_models = {
        "Gradient Boosting": lambda: GradientBoostingClassifier(n_estimators=100, max_depth=3, random_state=SEED),
        "One-vs-Rest (OvR)": lambda: OneVsRestClassifier(RandomForestClassifier(n_estimators=100, random_state=SEED, n_jobs=-1)),
        "One-vs-One (OvO)": lambda: OneVsOneClassifier(KNeighborsClassifier(n_neighbors=5), n_jobs=-1),
    }
    
    prev = pd.read_csv(BIN_OUT) if BIN_OUT.exists() else pd.DataFrame()
    done = set(zip(prev.Scenario, prev.Model)) if len(prev) else set()
    
    for name, factory in bin_models.items():
        for scen, (X_t, y_t, X_v, y_v) in {
            "Imbalanced": (Xtr_s, ytr, Xte_s, yte),
            "SMOTE": (Xsm, ysm, Xte_s, yte),
            "Balanced-undersample": (Xbtr_s, ybtr, Xbte_s, ybte)
        }.items():
            if (scen, name) in done:
                print(f"Skipping {name} ({scen}) - already present.", flush=True)
                continue
            print(f"Training binary {name} on {scen}...", flush=True)
            m = factory()
            t0 = time.perf_counter()
            m.fit(X_t, y_t)
            tr_t = time.perf_counter() - t0
            
            t0 = time.perf_counter()
            p = m.predict(X_v)
            te_t = time.perf_counter() - t0
            
            if hasattr(m, "predict_proba"):
                pr = m.predict_proba(X_v)[:, 1]
                roc_auc = roc_auc_score(y_v, pr)
                pr_auc = average_precision_score(y_v, pr)
            else:
                roc_auc = np.nan
                pr_auc = np.nan
                
            acc = accuracy_score(y_v, p)
            f1 = f1_score(y_v, p, zero_division=0)
            row = dict(
                Scenario=scen, Model=name, Accuracy=acc,
                Precision_legit=precision_score(y_v, p, zero_division=0),
                Recall_legit=recall_score(y_v, p, zero_division=0),
                F1_legit=f1,
                F1_attack=f1_score(y_v, p, pos_label=0, zero_division=0),
                MCC=matthews_corrcoef(y_v, p),
                Balanced_Acc=balanced_accuracy_score(y_v, p),
                ROC_AUC=roc_auc,
                PR_AUC=pr_auc,
                Train_s=round(tr_t, 3),
                Infer_s=round(te_t, 3),
                PES=((acc + f1) / 2) / np.log(1 + te_t)
            )
            pd.DataFrame([row]).to_csv(BIN_OUT, mode="a", header=not BIN_OUT.exists(), index=False)
            print(f"  Done: {name:20s} {scen:20s} | Acc: {acc:.4f} | F1(legit): {f1:.4f} | MCC: {row['MCC']:.4f}", flush=True)

if __name__ == "__main__":
    run_multiclass_completions()
    run_binary_completions()
    print("\nALL 100% BASELINE EXPERIMENTS COMPLETED SUCCESSFULLY!", flush=True)
