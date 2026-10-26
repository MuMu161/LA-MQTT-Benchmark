"""Binary task (legitimate = POSITIVE/minority class, as in the paper's Table 5/8).
Three scenarios: imbalanced original, SMOTE, and balanced-by-undersampling (paper: 'balanced without SMOTE')."""
import time, numpy as np, pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (accuracy_score, precision_score, recall_score, f1_score, matthews_corrcoef,
                             balanced_accuracy_score, roc_auc_score, average_precision_score)
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, BaggingClassifier, ExtraTreesClassifier, GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier
from imblearn.over_sampling import SMOTE
from prep import load_clean, ROOT, SEED
OUT = ROOT / "results" / "tables" / "binary_corrected.csv"
MODELS = {
 "CART": lambda: DecisionTreeClassifier(random_state=SEED),
 "Extra Trees": lambda: ExtraTreesClassifier(n_estimators=100, random_state=SEED, n_jobs=1),
 "Bagging": lambda: BaggingClassifier(random_state=SEED, n_jobs=1),
 "Random Forest": lambda: RandomForestClassifier(n_estimators=100, random_state=SEED, n_jobs=1),
 "LightGBM": lambda: LGBMClassifier(random_state=SEED, n_jobs=1, verbose=-1),
 "XGBoost": lambda: XGBClassifier(random_state=SEED, n_jobs=1, tree_method="hist"),
 "CatBoost": lambda: CatBoostClassifier(iterations=200, random_seed=SEED, verbose=0, thread_count=1, allow_writing_files=False),
}
done_bin = None
DONE = set(map(tuple, pd.read_csv(OUT)[['Scenario','Model']].values)) if OUT.exists() else set()
def run(name, factory, scen, Xtr, ytr, Xte, yte):
    if (scen, name) in DONE: return
    m = factory(); t = time.perf_counter(); m.fit(Xtr, ytr); tr = time.perf_counter() - t
    t = time.perf_counter(); p = m.predict(Xte); te = time.perf_counter() - t
    pr = m.predict_proba(Xte)[:, 1]; acc = accuracy_score(yte, p); f1 = f1_score(yte, p, zero_division=0)
    row = dict(Scenario=scen, Model=name, Accuracy=acc, Precision_legit=precision_score(yte, p, zero_division=0),
               Recall_legit=recall_score(yte, p, zero_division=0), F1_legit=f1,
               F1_attack=f1_score(yte, p, pos_label=0, zero_division=0), MCC=matthews_corrcoef(yte, p),
               Balanced_Acc=balanced_accuracy_score(yte, p), ROC_AUC=roc_auc_score(yte, pr),
               PR_AUC=average_precision_score(yte, pr), Train_s=tr, Infer_s=te,
               PES=((acc + f1) / 2) / np.log(1 + te))
    pd.DataFrame([row]).to_csv(OUT, mode="a", header=not OUT.exists(), index=False)
    print(f"[{time.strftime('%H:%M:%S')}] {scen:16s} {name:18s} acc={acc:.4f} F1(legit)={f1:.4f} MCC={row['MCC']:.4f} R(legit)={row['Recall_legit']:.3f}", flush=True)

if __name__ == "__main__":
    df = load_clean(); y = (df.label == "legitimate").astype(int).values; X = df.drop(columns=["label", "timestamp"])
    # --- Scenarios 1 & 2: full data, original and SMOTE-balanced training set
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=.2, random_state=SEED, stratify=y)
    sc = StandardScaler().fit(Xtr); Xtr_s, Xte_s = sc.transform(Xtr), sc.transform(Xte)
    Xsm, ysm = SMOTE(random_state=SEED).fit_resample(Xtr_s, ytr)
    # --- Scenario 3: balanced by undersampling (N legit + N attack, attack classes sampled proportionally)
    leg = df[df.label == "legitimate"]; att = df[df.label != "legitimate"]; N = len(leg)
    samp = pd.concat([att[att.label == l].sample(n=round((att.label == l).sum() / len(att) * N), random_state=SEED) for l in sorted(att.label.unique())])
    if len(samp) > N: samp = samp.sample(n=N, random_state=SEED)
    elif len(samp) < N: samp = pd.concat([samp, att.drop(samp.index).sample(n=N - len(samp), random_state=SEED)])
    bal = pd.concat([leg, samp]).sample(frac=1, random_state=SEED)
    yb = (bal.label == "legitimate").astype(int).values; Xb = bal.drop(columns=["label", "timestamp"])
    Xbtr, Xbte, ybtr, ybte = train_test_split(Xb, yb, test_size=.2, random_state=SEED, stratify=yb)
    scb = StandardScaler().fit(Xbtr); Xbtr, Xbte = scb.transform(Xbtr), scb.transform(Xbte)
    print("balanced set:", len(bal), "train", Xbtr.shape, flush=True)
    for name, f in MODELS.items():
        run(name, f, "Imbalanced", Xtr_s, ytr, Xte_s, yte)
        run(name, f, "SMOTE", Xsm, ysm, Xte_s, yte)
        run(name, f, "Balanced-undersample", Xbtr, ybtr, Xbte, ybte)
    print("ALL DONE", flush=True)
