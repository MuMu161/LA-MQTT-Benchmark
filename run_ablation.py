"""Leakage audit. In MQTTEEB-D, tcp_time_delta is an exact copy of timestamp.
A) random 80/20 split with/without tcp_time_delta;  B) leave-one-loop-out (LOLO) with/without it."""
import time, numpy as np, pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, f1_score, matthews_corrcoef, balanced_accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, BaggingClassifier, ExtraTreesClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from sklearn.preprocessing import LabelEncoder
from prep import load_clean_with_loop, ROOT, SEED
OUT = ROOT / "results" / "tables" / "ablation_timestamp.csv"
MODELS = {
 "CART": lambda: DecisionTreeClassifier(random_state=SEED),
 "Extra Trees": lambda: ExtraTreesClassifier(n_estimators=100, random_state=SEED, n_jobs=1),
 "Bagging": lambda: BaggingClassifier(random_state=SEED, n_jobs=1),
 "Random Forest": lambda: RandomForestClassifier(n_estimators=100, random_state=SEED, n_jobs=1),
 "XGBoost": lambda: XGBClassifier(random_state=SEED, n_jobs=1, tree_method="hist"),
}
def fit_eval(factory, Xtr, ytr, Xte, yte):
    sc = StandardScaler().fit(Xtr); m = factory().fit(sc.transform(Xtr), ytr); p = m.predict(sc.transform(Xte))
    return dict(Accuracy=accuracy_score(yte, p), F1_weighted=f1_score(yte, p, average="weighted"),
                F1_macro=f1_score(yte, p, average="macro"), MCC=matthews_corrcoef(yte, p),
                Balanced_Acc=balanced_accuracy_score(yte, p))
def emit(**r):
    pd.DataFrame([r]).to_csv(OUT, mode="a", header=not OUT.exists(), index=False)
    print(f"[{time.strftime('%H:%M:%S')}] {r['Protocol']:22s} {r['Features']:24s} {r['Model']:14s} fold={r['Fold']} acc={r['Accuracy']:.4f} wF1={r['F1_weighted']:.4f}", flush=True)
if __name__ == "__main__":
    df = load_clean_with_loop(); y = LabelEncoder().fit_transform(df.label); loop = df["loop"].values
    full = df.drop(columns=["label", "timestamp", "loop"]); noT = full.drop(columns=["tcp_time_delta"])
    sets = {"All 11 features": full, "Without tcp_time_delta": noT}
    for name, f in MODELS.items():
        for fs, Xd in sets.items():
            # A) random stratified 80/20 (paper protocol)
            Xtr, Xte, ytr, yte = train_test_split(Xd, y, test_size=.2, random_state=SEED, stratify=y)
            emit(Protocol="Random 80/20 split", Features=fs, Model=name, Fold="-", **fit_eval(f, Xtr, ytr, Xte, yte))
            # B) leave-one-loop-out
            for L in range(1, 5):
                te = loop == L
                emit(Protocol="Leave-one-loop-out", Features=fs, Model=name, Fold=f"loop{L}",
                     **fit_eval(f, Xd[~te], y[~te], Xd[te], y[te]))
    print("ALL DONE", flush=True)
