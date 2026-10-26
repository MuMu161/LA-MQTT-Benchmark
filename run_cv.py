"""Corrected 5-fold stratified CV on the TRAIN set (float64, scaler + SMOTE fitted inside each fold).
Original-vs-SMOTE, with ROC-AUC / PR-AUC per fold. (The notebook version cast to float32, which destroyed the
precision of the timestamp-like tcp_time_delta and gave a misleading ~92% accuracy.)"""
import time, numpy as np, pandas as pd
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler, label_binarize
from sklearn.metrics import accuracy_score, f1_score, matthews_corrcoef, balanced_accuracy_score, roc_auc_score, average_precision_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, BaggingClassifier, ExtraTreesClassifier
from xgboost import XGBClassifier
from imblearn.over_sampling import SMOTE
from prep import load_clean, ROOT, SEED
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
OUT = ROOT / "results" / "tables" / "cv5_corrected.csv"
MODELS = {
 "CART": lambda: DecisionTreeClassifier(random_state=SEED),
 "Random Forest": lambda: RandomForestClassifier(n_estimators=100, random_state=SEED, n_jobs=1),
 "XGBoost": lambda: XGBClassifier(random_state=SEED, n_jobs=1, tree_method="hist"),
}
if __name__ == "__main__":
    df = load_clean(); y = LabelEncoder().fit_transform(df.label); X = df.drop(columns=["label", "timestamp"]).values.astype(np.float64)
    Xtr, _, ytr, _ = train_test_split(X, y, test_size=.2, random_state=SEED, stratify=y)   # CV only on the training portion
    skf = StratifiedKFold(5, shuffle=True, random_state=SEED)
    done_cv = set(map(tuple, pd.read_csv(OUT)[['Model','Condition','Fold']].values)) if OUT.exists() else set()
    for name, f in MODELS.items():
        for cond in ["Original", "SMOTE"]:
            for k, (a, b) in enumerate(skf.split(Xtr, ytr), 1):
                if (name, cond, k) in done_cv: continue
                sc = StandardScaler().fit(Xtr[a]); A, B = sc.transform(Xtr[a]), sc.transform(Xtr[b]); ya = ytr[a]
                if cond == "SMOTE": A, ya = SMOTE(random_state=SEED).fit_resample(A, ya)
                t = time.perf_counter(); m = f().fit(A, ya); tr = time.perf_counter() - t
                p = m.predict(B); pr = m.predict_proba(B); Y = label_binarize(ytr[b], classes=list(range(6)))
                r = dict(Model=name, Condition=cond, Fold=k, Accuracy=accuracy_score(ytr[b], p), F1_weighted=f1_score(ytr[b], p, average="weighted"),
                         F1_macro=f1_score(ytr[b], p, average="macro"), MCC=matthews_corrcoef(ytr[b], p), Balanced_Acc=balanced_accuracy_score(ytr[b], p),
                         ROC_AUC_macro=roc_auc_score(ytr[b], pr, multi_class="ovr", average="macro"), PR_AUC_macro=average_precision_score(Y, pr, average="macro"), Train_s=tr)
                pd.DataFrame([r]).to_csv(OUT, mode="a", header=not OUT.exists(), index=False)
                print(f"[{time.strftime('%H:%M:%S')}] {name:14s} {cond:8s} fold{k} acc={r['Accuracy']:.4f} wF1={r['F1_weighted']:.4f}", flush=True)
    print("ALL DONE", flush=True)
