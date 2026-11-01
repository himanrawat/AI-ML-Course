# ======================================
# TOPIC: WHAT IS MACHINE LEARNING
# LEVEL: BEGINNER
# ID: ml.fundamentals.what-is-ml
# ======================================

# INTRODUCTION
# Traditional programming: you write rules, the computer applies them.
# Machine learning: you give examples, the computer LEARNS the rules.
#
# THEORY
# - A MODEL is a function with adjustable PARAMETERS, f(x; w) -> y.
#   TRAINING finds parameters that make predictions match examples.
# - Vocabulary: FEATURES (inputs X, shape (n_samples, n_features)),
#   TARGET/LABEL (y), SAMPLE (one row), PREDICTION (y_hat), LOSS (how wrong).
# - Types of learning:
#   SUPERVISED - labelled examples: REGRESSION (predict a number: price),
#     CLASSIFICATION (predict a category: spam/ham).
#   UNSUPERVISED - no labels: clustering, dimensionality reduction.
#   REINFORCEMENT - learn actions from rewards.
#   SELF-SUPERVISED - labels come from the data itself (next-token prediction
#     in LLMs).
# - The goal is GENERALISATION: good predictions on NEW data, not memorising
#   the training set.
# - scikit-learn's universal API: model.fit(X, y), model.predict(X),
#   model.score(X, y).
#
# REAL-WORLD ANALOGY
# Learning to recognise ripe mangoes: nobody hands you a rulebook; you see
# many mangoes labelled ripe/unripe and gradually learn what matters.
#
# SYNTAX:
#   model = SomeModel(hyperparameters)
#   model.fit(X_train, y_train)
#   predictions = model.predict(X_new)
#
# SMALL WORKING EXAMPLE:
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeClassifier

def rule_based_spam(text):
    return "free" in text or "win" in text

print("rule-based:", rule_based_spam("win a free trip"))
area = np.array([[50], [70], [90], [110], [130]])
price = np.array([150, 205, 260, 310, 370])
regressor = LinearRegression().fit(area, price)
print(f"learned: price = {regressor.coef_[0]:.2f} * area + {regressor.intercept_:.2f}")
print("predict 100 m2:", regressor.predict([[100]]).round(1))
X = np.array([[22, 0], [25, 1], [47, 1], [52, 0], [46, 1], [56, 1], [23, 0], [60, 1]])
bought = np.array([0, 0, 1, 0, 1, 1, 0, 1])
classifier = DecisionTreeClassifier(max_depth=2, random_state=0).fit(X, bought)
print("classify [40, 1] and [30, 0]:", classifier.predict([[40, 1], [30, 0]]))
print("training accuracy:", classifier.score(X, bought))

# EXPLANATION (LINE BY LINE):
# rule_based_spam               -> traditional programming: hand-written rules.
# area (5, 1) and price (5,)    -> X must be 2D (samples x features), y is 1D.
# LinearRegression().fit(...)   -> learns a slope and intercept from examples.
# regressor.predict([[100]])    -> generalise to an unseen house size.
# X = [age, visited_before]     -> two features; bought is the class label.
# DecisionTreeClassifier(max_depth=2) -> learns simple if/else rules from data.
# classifier.score              -> accuracy on the TRAINING data (optimistic!).
#
# COMMON MISTAKES:
# 1. Passing 1D X to scikit-learn (use X.reshape(-1, 1) for one feature).
# 2. Judging a model by training accuracy.
# 3. Using ML where a simple rule works perfectly well.
# 4. Confusing parameters (learned) with hyperparameters (you choose).

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# For each problem, write in comments whether it is regression,
# classification, clustering or not ML at all, and what X and y would be:
# house prices, grouping customers, detecting fraud, sorting names, sentiment.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Create synthetic data y = 4x - 2 + noise. Fit LinearRegression, print the
# learned parameters, and plot the data with the fitted line. Repeat with
# 5, 50 and 500 samples and comment on parameter accuracy.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Write your own class SimpleLinearRegression with fit/predict that follows
# the scikit-learn API (learned attributes end with "_"), using the closed-form
# least squares solution np.linalg.lstsq. Verify it matches sklearn on
# multi-feature data and that it works inside sklearn.model_selection.cross_val_score
# (inherit from BaseEstimator and RegressorMixin).

# YOUR CODE:

