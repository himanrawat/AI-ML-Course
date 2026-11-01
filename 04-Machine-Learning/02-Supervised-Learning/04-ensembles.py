# ======================================
# TOPIC: ENSEMBLES: RANDOM FORESTS AND GRADIENT BOOSTING
# LEVEL: ADVANCED
# ID: ml.supervised.ensembles
# ======================================

# INTRODUCTION
# For tabular data (spreadsheets, databases), tree ensembles are usually the
# strongest models - often better than deep learning. They combine many weak
# trees into one strong predictor.
#
# THEORY
# - ENSEMBLE: combine several models so their errors cancel out.
# - BAGGING (Bootstrap AGGregatING): train models on random resamples of the
#   data and average them -> reduces variance.
#   RANDOM FOREST = bagged deep trees + a random subset of features at each
#   split (decorrelates the trees). Robust, little tuning.
# - BOOSTING: train trees SEQUENTIALLY, each fixing the errors of the previous
#   ones -> reduces bias. GRADIENT BOOSTING fits each new tree to the gradient
#   of the loss (residuals for MSE). Key hyperparameters: n_estimators,
#   learning_rate, max_depth. Popular libraries: XGBoost, LightGBM, CatBoost;
#   sklearn has HistGradientBoosting.
# - Feature importance: impurity-based (fast, biased) or PERMUTATION
#   importance (shuffle a feature and measure the drop; more reliable).
#
# REAL-WORLD ANALOGY
# Bagging: asking 100 people to guess the number of sweets in a jar and taking
# the average. Boosting: a team where each member specialises in fixing the
# previous member's mistakes.
#
# SYNTAX:
#   RandomForestClassifier(n_estimators=300, n_jobs=-1)
#   HistGradientBoostingClassifier(learning_rate=0.1, max_iter=200)
#   permutation_importance(model, X_test, y_test)
#
# SMALL WORKING EXAMPLE:
import numpy as np
from sklearn.datasets import make_classification
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.inspection import permutation_importance
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

X, y = make_classification(n_samples=2000, n_features=12, n_informative=5,
                           n_redundant=2, random_state=0)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)
models = {
    "single tree": DecisionTreeClassifier(random_state=0),
    "random forest": RandomForestClassifier(n_estimators=200, n_jobs=-1, random_state=0),
    "gradient boosting": HistGradientBoostingClassifier(random_state=0),
}
for name, model in models.items():
    model.fit(X_train, y_train)
    print(f"{name:<18} train {model.score(X_train, y_train):.3f}  test {model.score(X_test, y_test):.3f}")
forest = models["random forest"]
result = permutation_importance(forest, X_test, y_test, n_repeats=5, random_state=0)
top = np.argsort(result.importances_mean)[::-1][:5]
print("top features (permutation):", top.tolist())
print("importance values:", result.importances_mean[top].round(3).tolist())

# EXPLANATION (LINE BY LINE):
# make_classification             -> 12 features, only 5 truly informative.
# single tree                     -> train 1.000, weaker test: overfitting.
# random forest                   -> averaging 200 decorrelated trees: better test score.
# HistGradientBoosting            -> sequential boosting, typically top accuracy.
# permutation_importance          -> shuffles each feature on TEST data and
#                                    measures the accuracy drop.
# top features                    -> mostly the informative ones.
#
# COMMON MISTAKES:
# 1. Trusting impurity-based importances for features with many unique values.
# 2. Boosting with a high learning rate and many trees (overfits) - use
#    early stopping.
# 3. Expecting ensembles to extrapolate beyond the training range (trees can't).
# 4. Skipping a simple baseline (logistic regression) before ensembles.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Train a RandomForestClassifier on the breast cancer dataset with 10, 100 and
# 500 trees. Print test accuracy and training time for each.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Implement bagging by hand: train 50 decision trees on bootstrap samples
# (rng.choice with replacement) and predict by majority vote. Compare with a
# single tree and with RandomForestClassifier.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Implement gradient boosting for regression from scratch: start from the
# mean, repeatedly fit a shallow DecisionTreeRegressor to the residuals and add
# learning_rate * prediction. Plot train/validation MSE per iteration, add
# early stopping, and compare with HistGradientBoostingRegressor.

# YOUR CODE:

