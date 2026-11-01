# ======================================
# TOPIC: INDEXING, VECTORIZATION AND BROADCASTING
# LEVEL: INTERMEDIATE
# ID: data-science.numpy.indexing-broadcasting
# ======================================

# INTRODUCTION
# Data cleaning and feature engineering are mostly "select these values,
# transform them". NumPy does that without loops using indexing,
# vectorized operations and broadcasting.
#
# THEORY
# - Basic indexing/slicing: a[0], a[1:3], a[:, 0], a[::2] (returns views).
# - BOOLEAN MASKS: a[a > 0] selects values where the condition is True.
#   Combine conditions with & | ~ and parentheses.
# - FANCY INDEXING: a[[0, 2, 5]] selects specific positions (returns a copy).
# - VECTORIZATION: operations apply element-wise to whole arrays (a * 2, np.log(a)).
# - BROADCASTING: arrays with different shapes combine when, comparing shapes
#   from the right, each dimension is equal or 1. Example: (4, 3) - (3,) works;
#   (4, 3) - (4,) fails, but (4, 3) - (4, 1) works.
# - np.where(cond, x, y) picks values element-wise. Reductions: sum, mean,
#   max, argmax with axis=.
#
# REAL-WORLD ANALOGY
# A teacher adding 5 bonus points: instead of updating each student one by
# one, they announce "everyone +5" (vectorization). Different bonuses per
# subject applied to every student is broadcasting.
#
# SYNTAX:
#   X[mask], X[:, [0, 2]], np.where(X > 0, X, 0), X - X.mean(axis=0)
#
# SMALL WORKING EXAMPLE:
import numpy as np

scores = np.array([
    [78, 92, 65],
    [88, 54, 90],
    [45, 70, 81],
    [93, 88, 97],
])
print("student 2:", scores[1], "| subject 1 column:", scores[:, 0])
print("all scores above 85:", scores[scores > 85])
passed_all = (scores >= 60).all(axis=1)
print("students who passed every subject:", np.flatnonzero(passed_all))
print("best subject per student:", scores.argmax(axis=1))
curved = scores + np.array([5, 0, 2])
print("curved:\n", curved)
student_bonus = np.array([[1], [2], [3], [4]])
print("per-student bonus shape:", (scores + student_bonus).shape)
standardized = (scores - scores.mean(axis=0)) / scores.std(axis=0)
print("standardized column means ~ 0:", np.round(standardized.mean(axis=0), 6))
print("clip below 60 to 60:\n", np.where(scores < 60, 60, scores))

# EXPLANATION (LINE BY LINE):
# scores[1], scores[:, 0]      -> a row and a column.
# scores[scores > 85]          -> boolean mask returns the matching values (1D).
# (scores >= 60).all(axis=1)   -> True for rows where every subject passed.
# np.flatnonzero(...)          -> indexes of True values.
# argmax(axis=1)               -> column index of each row's maximum.
# scores + [5, 0, 2]           -> (4,3) + (3,) broadcasts a per-subject curve.
# scores + (4,1) column        -> broadcasts a per-student bonus across columns.
# (scores - mean) / std        -> standardization in one line via broadcasting.
# np.where(cond, 60, scores)   -> element-wise if/else.
#
# COMMON MISTAKES:
# 1. Using and/or instead of &/| for masks (and forgetting parentheses).
# 2. Broadcasting along the wrong axis without realising (check shapes!).
# 3. Writing Python loops over array elements.
# 4. Modifying a slice (view) and accidentally changing the original.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# From a 5x5 array of 1..25, select: the centre value, the last row, every
# other column, all even numbers, and the 2x2 bottom-right block.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Generate (100, 4) random data with some values set to np.nan. Replace each
# NaN with its column mean (np.nanmean + np.where/broadcasting, no loops).
# Then cap every value at the 99th percentile of its column.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Compute the full pairwise Euclidean distance matrix between 500 points in
# 3D using broadcasting (shape (500, 1, 3) - (1, 500, 3)). Find each point's
# nearest neighbour (excluding itself) and compare speed with a double loop
# on 100 points.

# YOUR CODE:

