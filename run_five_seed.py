"""Implementation and execution of Five-Seed Statistical Validation, Paired t-tests, and McNemar Tests."""
import time, numpy as np, pandas as pd
from scipy import stats
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, f1_score, matthews_corrcoef, balanced_accuracy_score, confusion_matrix
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, BaggingClassifier, ExtraTreesClassifier
from xgboost import XGBClassifier
from prep import load_clean, ROOT

OUT_SEEDS = ROOT / "results" / "tables" / "five_seed_results.csv"
OUT_TTESTS = ROOT / "results" / "tables" / "five_seed_paired_ttests.csv"

SEEDS = [42, 43, 44, 45, 46]

MODELS = {
    "Bagging": lambda s: BaggingClassifier(random_state=s, n_jobs=-1),
    "CART": lambda s: DecisionTreeClassifier(random_state=s),
    "Extra Trees": lambda s: ExtraTreesClassifier(n_estimators=100, random_state=s, n_jobs=-1),
    "Random Forest": lambda s: RandomForestClassifier(n_estimators=100, random_state=s, n_jobs=-1),
    "XGBoost": lambda s: XGBClassifier(random_state=s, n_jobs=-1, tree_method="hist"),
}

def eval_metrics(y_true, y_pred):
    return {
        "Accuracy": accuracy_score(y_true, y_pred),
        "F1_weighted": f1_score(y_true, y_pred, average="weighted"),
        "F1_macro": f1_score(y_true, y_pred, average="macro"),
        "MCC": matthews_corrcoef(y_true, y_pred),
        "Balanced_Acc": balanced_accuracy_score(y_true, y_pred),
    }

def exact_mcnemar(y_true, y_pred1, y_pred2):
    correct1 = (y_pred1 == y_true)
    correct2 = (y_pred2 == y_true)
    n01 = np.sum(~correct1 & correct2)
    n10 = np.sum(correct1 & ~correct2)
    n = n01 + n10
    if n == 0:
        return 1.0, n01, n10
    # Two-tailed exact binomial test
    p_val = stats.binomtest(min(n01, n10), n, 0.5, alternative="two-sided").pvalue
    return p_val, n01, n10

def run_five_seed_experiments():
    print("=== Running 5-Seed Statistical Experiments (Seeds 42, 43, 44, 45, 46) ===", flush=True)
    df = load_clean()
    y = LabelEncoder().fit_transform(df["label"])
    
    feat_11 = [c for c in df.columns if c not in ["label", "timestamp"]]
    feat_10 = [c for c in feat_11 if c != "tcp_time_delta"]
    
    feature_sets = {
        "With_tcp_time_delta": feat_11,
        "Without_tcp_time_delta": feat_10,
    }
    
    results = []
    seed_42_preds = {}
    
    for cond_name, feat_cols in feature_sets.items():
        print(f"\n--- Condition: {cond_name} ---", flush=True)
        X = df[feat_cols].values.astype(np.float64)
        
        for s in SEEDS:
            Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.20, random_state=s, stratify=y)
            sc = StandardScaler().fit(Xtr)
            Xtr_s, Xte_s = sc.transform(Xtr), sc.transform(Xte)
            
            for model_name, factory in MODELS.items():
                m = factory(s).fit(Xtr_s, ytr)
                preds = m.predict(Xte_s)
                
                if s == 42:
                    seed_42_preds[(cond_name, model_name)] = (yte, preds)
                    
                m_dict = eval_metrics(yte, preds)
                m_dict.update({
                    "Condition": cond_name,
                    "Model": model_name,
                    "Seed": s,
                })
                results.append(m_dict)
                print(f"Seed {s} | {cond_name:22s} | {model_name:14s} | Acc: {m_dict['Accuracy']:.4f} | wF1: {m_dict['F1_weighted']:.4f}", flush=True)
                
    df_res = pd.DataFrame(results)
    df_res.to_csv(OUT_SEEDS, index=False)
    print(f"\nSaved 5-Seed Results to {OUT_SEEDS}", flush=True)
    
    # Statistical analysis: paired t-tests
    print("\n=== Computing Paired t-tests across 5 Seeds ===", flush=True)
    ttest_rows = []
    model_list = list(MODELS.keys())
    
    for cond_name in feature_sets.keys():
        sub = df_res[df_res["Condition"] == cond_name]
        for i in range(len(model_list)):
            for j in range(i + 1, len(model_list)):
                m1, m2 = model_list[i], model_list[j]
                acc1 = sub[sub["Model"] == m1].sort_values("Seed")["Accuracy"].values
                acc2 = sub[sub["Model"] == m2].sort_values("Seed")["Accuracy"].values
                
                diff = (acc1 - acc2) * 100 # percentage points
                t_stat, p_val = stats.ttest_rel(acc1, acc2)
                
                # Also exact McNemar on seed 42
                y_true, p1 = seed_42_preds[(cond_name, m1)]
                _, p2 = seed_42_preds[(cond_name, m2)]
                p_mcnemar, n01, n10 = exact_mcnemar(y_true, p1, p2)
                
                ttest_rows.append({
                    "Condition": cond_name,
                    "Model_A": m1,
                    "Model_B": m2,
                    "Mean_Diff_pp": round(np.mean(diff), 3),
                    "Std_Diff_pp": round(np.std(diff), 3),
                    "Paired_t_stat": round(t_stat, 3),
                    "Paired_t_pval": p_val,
                    "McNemar_pval_seed42": p_mcnemar,
                    "McNemar_n01": n01,
                    "McNemar_n10": n10,
                })
                print(f"{cond_name:22s} | {m1:12s} vs {m2:12s} | Diff: {np.mean(diff):+6.2f} pp | t: {t_stat:6.2f} | p(t): {p_val:.4e} | p(McNemar): {p_mcnemar:.4e}", flush=True)
                
    df_ttests = pd.DataFrame(ttest_rows)
    df_ttests.to_csv(OUT_TTESTS, index=False)
    print(f"\nSaved Paired t-tests & McNemar Results to {OUT_TTESTS}", flush=True)

if __name__ == "__main__":
    run_five_seed_experiments()
