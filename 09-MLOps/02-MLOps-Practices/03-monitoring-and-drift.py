# ======================================
# TOPIC: MONITORING AND DATA DRIFT
# LEVEL: ADVANCED
# ID: mlops.practices.monitoring-drift
# ======================================

# INTRODUCTION
# Models degrade silently: customers change, products change, upstream data
# pipelines break. Monitoring catches problems before users or the business do.
#
# THEORY
# What to monitor:
# - SERVICE health: request rate, errors, latency (p50/p95/p99), saturation.
# - DATA quality: missing values, out-of-range values, schema changes.
# - DATA DRIFT: input feature distributions shift away from training data.
# - PREDICTION drift: output distribution changes (e.g. suddenly 40% "fraud").
# - CONCEPT drift: the relationship between inputs and the target changes
#   (needs labels - often delayed).
# - Model PERFORMANCE once ground truth arrives; business KPIs.
# Drift statistics:
# - PSI (population stability index): sum((a - e) * ln(a / e)) over bins;
#   < 0.1 stable, 0.1-0.25 moderate, > 0.25 significant drift.
# - Kolmogorov-Smirnov test for continuous features; chi-square for categories.
# Response: alert -> investigate -> fix data bug or retrain on recent data ->
# evaluate -> redeploy. Not every drift needs retraining.
#
# REAL-WORLD ANALOGY
# A ship's navigator checking position against the planned route: small
# drift is corrected early; ignoring it means ending up far off course.
#
# SYNTAX:
#   psi = np.sum((actual - expected) * np.log(actual / expected))
#   scipy.stats.ks_2samp(train_values, live_values)
#
# SMALL WORKING EXAMPLE:
import numpy as np
from scipy.stats import ks_2samp

rng = np.random.default_rng(0)
train_income = rng.lognormal(10.5, 0.5, 10_000)
weeks = {
    "week 1 (normal)": rng.lognormal(10.5, 0.5, 2_000),
    "week 2 (slight shift)": rng.lognormal(10.55, 0.5, 2_000),
    "week 3 (new market)": rng.lognormal(10.9, 0.6, 2_000),
    "week 4 (pipeline bug: income sent in thousands)": rng.lognormal(10.5, 0.5, 2_000) / 1000,
}

def psi(expected, actual, bins=10):
    edges = np.quantile(expected, np.linspace(0, 1, bins + 1))
    edges[0], edges[-1] = -np.inf, np.inf
    e = np.histogram(expected, edges)[0] / len(expected)
    a = np.histogram(actual, edges)[0] / len(actual)
    e, a = np.clip(e, 1e-6, None), np.clip(a, 1e-6, None)
    return float(np.sum((a - e) * np.log(a / e)))

for week, live in weeks.items():
    score = psi(train_income, live)
    p_value = ks_2samp(train_income, live).pvalue
    level = "OK" if score < 0.1 else "WARN" if score < 0.25 else "ALERT"
    print(f"{week:<44} PSI {score:7.3f}  KS p={p_value:.3g}  [{level}]")

# EXPLANATION (LINE BY LINE):
# train_income               -> the feature's distribution at training time.
# weeks                      -> live data: stable, slightly shifted, a real market change,
#                               and a unit bug from an upstream pipeline.
# psi()                      -> bins from training-data quantiles; compares bin shares;
#                               clipping avoids log(0).
# ks_2samp                   -> statistical test; with thousands of samples even tiny
#                               shifts become "significant", so PSI thresholds are often
#                               more practical for alerting.
# Week 4                     -> enormous PSI: a data bug, not a reason to retrain.
#
# COMMON MISTAKES:
# 1. Monitoring only uptime and latency, never data or predictions.
# 2. Retraining automatically on corrupted data.
# 3. Alerting on p-values alone with huge samples (constant false alarms).
# 4. No baseline snapshot of the training distribution.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Compute PSI for a categorical feature (plan: basic/pro/enterprise) between
# training shares (60/30/10) and live shares (45/35/20) by hand and in code.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Write a DriftMonitor class that stores baseline distributions for several
# numeric and categorical features, scores a new batch (PSI per feature), and
# returns a report sorted by severity. Test with simulated batches.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Simulate concept drift: train a classifier on data where y depends on x1,
# then generate live data where y gradually depends on x2. Track rolling
# accuracy as delayed labels arrive, detect the drop, retrain on a recent
# window, and plot accuracy over time before and after retraining.

# YOUR CODE:

