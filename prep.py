"""Shared, paper-aligned preprocessing for MQTTEEB-D (Allaga et al., Ad Hoc Networks 181, 2026).
Every experiment imports this so all models see the identical split (seed 42)."""
import numpy as np, pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder

ROOT = Path(__file__).resolve().parent
_CANDIDATES = [ROOT / "data" / "MQTTEEB-D_Final_Dataset" / "Preprocessed_Data" / "MQTTEEB-D_cleaned_data.csv",
               ROOT / "data" / "MQTTEEB-D_cleaned_data.csv"]
CSV = next((p for p in _CANDIDATES if p.exists()), _CANDIDATES[0])
HEX_COLS = ["tcp_flags", "mqtt_conack_flags", "mqtt_conflags", "mqtt_hdrflags"]
CLASS_NAMES = ["bruteforce", "dos", "flood", "legitimate", "malformed", "slowite"]
SEED = 42

def _hex_to_int(v):
    if pd.isna(v): return np.nan
    if isinstance(v, (int, np.integer, float, np.floating)): return int(v)
    v = str(v).strip()
    try: return int(v, 16)
    except ValueError:
        try: return int(float(v))
        except ValueError: return np.nan

def load_clean():
    """Drop 246 unlabeled rows, hex->int on 4 protocol fields. Keeps timestamp (needed for audits)."""
    df = pd.read_csv(CSV, low_memory=False).dropna(subset=["label"]).copy()
    for c in HEX_COLS: df[c] = df[c].apply(_hex_to_int)
    return df.reset_index(drop=True)

def get_split(drop_cols=("timestamp",), binary=False, smote=True):
    """Returns dict with scaled train/test (+ SMOTE train). Scaler/SMOTE fit on TRAIN only."""
    df = load_clean()
    le = LabelEncoder(); y = le.fit_transform(df["label"])
    assert list(le.classes_) == CLASS_NAMES
    if binary: y = (df["label"] == "legitimate").astype(int).values  # 1 = legitimate (minority, paper's positive class)
    X = df.drop(columns=["label", *drop_cols])
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.20, random_state=SEED, stratify=y)
    sc = StandardScaler().fit(Xtr)
    out = dict(Xtr=sc.transform(Xtr), Xte=sc.transform(Xte), ytr=ytr, yte=yte, cols=list(X.columns), scaler=sc)
    if smote:
        from imblearn.over_sampling import SMOTE
        out["Xtr_s"], out["ytr_s"] = SMOTE(random_state=SEED).fit_resample(out["Xtr"], ytr)
    return out

if __name__ == "__main__":
    d = get_split()
    print("train", d["Xtr"].shape, "test", d["Xte"].shape, "SMOTE train", d["Xtr_s"].shape)
    print("features:", d["cols"])

LOOP_SIZES = [137319, 42470, 21501, 21523]  # rows per raw capture loop (before dropping unlabeled rows)

def load_clean_with_loop():
    """Same cleaning as load_clean(), plus a 'loop' column (1-4) recovered from original row order."""
    df = pd.read_csv(CSV, low_memory=False)
    df["loop"] = np.repeat(np.arange(1, 5), LOOP_SIZES)
    df = df.dropna(subset=["label"]).copy()
    for c in HEX_COLS: df[c] = df[c].apply(_hex_to_int)
    return df.reset_index(drop=True)
