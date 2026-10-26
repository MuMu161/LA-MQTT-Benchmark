"""Deep-learning benchmark (ANN, 1D-CNN, SimpleRNN, LSTM) on the ORIGINAL imbalanced data (paper Table 7 setting).
Per-epoch train/val accuracy+loss are logged. Run with all features and without tcp_time_delta (timestamp duplicate).
Architectures are fixed and small (the paper does not publish its architectures)."""
import os, time, numpy as np, pandas as pd
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
import tensorflow as tf
from tensorflow.keras import layers, models
from sklearn.metrics import (accuracy_score, precision_score, recall_score, f1_score, matthews_corrcoef,
                             roc_auc_score, average_precision_score)
from sklearn.preprocessing import label_binarize
from prep import get_split, ROOT, SEED
EPOCHS, BATCH = 12, 512
HIST, RES = ROOT / "results/tables/dl_epoch_history.csv", ROOT / "results/tables/dl_results.csv"
def build(kind, n):
    m = models.Sequential([layers.Input((n,))] if kind == "ANN" else [layers.Input((n,)), layers.Reshape((n, 1))])
    if kind == "ANN": m.add(layers.Dense(128, activation="relu")); m.add(layers.Dropout(.2)); m.add(layers.Dense(64, activation="relu"))
    elif kind == "1D-CNN": m.add(layers.Conv1D(64, 3, activation="relu")); m.add(layers.Conv1D(64, 3, activation="relu")); m.add(layers.GlobalMaxPooling1D()); m.add(layers.Dense(64, activation="relu"))
    elif kind == "SimpleRNN": m.add(layers.SimpleRNN(64))
    elif kind == "LSTM": m.add(layers.LSTM(64))
    m.add(layers.Dense(6, activation="softmax"))
    m.compile(optimizer=tf.keras.optimizers.Adam(1e-3), loss="sparse_categorical_crossentropy", metrics=["accuracy"]); return m
if __name__ == "__main__":
    done = set(map(tuple, pd.read_csv(RES)[["Features", "Model"]].values)) if RES.exists() else set()
    for fs, drop in [("All 11 features", ("timestamp",)), ("Without tcp_time_delta", ("timestamp", "tcp_time_delta"))]:
        d = get_split(drop_cols=drop, smote=False); Xtr, ytr, Xte, yte = d["Xtr"].astype("float32"), d["ytr"], d["Xte"].astype("float32"), d["yte"]
        for kind in ["ANN", "1D-CNN", "SimpleRNN", "LSTM"]:
            if (fs, kind) in done: continue
            tf.keras.utils.set_random_seed(SEED); m = build(kind, Xtr.shape[1])
            t = time.perf_counter(); h = m.fit(Xtr, ytr, epochs=EPOCHS, batch_size=BATCH, validation_split=.1, verbose=0).history; tr = time.perf_counter() - t
            ep = pd.DataFrame(dict(Features=fs, Model=kind, Epoch=np.arange(1, EPOCHS + 1), Train_Acc=h["accuracy"], Val_Acc=h["val_accuracy"], Train_Loss=h["loss"], Val_Loss=h["val_loss"]))
            ep.to_csv(HIST, mode="a", header=not HIST.exists(), index=False)
            t = time.perf_counter(); pr = m.predict(Xte, batch_size=2048, verbose=0); te = time.perf_counter() - t; p = pr.argmax(1)
            Y = label_binarize(yte, classes=list(range(6)))
            acc = accuracy_score(yte, p); f1 = f1_score(yte, p, average="weighted", zero_division=0)
            r = dict(Features=fs, Model=kind, Accuracy=acc, Precision_w=precision_score(yte, p, average="weighted", zero_division=0), Recall_w=recall_score(yte, p, average="weighted", zero_division=0),
                     F1_weighted=f1, MCC=matthews_corrcoef(yte, p), ROC_AUC_macro=roc_auc_score(yte, pr, multi_class="ovr", average="macro"),
                     PR_AUC_macro=average_precision_score(Y, pr, average="macro"), Train_s=tr, Infer_s=te, Epochs=EPOCHS, PES=((acc + f1) / 2) / np.log(1 + te))
            pd.DataFrame([r]).to_csv(RES, mode="a", header=not RES.exists(), index=False)
            np.savez_compressed(ROOT / f"results/preds/DL_{kind}_{fs.split()[0]}.npz", y_true=yte, y_pred=p, proba=pr.astype("float32"))
            print(f"[{time.strftime('%H:%M:%S')}] {fs:24s} {kind:10s} acc={acc:.4f} wF1={f1:.4f} MCC={r['MCC']:.4f} train={tr:.0f}s", flush=True)
    print("ALL DONE", flush=True)
