# ======================================
# TOPIC: TRAIN/VALIDATION/TEST SPLITS AND DATA LEAKAGE
# LEVEL: BEGINNER
# ID: ml.fundamentals.splits-leakage
# ======================================

# INTRODUCTION
# A model that has seen the exam questions will ace the exam and fail in the
# real world. Proper data splits are how we measure real performance honestly.
#
# THEORY
# - TRAIN set: used to fit parameters.
# - VALIDATION set: used to choose models and hyperparameters.
# - TEST set: touched ONCE at the end to estimate real-world performance.
#   Typical split: 60-80% train, 10-20% validation, 10-20% test.
# - train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
#   stratify keeps class proportions equal in every split.
# - DATA LEAKAGE: information from outside the training data (especially the
#   test set or the future) leaks into training. Forms:
#   * Preprocessing fit on ALL data (scaler/imputer means include test rows).
#   * Features that are only known after the outcome.
#   * Duplicate/near-duplicate rows across splits.
#   * Random splits of TIME SERIES (training on the future). Use time-based splits.
#   * Grouped data (same patient in train and test) - use GroupKFold.
#
# REAL-WORLD ANALOGY
# Practice papers (train), a mock exam to decide your study plan (validation),
# and the final exam you see only once (test).
#
# SYNTAX:
#   X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,
#                                                       stratify=y, random_state=42)
#
# SMALL WORKING EXAMPLE:
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

rng = np.random.default_rng(0)
X = rng.normal(size=(1000, 5))
y = (X[:, 0] + 0.5 * X[:, 1] + rng.normal(scale=1.0, size=1000) > 1.2).astype(int)
X_temp, X_test, y_temp, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
X_train, X_val, y_train, y_val = train_test_split(X_temp, y_temp, test_size=0.25, stratify=y_temp, random_state=42)
print("sizes:", len(X_train), len(X_val), len(X_test))
print("positive rate:", [round(part.mean(), 3) for part in (y_train, y_val, y_test)])
scaler = StandardScaler().fit(X_train)
model = LogisticRegression().fit(scaler.transform(X_train), y_train)
print("validation accuracy:", round(model.score(scaler.transform(X_val), y_val), 3))
leaky_feature = y + rng.normal(scale=0.01, size=1000)
X_leaky = np.column_stack([X, leaky_feature])
Xl_train, Xl_test, yl_train, yl_test = train_test_split(X_leaky, y, test_size=0.2, random_state=42)
leaky_model = LogisticRegression().fit(Xl_train, yl_train)
print("leaky 'accuracy' (too good to be true):", leaky_model.score(Xl_test, yl_test))

# EXPLANATION (LINE BY LINE):
# First split: 80% temp / 20% test. Second split of temp: 75% train / 25% val.
#   -> 600 / 200 / 200 rows.
# stratify=...              -> each split keeps the same positive rate.
# StandardScaler().fit(X_train) -> learn means/stds from TRAINING data only,
#                              then apply to val/test with transform().
# validation accuracy       -> used for decisions; the test set stays untouched.
# leaky_feature             -> basically the label itself plus noise.
# accuracy 1.0              -> a warning sign of leakage, not a great model.
#
# COMMON MISTAKES:
# 1. scaler.fit(X) on the full dataset before splitting.
# 2. Tuning hyperparameters on the test set (it becomes a validation set).
# 3. Random splits for time-ordered data.
# 4. Forgetting stratify with imbalanced classes.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Split the Iris dataset 70/30 with and without stratify. Print class counts
# in each split and explain the difference.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Create a daily time series (365 days) of sales with a trend. Compare a random
# split with a time-based split (first 300 days train, last 65 test) for a
# model using the day index; explain why the random split is overly optimistic.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Demonstrate preprocessing leakage: with 50 samples and 10,000 random
# features (pure noise) and random labels, select the 20 features most
# correlated with y using ALL data, then cross-validate a classifier - accuracy
# looks great. Repeat with feature selection inside a Pipeline (fit only on
# training folds) and show accuracy drops to ~50%.

# YOUR CODE:

