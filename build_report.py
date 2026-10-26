"""Builds paper-vs-ours comparison tables from the corrected result CSVs."""
import pandas as pd, numpy as np
from prep import ROOT
T = ROOT / "results" / "tables"
# Values transcribed from the base paper (Allaga et al., 2026): Table 6 (imbalanced multi-class), Table 9 (SMOTE multi-class)
paper_orig = {"Bagging": (.99, .9852, .9989, .9951), "CART": (.98, .9831, .9888, .9640), "Extra Trees": (.97, .9726, .9979, .9896),
              "OvR Random Forest": (.97, .9681, .9981, .9905), "Random Forest": (.96, .9580, .9974, .9870),
              "Gradient Boosting (tuned)": (.86, .9013, .9866, .9180), "XGBoost": (.85, .8849, .9862, .9025),
              "CatBoost": (.84, .8794, .9843, .8970), "LightGBM": (.85, .8471, .9834, .8909)}
paper_smote = {"Bagging": .99, "CART": .99, "Extra Trees": .99, "OvR Random Forest": .99, "Random Forest": .99, "K-NN (k=5)": .98,
               "Gradient Boosting (tuned)": .93, "XGBoost": .89, "LightGBM": .89}
m = pd.read_csv(T / "multiclass_corrected.csv")
rows = []
for name in paper_orig:
    o = m[(m.Model == name) & (m.Dataset == "Original")]; s = m[(m.Model == name) & (m.Dataset == "SMOTE")]
    r = dict(Model=name, Paper_F1_orig=paper_orig[name][0], Ours_F1_orig=o.F1_weighted.iloc[0] if len(o) else np.nan,
             Paper_MCC_orig=paper_orig[name][1], Ours_MCC_orig=o.MCC.iloc[0] if len(o) else np.nan,
             Paper_ROC_orig=paper_orig[name][2], Ours_ROC_orig=o.ROC_AUC_macro.iloc[0] if len(o) else np.nan,
             Paper_F1_SMOTE=paper_smote.get(name, np.nan), Ours_F1_SMOTE=s.F1_weighted.iloc[0] if len(s) else np.nan)
    rows.append(r)
cmp = pd.DataFrame(rows); cmp["Gap_F1_orig_pp"] = (cmp.Ours_F1_orig - cmp.Paper_F1_orig) * 100
cmp["Gap_F1_SMOTE_pp"] = (cmp.Ours_F1_SMOTE - cmp.Paper_F1_SMOTE) * 100
cmp.round(4).to_csv(T / "PAPER_VS_OURS_multiclass.csv", index=False)
pd.set_option("display.width", 220); print(cmp.round(3).to_string(index=False))
