# ======================================
# TOPIC: HYPERPARAMETER TUNING
# LEVEL: ADVANCED
# ID: ml.features.hyperparameter-tuning
# ======================================

# INTRODUCTION
# Hyperparameters (tree depth, regularization strength, learning rate) are set
# before training and can change results a lot. Tuning them systematically,
# without cheating on the test set, is a core ML skill.
#
# THEORY
# - PARAMETERS are learned (weights); HYPERPARAMETERS are chosen (alpha, depth).
# - GRID SEARCH tries every combination (expensive, exhaustive).
# - RANDOM SEARCH samples combinations - usually finds good settings faster,
#   especially when only a few hyperparameters matter.
# - Bayesian optimisation (Optuna) learns which regions look promising.
# - Use cross-validation INSIDE the search, then evaluate the best model ONCE
#   on a held-out test set.
# - With pipelines, address steps by name: "clf__C", "pre__num__impute__strategy".
# - Search on a log scale for scale-type values (C, alpha, learning rate).
# - NESTED cross-validation gives an unbiased estimate of the whole tuning
#   procedure.
#
# REAL-WORLD ANALOGY
# Tuning a guitar: you adjust each string's tension (hyperparameter), listening
# to the result (validation score), before the concert (test).
#
# SYNTAX:
#   GridSearchCV(pipeline, {"clf__C": [0.1, 1, 10]}, cv=5, scoring="f1")
#   RandomizedSearchCV(pipeline, {"clf__C": loguniform(1e-3, 1e2)}, n_iter=30)
#
# SMALL WORKING EXAMPLE:
from scipy.stats import loguniform, randint
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

X, y = load_breast_cancer(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, random_state=0)
pipe = Pipeline([("scale", StandardScaler()), ("clf", LogisticRegression(max_iter=5000))])
grid = GridSearchCV(pipe, {"clf__C": [0.001, 0.01, 0.1, 1, 10, 100]}, cv=5, scoring="f1")
grid.fit(X_train, y_train)
print("grid best:", grid.best_params_, "cv f1:", round(grid.best_score_, 4))
for c, score in zip(grid.cv_results_["param_clf__C"], grid.cv_results_["mean_test_score"]):
    print(f"  C={c:<6} f1={score:.4f}")
search = RandomizedSearchCV(
    RandomForestClassifier(random_state=0, n_jobs=-1),
    {"n_estimators": randint(50, 400), "max_depth": [3, 5, 8, None],
     "min_samples_leaf": randint(1, 10), "max_features": loguniform(0.1, 1.0)},
    n_iter=15, cv=5, scoring="f1", random_state=0,
)
search.fit(X_train, y_train)
print("random best:", {k: (round(v, 3) if isinstance(v, float) else v) for k, v in search.best_params_.items()})
for name, model in [("logistic", grid.best_estimator_), ("forest", search.best_estimator_)]:
    print(f"{name} TEST accuracy (evaluated once): {model.score(X_test, y_test):.4f}")

# EXPLANATION (LINE BY LINE):
# Pipeline with names "scale" and "clf" -> parameters addressed as "clf__C".
# GridSearchCV over C on a log scale     -> 6 values x 5 folds = 30 fits.
# best_params_ / best_score_             -> chosen by cross-validated F1 on TRAIN data.
# cv_results_                            -> scores for every candidate (inspect them!).
# RandomizedSearchCV with distributions  -> 15 random combinations instead of a full grid.
# loguniform(0.1, 1.0)                   -> sample fractions on a log scale.
# best_estimator_                        -> refit on all training data; tested once at the end.
#
# COMMON MISTAKES:
# 1. Tuning on the test set (scores become optimistic).
# 2. Linear grids for scale parameters (use log scales).
# 3. Huge grids that take hours when random search would do.
# 4. Reporting the CV score of the best config as the final performance
#    (it is optimistically biased - use a test set or nested CV).

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Use GridSearchCV to tune n_neighbors (1..30) for KNeighborsClassifier on
# Iris (inside a pipeline with scaling). Print the best k and its CV accuracy.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Tune HistGradientBoostingClassifier (learning_rate, max_depth, max_iter,
# l2_regularization) with RandomizedSearchCV on the breast cancer data. Plot
# the CV score of every tried candidate against learning_rate.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Implement nested cross-validation (outer 5-fold for evaluation, inner
# GridSearchCV for tuning) by hand with a loop, and compare its score with
# the non-nested best_score_. Explain the difference in a comment.

# YOUR CODE:

