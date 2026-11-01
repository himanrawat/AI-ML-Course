# ======================================
# TOPIC: EXPERIMENT TRACKING AND MODEL REGISTRY
# LEVEL: INTERMEDIATE
# ID: mlops.practices.experiment-tracking
# ======================================

# INTRODUCTION
# After 50 training runs, "which settings gave the best model, and which file
# is in production?" becomes impossible to answer from memory. Experiment
# tracking and a model registry make ML work reproducible and auditable.
#
# THEORY
# EXPERIMENT TRACKING - per run, record:
# - parameters (hyperparameters, data version, code commit), metrics (per
#   epoch and final), artifacts (model file, plots), environment, random seed.
# - Tools: MLflow (open source), Weights & Biases, Neptune; for LLM apps,
#   prompt/eval tracking tools play the same role.
# MODEL REGISTRY:
# - Named models with numbered VERSIONS and STAGES (candidate, staging,
#   production, archived), plus lineage: which run/data produced the version.
# - Promotion requires passing evaluation gates; rollback = re-promoting the
#   previous version.
# REPRODUCIBILITY: fixed seeds, pinned dependencies, versioned data (DVC or
# dataset hashes), code commit hash.
#
# REAL-WORLD ANALOGY
# A lab notebook (experiment tracking) plus a pharmacy's approved-medicine
# shelf (registry): every experiment is written down, and only tested,
# labelled batches reach the shelf.
#
# SYNTAX:
#   with tracker.run("name") as run: run.log_params(...); run.log_metric(...)
#
# SMALL WORKING EXAMPLE:
import hashlib
import json
import tempfile
import time
from contextlib import contextmanager
from pathlib import Path

import joblib
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score

ROOT = Path(tempfile.mkdtemp())

@contextmanager
def tracked_run(name, params):
    run_id = f"{name}-{int(time.time() * 1000) % 100000}"
    run = {"run_id": run_id, "params": params, "metrics": {}, "artifacts": []}
    yield run
    (ROOT / "runs").mkdir(exist_ok=True)
    (ROOT / "runs" / f"{run_id}.json").write_text(json.dumps(run, indent=1))

X, y = load_breast_cancer(return_X_y=True)
data_hash = hashlib.sha256(X.tobytes()).hexdigest()[:12]
for depth in (2, 5, None):
    params = {"max_depth": depth, "n_estimators": 100, "seed": 0, "data_version": data_hash}
    with tracked_run(f"rf-depth{depth}", params) as run:
        model = RandomForestClassifier(max_depth=depth, n_estimators=100, random_state=0)
        run["metrics"]["cv_f1"] = round(cross_val_score(model, X, y, cv=5, scoring="f1").mean(), 4)
        path = ROOT / f"{run['run_id']}.joblib"
        joblib.dump(model.fit(X, y), path)
        run["artifacts"].append(str(path))
runs = [json.loads(p.read_text()) for p in (ROOT / "runs").glob("*.json")]
best = max(runs, key=lambda r: r["metrics"]["cv_f1"])
for r in sorted(runs, key=lambda r: -r["metrics"]["cv_f1"]):
    print(f"{r['run_id']:<20} depth={str(r['params']['max_depth']):<5} cv_f1={r['metrics']['cv_f1']}")
registry = {"breast-cancer-rf": [{"version": 1, "run_id": best["run_id"], "stage": "production",
                                  "artifact": best["artifacts"][0]}]}
print("registered:", registry)
print("reloaded model works:", joblib.load(registry["breast-cancer-rf"][0]["artifact"]).predict(X[:3]).tolist())

# EXPLANATION (LINE BY LINE):
# tracked_run                -> context manager that saves params, metrics and artifact
#                               paths as one JSON record per run.
# data_hash                  -> a fingerprint of the training data (data versioning).
# Loop over max_depth        -> three runs with different hyperparameters.
# cross_val_score F1         -> the comparable metric; the model artifact is saved too.
# best run                   -> chosen from recorded metrics, not memory.
# registry                   -> model name -> versions with stage and lineage (run id).
# joblib.load                -> the registered artifact reproduces predictions.
#
# COMMON MISTAKES:
# 1. Not recording the data version or code commit.
# 2. Comparing runs evaluated on different splits.
# 3. Overwriting "model.pkl" with no version history.
# 4. Promoting models manually without an evaluation gate.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Add the Python and scikit-learn versions and the current Git commit (if any)
# to each run record, and print a comparison table of all runs.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Install MLflow in the course venv and re-implement the loop with
# mlflow.start_run, log_params, log_metric and sklearn.log_model. Open the
# MLflow UI (mlflow ui) and compare runs there.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Build a ModelRegistry class persisted to JSON with register(), promote()
# (only if the candidate beats production on a held-out test set), rollback(),
# and load(stage). Write pytest tests for promotion, refusal and rollback.

# YOUR CODE:

