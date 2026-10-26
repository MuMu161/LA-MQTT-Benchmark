"""Implementation and execution of Feature Group Ablation and Leave-One-Feature-Out Ablation."""
import time, numpy as np, pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, f1_score, matthews_corrcoef, balanced_accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier
from prep import load_clean, ROOT, SEED

OUT_GRP = ROOT / "results" / "tables" / "feature_group_ablation.csv"
OUT_LOO = ROOT / "results" / "tables" / "leave_one_feature_out_ablation.csv"

TRANSPORT_FEATS = ["tcp_flags", "tcp_len"]
APPLICATION_FEATS = [
    "mqtt_conack_flags", "mqtt_conflag_cleansess", "mqtt_conflags",
    "mqtt_dupflag", "mqtt_hdrflags", "mqtt_kalive", "mqtt_msg", "mqtt_qos"
]
ALL_10_FEATS = TRANSPORT_FEATS + APPLICATION_FEATS
ALL_11_FEATS = ALL_10_FEATS + ["tcp_time_delta"]

def eval_subset(Xtr, Xte, ytr, yte, model_factory):
    sc = StandardScaler().fit(Xtr)
    m = model_factory().fit(sc.transform(Xtr), ytr)
    p = m.predict(sc.transform(Xte))
    return {
        "Accuracy": accuracy_score(yte, p),
        "F1_weighted": f1_score(yte, p, average="weighted"),
        "F1_macro": f1_score(yte, p, average="macro"),
        "MCC": matthews_corrcoef(yte, p),
    }

def run_group_ablation(df, y):
    print("=== Running Feature Group Ablation ===", flush=True)
    groups = {
        "Transport only (tcp_flags, tcp_len)": TRANSPORT_FEATS,
        "Application only (8 MQTT fields)": APPLICATION_FEATS,
        "All 10 (no tcp_time_delta)": ALL_10_FEATS,
        "All 11 (with tcp_time_delta)": ALL_11_FEATS,
    }
    
    rows = []
    for grp_name, feats in groups.items():
        X = df[feats].values.astype(np.float64)
        Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.20, random_state=SEED, stratify=y)
        
        # CART
        res_cart = eval_subset(Xtr, Xte, ytr, yte, lambda: DecisionTreeClassifier(random_state=SEED))
        res_cart.update({"Feature_Group": grp_name, "Model": "CART", "Num_Features": len(feats)})
        rows.append(res_cart)
        
        # Random Forest
        res_rf = eval_subset(Xtr, Xte, ytr, yte, lambda: RandomForestClassifier(n_estimators=100, random_state=SEED, n_jobs=-1))
        res_rf.update({"Feature_Group": grp_name, "Model": "Random Forest", "Num_Features": len(feats)})
        rows.append(res_rf)
        
        print(f"Group: {grp_name:35s} | CART Acc: {res_cart['Accuracy']:.4f} | RF Acc: {res_rf['Accuracy']:.4f}", flush=True)
        
    df_grp = pd.DataFrame(rows)
    df_grp.to_csv(OUT_GRP, index=False)
    print(f"Saved Feature Group Ablation to {OUT_GRP}\n", flush=True)

def run_leave_one_out_ablation(df, y):
    print("=== Running Leave-One-Feature-Out Ablation (from 10 sanitized features) ===", flush=True)
    rows = []
    
    # Baseline with all 10
    X_all = df[ALL_10_FEATS].values.astype(np.float64)
    Xtr, Xte, ytr, yte = train_test_split(X_all, y, test_size=0.20, random_state=SEED, stratify=y)
    
    cart_base = eval_subset(Xtr, Xte, ytr, yte, lambda: DecisionTreeClassifier(random_state=SEED))
    et_base = eval_subset(Xtr, Xte, ytr, yte, lambda: ExtraTreesClassifier(n_estimators=100, random_state=SEED, n_jobs=-1))
    
    rows.append({
        "Excluded_Feature": "None (All 10 Features)",
        "Model": "CART",
        "Accuracy": cart_base["Accuracy"],
        "F1_weighted": cart_base["F1_weighted"],
        "Delta_pp": 0.0,
    })
    rows.append({
        "Excluded_Feature": "None (All 10 Features)",
        "Model": "Extra Trees",
        "Accuracy": et_base["Accuracy"],
        "F1_weighted": et_base["F1_weighted"],
        "Delta_pp": 0.0,
    })
    print(f"Baseline All 10 | CART Acc: {cart_base['Accuracy']:.4f} | ET Acc: {et_base['Accuracy']:.4f}", flush=True)
    
    for feat in ALL_10_FEATS:
        sub_feats = [f for f in ALL_10_FEATS if f != feat]
        X = df[sub_feats].values.astype(np.float64)
        Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.20, random_state=SEED, stratify=y)
        
        cart_res = eval_subset(Xtr, Xte, ytr, yte, lambda: DecisionTreeClassifier(random_state=SEED))
        et_res = eval_subset(Xtr, Xte, ytr, yte, lambda: ExtraTreesClassifier(n_estimators=100, random_state=SEED, n_jobs=-1))
        
        delta_cart = (cart_res["Accuracy"] - cart_base["Accuracy"]) * 100
        delta_et = (et_res["Accuracy"] - et_base["Accuracy"]) * 100
        
        rows.append({
            "Excluded_Feature": feat,
            "Model": "CART",
            "Accuracy": cart_res["Accuracy"],
            "F1_weighted": cart_res["F1_weighted"],
            "Delta_pp": round(delta_cart, 2),
        })
        rows.append({
            "Excluded_Feature": feat,
            "Model": "Extra Trees",
            "Accuracy": et_res["Accuracy"],
            "F1_weighted": et_res["F1_weighted"],
            "Delta_pp": round(delta_et, 2),
        })
        print(f"Exclude: {feat:25s} | CART Acc: {cart_res['Accuracy']:.4f} ({delta_cart:+.2f}pp) | ET Acc: {et_res['Accuracy']:.4f} ({delta_et:+.2f}pp)", flush=True)
        
    df_loo = pd.DataFrame(rows)
    df_loo.to_csv(OUT_LOO, index=False)
    print(f"Saved Leave-One-Feature-Out Ablation to {OUT_LOO}\n", flush=True)

if __name__ == "__main__":
    df = load_clean()
    y = LabelEncoder().fit_transform(df["label"])
    run_group_ablation(df, y)
    run_leave_one_out_ablation(df, y)
