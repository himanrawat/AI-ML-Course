# ======================================
# TOPIC: LINEAR REGRESSION
# LEVEL: INTERMEDIATE
# ID: ml.supervised.linear-regression
# ======================================

# INTRODUCTION
# Linear regression predicts a number as a weighted sum of features. It is
# simple, fast, interpretable - and the building block of neural networks.
# (Maths: 02-Mathematics vectors, matrix multiplication, gradient descent.)
#
# THEORY
# - Model: y_hat = w1*x1 + w2*x2 + ... + b = X @ w + b.
# - Loss: MEAN SQUARED ERROR = mean((y_hat - y)^2).
# - Solve by:
#   * Closed form (least squares / normal equation): w = (X^T X)^-1 X^T y
#     (computed stably with np.linalg.lstsq).
#   * Gradient descent: w -= lr * 2/n * X^T (X w - y).
# - Coefficients: each weight is the change in y for a one-unit change in that
#   feature, holding others fixed (only comparable if features are scaled).
# - Assumptions worth checking: roughly linear relationship, independent
#   errors, no extreme multicollinearity. Inspect RESIDUALS (y - y_hat).
# - R^2 = 1 - SS_residual / SS_total: fraction of variance explained.
#
# REAL-WORLD ANALOGY
# A taxi fare: base fare + rate per km + rate per minute. Given many past
# rides, linear regression recovers the base fare and the rates.
#
# SYNTAX:
#   model = LinearRegression().fit(X_train, y_train)
#   model.coef_, model.intercept_, model.score(X_test, y_test)
#
# SMALL WORKING EXAMPLE:
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split

rng = np.random.default_rng(5)
km = rng.uniform(1, 30, 300)
minutes = km * 2.5 + rng.normal(0, 8, 300).clip(-km * 2, None)
fare = 50 + 12 * km + 1.5 * minutes + rng.normal(0, 10, 300)
X = np.column_stack([km, minutes])
X_train, X_test, y_train, y_test = train_test_split(X, fare, random_state=0)
model = LinearRegression().fit(X_train, y_train)
print("sklearn: base", round(model.intercept_, 2), "rates", model.coef_.round(2))
X_b = np.column_stack([np.ones(len(X_train)), X_train])
w, *_ = np.linalg.lstsq(X_b, y_train, rcond=None)
print("closed form:", w.round(2))
predictions = model.predict(X_test)
residuals = y_test - predictions
print("test R^2:", round(r2_score(y_test, predictions), 4))
print("residual mean ~0:", round(residuals.mean(), 2), "| residual std:", round(residuals.std(), 2))
print("fare for 10 km, 25 min:", model.predict([[10, 25]]).round(1))

# EXPLANATION (LINE BY LINE):
# fare = 50 + 12*km + 1.5*minutes + noise -> the true (hidden) pricing rule.
# X = [km, minutes]                 -> two features.
# LinearRegression().fit            -> recovers base ~50 and rates ~12 and ~1.5.
# Closed form with a column of ones -> the same answer via least squares.
# r2_score                          -> close to 1: most variance explained.
# residuals                         -> centred at 0 with std ~ the noise level (10).
#
# COMMON MISTAKES:
# 1. Interpreting coefficients of unscaled or highly correlated features.
# 2. Extrapolating far outside the training range.
# 3. Ignoring residual patterns that reveal non-linearity.
# 4. Using R^2 on training data as proof of a good model.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Fit LinearRegression on sklearn's load_diabetes data (train/test split) and
# print the test R^2 and the three features with the largest absolute weights.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Implement linear regression with batch gradient descent (standardize X first),
# record the loss per step, and compare the final weights and test R^2 with
# sklearn on the taxi data.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Create data where y depends on x^2 and an interaction x1*x2. Show linear
# regression fails (residual plot), fix it with engineered features
# (PolynomialFeatures(interaction_only=...)), and demonstrate multicollinearity:
# add a near-duplicate feature and show how unstable the coefficients become
# across bootstrap resamples, then fix it with Ridge.

# YOUR CODE:

