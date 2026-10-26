# MQTTEEB-D Project (merged)

Replication of "MQTTEEB-D: A high-fidelity benchmark for real-time MQTT anomaly detection using machine learning techniques"
(Allaga et al., Ad Hoc Networks 181, 2026) with a leakage audit.

## Start here
Open `MQTTEEB-D_Final.ipynb` and click Kernel > Restart & Run All. It loads saved results in seconds.
To retrain everything, set `RUN_HEAVY = True` in the second cell (several hours).

## Folder map
| Path | What it is |
|---|---|
| `MQTTEEB-D_Final.ipynb` | The single main notebook (all sections, tables, figures) |
| `prep.py` | Shared preprocessing (same split for every experiment) |
| `run_*.py` | Experiments: multiclass, binary, cv, ablation, dl (dl_long = final deep-learning run) |
| `make_*.py`, `build_*.py` | Figure and table builders |
| `results/tables`, `results/figures` | Corrected results used in the paper |
| `data/` | Your original dataset folder (unchanged) |
| `archive_old_project/` | Your original notebooks and old results, kept untouched for reference. Do not cite their tables. |

## Notes
* Gradient Boosting (tuned) is not retrained here; use the validated values from the old notebook (0.9801 original, 0.9289 SMOTE) and label them as such.
* PES uses the paper's Table 3 scale (fractions).
