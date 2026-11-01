# ======================================
# TOPIC: REGRESSION METRICS AND CROSS-VALIDATION
# LEVEL: INTERMEDIATE
# ID: ml.evaluation.regression-metrics-cv
# ======================================

# INTRODUCTION
# One train/test split gives one noisy estimate. Cross-validation gives a more
# reliable estimate - and regression needs its own metrics.
#
# THEORY
# REGRESSION METRICS:
# - MAE = mean(|y - y_hat|): average error in original units; robust to outliers.
# - MSE = mean((y - y_hat)^2); RMSE = sqrt(MSE): punishes large errors more.
# - R^2: fraction of variance explained (1 perfect, 0 = predicting the mean,
#   can be negative).
# - MAPE: percentage error (undefined when y = 0).
# CROSS-VALIDATION:
# - K-FOLD: split data into k folds; train on k-1, validate on the remaining
#   one; repeat k times; report mean +/- std.
# - StratifiedKFold for classification, GroupKFold when samples are grouped,
#   TimeSeriesSplit for time-ordered data.
# - cross_val_score / cross_validate run this for you; put preprocessing inside
#   a Pipeline so it is re-fit on each training fold (no leakage).
# - Keep a final hold-out test set for the very end.
#
# REAL-WORLD ANALOGY
# Judging a chef with one dish is luck-dependent; asking them to cook five
# different dishes and averaging the scores is much fairer.
#
# SYNTAX:
#   cross_val_score(pipeline, X, y, cv=KFold(5, shuffle=True, random_state=0),
#                   scoring="neg_root_mean_squared_error")
#
# SMALL WORKING EXAMPLE:
import numpy as np
from sklearn.datasets import load_diabetes
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import KFold, cross_validate
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

y_true = np.array([100, 150, 200, 250])
y_pred = np.array([110, 140, 210, 400])
print("MAE", mean_absolute_error(y_true, y_pred),
      "| RMSE", round(np.sqrt(mean_squared_error(y_true, y_pred)), 1),
      "| R2", round(r2_score(y_true, y_pred), 3))
X, y = load_diabetes(return_X_y=True)
cv = KFold(n_splits=5, shuffle=True, random_state=0)
candidates = {
    "baseline (mean)": DummyRegressor(),
    "ridge": make_pipeline(StandardScaler(), Ridge(alpha=1.0)),
    "random forest": RandomForestRegressor(n_estimators=200, random_state=0, n_jobs=-1),
}
for name, model in candidates.items():
    result = cross_validate(model, X, y, cv=cv,
                            scoring=["neg_mean_absolute_error", "r2"])
    mae = -result["test_neg_mean_absolute_error"]
    r2 = result["test_r2"]
    print(f"{name:<16} MAE {mae.mean():6.1f} +/- {mae.std():4.1f} | R2 {r2.mean():.3f} +/- {r2.std():.3f}")

# EXPLANATION (LINE BY LINE):
# One large error (250 vs 400) -> RMSE (~76) is much larger than MAE (~45).
# KFold(5, shuffle=True)      -> 5 different train/validation splits.
# DummyRegressor              -> predicts the mean: the baseline to beat (R2 ~ 0).
# make_pipeline(StandardScaler(), Ridge()) -> scaling is re-fit inside each fold.
# cross_validate(..., scoring=[...]) -> several metrics at once; sklearn uses
#                                  "neg_" so that larger is always better.
# mean +/- std                -> report the variability across folds, not just the mean.
#
# COMMON MISTAKES:
# 1. Reporting a single split's score as the truth.
# 2. Scaling before cross-validation (leakage) instead of inside a Pipeline.
# 3. Forgetting that sklearn error scorers are negative.
# 4. Using plain KFold on time series or grouped data.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# For predictions [3, 5, 2, 8] and truth [2, 5, 4, 10], compute MAE, MSE, RMSE
# and R^2 by hand (comments) and with sklearn.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Compare 5-fold and 10-fold CV, with and without shuffling, for Ridge on the
# diabetes data. Then run 10 repetitions of 5-fold CV with different random
# states (RepeatedKFold) and plot the distribution of R^2 scores.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Implement k_fold_indices(n, k, shuffle, seed) yourself and a function
# my_cross_val(model_factory, X, y, k, metric) that clones a fresh model per
# fold. Verify it matches sklearn's KFold + cross_val_score exactly. Then use
# TimeSeriesSplit on a synthetic trend series and explain the fold structure.

# YOUR CODE:

