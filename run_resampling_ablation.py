"""Implementation and execution of Resampling & Class-Weight Ablation (Without tcp_time_delta)."""
import time, numpy as np, pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.utils.class_weight import compute_sample_weight
from sklearn.metrics import accuracy_score, f1_score, matthews_corrcoef, balanced_accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier
from xgboost import XGBClassifier
from imblearn.over_sampling import SMOTE
from prep import load_clean, ROOT, SEED

OUT = ROOT / "results" / "tables" / "resampling_ablation_results.csv"

FEATS = [
    "tcp_flags", "tcp_len", "mqtt_conack_flags", "mqtt_conflag_cleansess",
    "mqtt_conflags", "mqtt_dupflag", "mqtt_hdrflags", "mqtt_kalive", "mqtt_msg", "mqtt_qos"
]

def eval_model(m, Xte, yte):
    p = m.predict(Xte)
    return {
        "Accuracy": accuracy_score(yte, p),
        "F1_weighted": f1_score(yte, p, average="weighted"),
        "F1_macro": f1_score(yte, p, average="macro"),
        "MCC": matthews_corrcoef(yte, p),
        "Balanced_Acc": balanced_accuracy_score(yte, p),
    }

def run_resampling_ablation():
    print("=== Running Resampling and Cost-Sensitive Weighting Ablation (Without tcp_time_delta) ===", flush=True)
    df = load_clean()
    y = LabelEncoder().fit_transform(df["label"])
    X = df[FEATS].values.astype(np.float64)
    
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.20, random_state=SEED, stratify=y)
    sc = StandardScaler().fit(Xtr)
    Xtr_s, Xte_s = sc.transform(Xtr), sc.transform(Xte)
    
    # Pre-generate SMOTE data on train only
    print("Synthesizing SMOTE samples on training split...", flush=True)
    smote = SMOTE(random_state=SEED)
    Xtr_smote, ytr_smote = smote.fit_resample(Xtr_s, ytr)
    
    # Pre-generate sample weights for balanced
    sample_weights_tr = compute_sample_weight("balanced", ytr)
    
    models = {
        "CART": {
            "orig": lambda: DecisionTreeClassifier(random_state=SEED),
            "smote": lambda: DecisionTreeClassifier(random_state=SEED),
            "class_weight": lambda: DecisionTreeClassifier(random_state=SEED, class_weight="balanced"),
        },
        "Extra Trees": {
            "orig": lambda: ExtraTreesClassifier(n_estimators=100, random_state=SEED, n_jobs=-1),
            "smote": lambda: ExtraTreesClassifier(n_estimators=100, random_state=SEED, n_jobs=-1),
            "class_weight": lambda: ExtraTreesClassifier(n_estimators=100, random_state=SEED, n_jobs=-1, class_weight="balanced"),
        },
        "Random Forest": {
            "orig": lambda: RandomForestClassifier(n_estimators=100, random_state=SEED, n_jobs=-1),
            "smote": lambda: RandomForestClassifier(n_estimators=100, random_state=SEED, n_jobs=-1),
            "class_weight": lambda: RandomForestClassifier(n_estimators=100, random_state=SEED, n_jobs=-1, class_weight="balanced"),
        },
        "XGBoost": {
            "orig": lambda: XGBClassifier(random_state=SEED, n_jobs=-1, tree_method="hist"),
            "smote": lambda: XGBClassifier(random_state=SEED, n_jobs=-1, tree_method="hist"),
            "class_weight": lambda: XGBClassifier(random_state=SEED, n_jobs=-1, tree_method="hist"),
        },
    }
    
    records = []
    for model_name, configs in models.items():
        # 1. Original
        t0 = time.perf_counter()
        m_orig = configs["orig"]().fit(Xtr_s, ytr)
        t_orig = time.perf_counter() - t0
        r_orig = eval_model(m_orig, Xte_s, yte)
        r_orig.update({"Model": model_name, "Condition": "Original", "Fit_Time_s": round(t_orig, 2)})
        records.append(r_orig)
        print(f"{model_name:14s} | Original     | Acc: {r_orig['Accuracy']:.4f} | wF1: {r_orig['F1_weighted']:.4f} | mF1: {r_orig['F1_macro']:.4f}", flush=True)
        
        # 2. SMOTE
        t0 = time.perf_counter()
        m_smote = configs["smote"]().fit(Xtr_smote, ytr_smote)
        t_smote = time.perf_counter() - t0
        r_smote = eval_model(m_smote, Xte_s, yte)
        r_smote.update({"Model": model_name, "Condition": "SMOTE", "Fit_Time_s": round(t_smote, 2)})
        records.append(r_smote)
        print(f"{model_name:14s} | SMOTE        | Acc: {r_smote['Accuracy']:.4f} | wF1: {r_smote['F1_weighted']:.4f} | mF1: {r_smote['F1_macro']:.4f}", flush=True)
        
        # 3. Class Weights
        t0 = time.perf_counter()
        if model_name == "XGBoost":
            m_cw = configs["class_weight"]().fit(Xtr_s, ytr, sample_weight=sample_weights_tr)
        else:
            m_cw = configs["class_weight"]().fit(Xtr_s, ytr)
        t_cw = time.perf_counter() - t0
        r_cw = eval_model(m_cw, Xte_s, yte)
        r_cw.update({"Model": model_name, "Condition": "Class_Weights", "Fit_Time_s": round(t_cw, 2)})
        records.append(r_cw)
        print(f"{model_name:14s} | Class_Weights| Acc: {r_cw['Accuracy']:.4f} | wF1: {r_cw['F1_weighted']:.4f} | mF1: {r_cw['F1_macro']:.4f}", flush=True)
        
    df_res = pd.DataFrame(records)
    df_res.to_csv(OUT, index=False)
    print(f"\nSaved Resampling Ablation Results to {OUT}", flush=True)

if __name__ == "__main__":
    run_resampling_ablation()
