# ======================================
# TOPIC: CLASSIFICATION METRICS
# LEVEL: INTERMEDIATE
# ID: ml.evaluation.classification-metrics
# ======================================

# INTRODUCTION
# "99% accurate" can mean useless: if 1% of transactions are fraud, a model
# that always says "not fraud" is 99% accurate. Choosing the right metric is
# choosing what "good" means for the business. These metrics are also used to
# evaluate LLM classifiers and prompts later in the course.
#
# THEORY
# CONFUSION MATRIX (binary): TP, FP (false alarm), FN (missed), TN.
# - ACCURACY = (TP + TN) / all. Misleading with imbalanced classes.
# - PRECISION = TP / (TP + FP): of predicted positives, how many are right?
#   Important when false alarms are costly (spam filter hiding real email).
# - RECALL = TP / (TP + FN): of actual positives, how many did we find?
#   Important when misses are costly (cancer screening, fraud).
# - F1 = harmonic mean of precision and recall.
# - ROC-AUC: ranking quality across all thresholds (0.5 random, 1.0 perfect).
#   PR-AUC (average precision) is more informative for rare positives.
# - Multiclass: per-class metrics averaged with "macro" (classes equal) or
#   "weighted" (by support).
# - Always compare with a BASELINE (DummyClassifier).
#
# REAL-WORLD ANALOGY
# A fishing net: precision = what fraction of the catch is the fish you
# wanted; recall = what fraction of those fish in the lake you caught.
#
# SYNTAX:
#   confusion_matrix(y_true, y_pred); classification_report(y_true, y_pred)
#   precision_score, recall_score, f1_score, roc_auc_score(y_true, scores)
#
# SMALL WORKING EXAMPLE:
from sklearn.datasets import make_classification
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (average_precision_score, classification_report,
                             confusion_matrix, roc_auc_score)
from sklearn.model_selection import train_test_split

X, y = make_classification(n_samples=5000, weights=[0.97], flip_y=0.01, random_state=1)
X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, random_state=1)
dummy = DummyClassifier(strategy="most_frequent").fit(X_train, y_train)
model = LogisticRegression(max_iter=1000).fit(X_train, y_train)
print("dummy accuracy:", round(dummy.score(X_test, y_test), 3), "(predicts no positives at all)")
scores = model.predict_proba(X_test)[:, 1]
for threshold in (0.5, 0.2):
    predictions = (scores >= threshold).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_test, predictions).ravel()
    print(f"threshold {threshold}: TP={tp} FP={fp} FN={fn} TN={tn}")
    print(classification_report(y_test, predictions, digits=3, zero_division=0).splitlines()[3])
print("ROC-AUC:", round(roc_auc_score(y_test, scores), 3), "| PR-AUC:", round(average_precision_score(y_test, scores), 3))

# EXPLANATION (LINE BY LINE):
# weights=[0.97]           -> only ~3% positives: an imbalanced problem.
# DummyClassifier          -> always predicts the majority class: ~97% accuracy, 0 recall.
# predict_proba(...)[:, 1] -> scores; we choose the threshold ourselves.
# confusion_matrix(...).ravel() -> tn, fp, fn, tp for binary problems.
# classification_report line 3 -> precision/recall/F1 for the positive class.
# Lower threshold (0.2)    -> recall goes up, precision goes down: the trade-off.
# ROC-AUC / PR-AUC         -> threshold-independent ranking quality.
#
# COMMON MISTAKES:
# 1. Reporting accuracy on imbalanced data.
# 2. Using the default 0.5 threshold without thinking about costs.
# 3. Computing ROC-AUC from hard predictions instead of scores.
# 4. Comparing models on different test sets.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Given y_true = [1,0,1,1,0,0,1,0,1,0] and y_pred = [1,0,0,1,0,1,1,0,0,0],
# compute TP, FP, FN, TN, accuracy, precision, recall and F1 by hand
# (comments) and verify with sklearn.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Plot the precision-recall curve and the ROC curve for the model above. Find
# the threshold that maximises F1, and the lowest threshold that keeps
# precision >= 0.8.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Fraud costs 500 when missed, and a manual review (false alarm) costs 5.
# Write expected_cost(y_true, scores, threshold) and choose the threshold that
# minimises cost on a VALIDATION split, then report cost on the test split.
# Compare against the F1-optimal threshold.

# YOUR CODE:

