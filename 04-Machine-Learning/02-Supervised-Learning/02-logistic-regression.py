# ======================================
# TOPIC: LOGISTIC REGRESSION
# LEVEL: INTERMEDIATE
# ID: ml.supervised.logistic-regression
# ======================================

# INTRODUCTION
# Logistic regression is the standard first model for classification: spam
# or not, churn or not. It outputs probabilities and is the same structure
# as the final layer of most neural network classifiers.
#
# THEORY
# - Compute a score z = X @ w + b, then squash it into a probability with the
#   SIGMOID: p = 1 / (1 + e^(-z)).
# - Predict class 1 if p >= threshold (default 0.5). The threshold is a
#   business decision (trade precision vs recall).
# - Loss: BINARY CROSS-ENTROPY (log loss) = -mean(y log p + (1 - y) log(1 - p)).
#   It punishes confident wrong answers heavily.
# - Coefficients act on the LOG-ODDS: log(p / (1 - p)) = z.
#   exp(w_i) is the odds multiplier for a one-unit increase in feature i.
# - Multiclass: softmax regression (multinomial) generalises to K classes.
# - Regularization is built in (sklearn's C = 1 / alpha: smaller C = stronger).
#
# REAL-WORLD ANALOGY
# A bank's credit check: points are added for income, deducted for missed
# payments, and the total score is converted into a probability of default.
#
# SYNTAX:
#   clf = LogisticRegression(C=1.0).fit(X, y)
#   clf.predict_proba(X)[:, 1]
#
# SMALL WORKING EXAMPLE:
import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import log_loss
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

print("sigmoid of -4, 0, 4:", sigmoid(np.array([-4, 0, 4])).round(3))
data = load_breast_cancer()
X_train, X_test, y_train, y_test = train_test_split(
    data.data, data.target, test_size=0.25, stratify=data.target, random_state=0)
clf = make_pipeline(StandardScaler(), LogisticRegression(C=1.0, max_iter=1000)).fit(X_train, y_train)
proba = clf.predict_proba(X_test)[:, 1]
print("test accuracy:", round(clf.score(X_test, y_test), 3), "| log loss:", round(log_loss(y_test, proba), 3))
for threshold in (0.3, 0.5, 0.9):
    predicted = (proba >= threshold).astype(int)
    print(f"threshold {threshold}: predicted positives = {predicted.sum()}")
weights = clf[-1].coef_[0]
top = np.argsort(np.abs(weights))[::-1][:3]
for i in top:
    print(f"{data.feature_names[i]:<22} odds x{np.exp(weights[i]):.2f} per std")
print("log loss confident & wrong:", round(log_loss([1], [[0.99, 0.01]], labels=[0, 1]), 2))

# EXPLANATION (LINE BY LINE):
# sigmoid maps any number into (0, 1): -4 -> 0.018, 0 -> 0.5, 4 -> 0.982.
# load_breast_cancer           -> binary classification dataset (malignant/benign).
# StandardScaler + LogisticRegression in a pipeline -> scaling fit on train only.
# predict_proba(...)[:, 1]     -> probability of class 1 for each test sample.
# Different thresholds         -> more or fewer positive predictions.
# np.exp(weight)               -> odds multiplier for +1 standard deviation.
# log_loss for a 99%-confident wrong answer -> about 4.6: heavily penalised.
#
# COMMON MISTAKES:
# 1. Treating it as regression because of the name.
# 2. Always using threshold 0.5 regardless of costs.
# 3. Not scaling features (slow convergence, uninterpretable weights).
# 4. Reading coefficients as probabilities rather than log-odds effects.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Train logistic regression on a 2-feature synthetic dataset
# (sklearn.datasets.make_classification) and print the probability for
# three new points. Plot the data and the decision boundary line.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Implement logistic regression from scratch with gradient descent on binary
# cross-entropy (gradient X.T @ (p - y) / n). Compare accuracy and weights with
# sklearn (use a large C to minimise regularization differences).

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Train multinomial logistic regression on the digits dataset (load_digits).
# Show the 10 x 64 coefficient matrix as 8x8 images (one per digit), find the
# most confused class pair from a confusion matrix, and check calibration
# with sklearn.calibration.calibration_curve.

# YOUR CODE:

