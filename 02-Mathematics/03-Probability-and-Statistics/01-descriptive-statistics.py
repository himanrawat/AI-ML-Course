# ======================================
# TOPIC: DESCRIPTIVE STATISTICS
# LEVEL: BEGINNER
# ID: math.statistics.descriptive
# ======================================

# INTRODUCTION
# Before modelling anything, you summarise data: what is typical, how spread
# out it is, whether there are outliers. (Study with 03-Data-Science EDA.)
#
# THEORY
# - Central tendency: MEAN (average, sensitive to outliers), MEDIAN (middle
#   value, robust), MODE (most frequent).
# - Spread: RANGE, VARIANCE (average squared distance from the mean),
#   STANDARD DEVIATION (square root of variance, same units as the data),
#   PERCENTILES / QUARTILES, IQR = Q3 - Q1.
# - Sample variance divides by (n - 1) (np.var(x, ddof=1)); population by n.
# - Z-SCORE: (x - mean) / std = how many standard deviations from the mean.
# - CORRELATION (Pearson r in [-1, 1]) measures LINEAR relationship between two
#   variables. Correlation is not causation.
# - Outlier rule of thumb: outside [Q1 - 1.5 IQR, Q3 + 1.5 IQR].
#
# REAL-WORLD ANALOGY
# Salaries in a small company with one billionaire founder: the mean salary
# looks huge, the median tells the real story of a typical employee.
#
# SYNTAX:
#   np.mean, np.median, np.std(x, ddof=1), np.percentile(x, [25, 50, 75]),
#   np.corrcoef(x, y)
#
# SMALL WORKING EXAMPLE:
import statistics

import numpy as np

salaries = np.array([42, 45, 47, 50, 52, 55, 58, 60, 900], dtype=float)
print("mean:", round(salaries.mean(), 1), "| median:", np.median(salaries))
print("std (sample):", round(salaries.std(ddof=1), 1))
q1, q3 = np.percentile(salaries, [25, 75])
iqr = q3 - q1
outliers = salaries[(salaries < q1 - 1.5 * iqr) | (salaries > q3 + 1.5 * iqr)]
print("Q1, Q3, IQR:", q1, q3, iqr, "| outliers:", outliers)
z_scores = (salaries - salaries.mean()) / salaries.std(ddof=1)
print("z-scores:", np.round(z_scores, 2))
print("mode:", statistics.mode([1, 2, 2, 3, 3, 3]))
hours = np.array([1, 2, 3, 4, 5, 6])
scores = np.array([52, 55, 61, 68, 70, 79])
print("correlation hours vs scores:", round(np.corrcoef(hours, scores)[0, 1], 3))

# EXPLANATION (LINE BY LINE):
# salaries includes one extreme value (900).
# mean ~ 145 is pulled up by the outlier; median 52 is robust.
# std(ddof=1)          -> sample standard deviation.
# percentile([25, 75]) -> Q1 and Q3; IQR is their difference.
# boolean mask with |  -> values outside the IQR fences are outliers: [900].
# z-scores             -> the outlier is about 2.7 standard deviations above the mean.
# statistics.mode      -> the most common value (3).
# np.corrcoef(...)[0, 1] -> strong positive correlation (~0.99).
#
# COMMON MISTAKES:
# 1. Reporting only the mean for skewed data.
# 2. Mixing ddof=0 (NumPy's default) and ddof=1 (pandas' default).
# 3. Reading correlation as causation.
# 4. Deleting outliers without understanding them (they may be the signal).

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# For the data [4, 8, 6, 5, 3, 7, 9, 5], compute mean, median, mode, range,
# variance and standard deviation by hand (comments) and with NumPy.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Generate 1,000 samples from a normal distribution and 1,000 from an
# exponential distribution. Compare their mean/median and draw both histograms.
# Explain how skew shows up in mean vs median.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Create Anscombe-style data: 4 pairs of (x, y) arrays with nearly identical
# means, variances and correlation but very different shapes (or load
# seaborn-free versions by hand). Plot them in a 2x2 grid and write the lesson
# in a comment.

# YOUR CODE:

