"""Implementation and execution of Protocol P2 (Deduplicated split) and Protocol P3 (Pattern-grouped 5-fold CV)."""
import time, numpy as np, pandas as pd
from sklearn.model_selection import train_test_split, GroupKFold
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, f1_score, matthews_corrcoef, balanced_accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, BaggingClassifier, ExtraTreesClassifier
from xgboost import XGBClassifier
from prep import load_clean, ROOT, SEED

OUT = ROOT / "results" / "tables" / "protocol_p2_p3_results.csv"

MODELS = {
    "CART": lambda: DecisionTreeClassifier(random_state=SEED),
    "Extra Trees": lambda: ExtraTreesClassifier(n_estimators=100, random_state=SEED, n_jobs=-1),
    "Bagging": lambda: BaggingClassifier(random_state=SEED, n_jobs=-1),
    "Random Forest": lambda: RandomForestClassifier(n_estimators=100, random_state=SEED, n_jobs=-1),
    "XGBoost": lambda: XGBClassifier(random_state=SEED, n_jobs=-1, tree_method="hist"),
}

def evaluate_predictions(y_true, y_pred):
    return {
        "Accuracy": accuracy_score(y_true, y_pred),
        "F1_weighted": f1_score(y_true, y_pred, average="weighted"),
        "F1_macro": f1_score(y_true, y_pred, average="macro"),
        "MCC": matthews_corrcoef(y_true, y_pred),
        "Balanced_Acc": balanced_accuracy_score(y_true, y_pred),
    }

def run_p2():
    print("=== Running Protocol P2: Deduplicated Split (Without tcp_time_delta) ===", flush=True)
    df = load_clean()
    # Exclude time columns
    feat_cols = [c for c in df.columns if c not in ["label", "timestamp", "tcp_time_delta"]]
    
    # Deduplicate based on unique (features, label) tuples
    df_dedup = df.drop_duplicates(subset=[*feat_cols, "label"]).copy().reset_index(drop=True)
    print(f"Total unique (feature pattern, label) rows: {len(df_dedup)} (from original {len(df)})", flush=True)
    
    y = LabelEncoder().fit_transform(df_dedup["label"])
    X = df_dedup[feat_cols].values.astype(np.float64)
    
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.20, random_state=SEED, stratify=y)
    sc = StandardScaler().fit(Xtr)
    Xtr_s, Xte_s = sc.transform(Xtr), sc.transform(Xte)
    
    rows = []
    for name, factory in MODELS.items():
        t0 = time.perf_counter()
        m = factory().fit(Xtr_s, ytr)
        t_fit = time.perf_counter() - t0
        preds = m.predict(Xte_s)
        metrics = evaluate_predictions(yte, preds)
        metrics.update({
            "Protocol": "P2_Deduplicated_Split",
            "Model": name,
            "Train_Samples": len(Xtr),
            "Test_Samples": len(Xte),
            "Train_Time_s": round(t_fit, 3),
        })
        rows.append(metrics)
        print(f"P2 | {name:14s} | Acc: {metrics['Accuracy']:.4f} | wF1: {metrics['F1_weighted']:.4f} | Time: {t_fit:.2f}s", flush=True)
    return rows

def run_p3():
    print("\n=== Running Protocol P3: Pattern-Grouped 5-Fold Cross-Validation (Without tcp_time_delta) ===", flush=True)
    df = load_clean()
    feat_cols = [c for c in df.columns if c not in ["label", "timestamp", "tcp_time_delta"]]
    
    # Construct distinct group IDs based purely on unique feature patterns
    df["pattern_group"] = df.groupby(feat_cols).ngroup()
    n_groups = df["pattern_group"].nunique()
    print(f"Total distinct feature patterns (groups): {n_groups} across {len(df)} total rows", flush=True)
    
    y = LabelEncoder().fit_transform(df["label"])
    X = df[feat_cols].values.astype(np.float64)
    groups = df["pattern_group"].values
    
    gkf = GroupKFold(n_splits=5)
    
    summary_rows = []
    for name, factory in MODELS.items():
        fold_accs, fold_wf1, fold_mf1, fold_mcc, fold_bacc = [], [], [], [], []
        t0_model = time.perf_counter()
        
        for fold, (train_idx, test_idx) in enumerate(gkf.split(X, y, groups=groups), 1):
            Xtr, Xte = X[train_idx], X[test_idx]
            ytr, yte = y[train_idx], y[test_idx]
            
            sc = StandardScaler().fit(Xtr)
            Xtr_s, Xte_s = sc.transform(Xtr), sc.transform(Xte)
            
            m = factory().fit(Xtr_s, ytr)
            preds = m.predict(Xte_s)
            
            m_dict = evaluate_predictions(yte, preds)
            fold_accs.append(m_dict["Accuracy"])
            fold_wf1.append(m_dict["F1_weighted"])
            fold_mf1.append(m_dict["F1_macro"])
            fold_mcc.append(m_dict["MCC"])
            fold_bacc.append(m_dict["Balanced_Acc"])
            print(f"  P3 | {name:14s} Fold {fold}/5: Acc={m_dict['Accuracy']:.4f}, wF1={m_dict['F1_weighted']:.4f}", flush=True)
            
        t_total = time.perf_counter() - t0_model
        res = {
            "Protocol": "P3_Grouped_5Fold_CV",
            "Model": name,
            "Accuracy": np.mean(fold_accs),
            "Accuracy_std": np.std(fold_accs),
            "F1_weighted": np.mean(fold_wf1),
            "F1_macro": np.mean(fold_mf1),
            "MCC": np.mean(fold_mcc),
            "Balanced_Acc": np.mean(fold_bacc),
            "Train_Time_s": round(t_total, 3),
        }
        summary_rows.append(res)
        print(f"P3 Summary | {name:14s} | Acc: {res['Accuracy']:.4f} +/- {res['Accuracy_std']:.4f} | wF1: {res['F1_weighted']:.4f}", flush=True)
    return summary_rows

if __name__ == "__main__":
    p2_res = run_p2()
    p3_res = run_p3()
    df_all = pd.DataFrame(p2_res + p3_res)
    df_all.to_csv(OUT, index=False)
    print(f"\nSaved P2 and P3 results to {OUT}", flush=True)
