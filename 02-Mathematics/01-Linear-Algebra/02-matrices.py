# ======================================
# TOPIC: MATRICES
# LEVEL: BEGINNER
# ID: math.linear-algebra.matrices
# ======================================

# INTRODUCTION
# A dataset is a matrix: rows are examples, columns are features. A neural
# network layer is a matrix of weights. Matrices let us process many vectors
# at once.
#
# THEORY
# - A matrix is a 2D grid of numbers with SHAPE (rows, columns).
#   X[i, j] is the element in row i, column j.
# - Convention in ML: X has shape (n_samples, n_features).
# - Element-wise operations (+, -, *) need the same shape (or broadcasting).
# - TRANSPOSE X.T swaps rows and columns: shape (m, n) -> (n, m).
# - Identity matrix I: 1s on the diagonal, 0 elsewhere; I @ A = A.
# - Special shapes: square (n, n), diagonal, symmetric (A == A.T).
# - Tensors generalise matrices to more dimensions: images are
#   (height, width, channels); batches add another axis.
#
# REAL-WORLD ANALOGY
# A spreadsheet: each row is a customer, each column a property (age, income).
# Transposing turns it sideways so each row becomes a property.
#
# SYNTAX:
#   X = np.array([[1, 2], [3, 4]]);  X.shape;  X.T;  np.eye(3)
#   X[0], X[:, 1], X[1, 0]
#
# SMALL WORKING EXAMPLE:
import numpy as np

X = np.array([
    [25, 50_000, 2],
    [32, 64_000, 5],
    [47, 120_000, 20],
    [51, 98_000, 25],
], dtype=float)
print("shape:", X.shape, "| samples:", X.shape[0], "| features:", X.shape[1])
print("first customer:", X[0])
print("all incomes:", X[:, 1])
print("column means:", X.mean(axis=0))
X_centered = X - X.mean(axis=0)
print("centered column means ~ 0:", np.allclose(X_centered.mean(axis=0), 0))
print("transpose shape:", X.T.shape)
I = np.eye(3)
print("identity keeps rows unchanged:", np.allclose(X @ I, X))
S = X.T @ X
print("X^T X is symmetric:", np.allclose(S, S.T), S.shape)

# EXPLANATION (LINE BY LINE):
# X = 4 customers x 3 features (age, income, years as customer).
# X.shape -> (4, 3).
# X[0] -> first row (one customer); X[:, 1] -> second column (all incomes).
# X.mean(axis=0) -> average of each COLUMN (axis 0 runs down the rows).
# X - X.mean(axis=0) -> broadcasting subtracts each column's mean: "centering".
# X.T -> shape (3, 4).
# X @ I -> multiplying by the identity changes nothing.
# X.T @ X -> a (3, 3) symmetric matrix; it appears in linear regression and PCA.
#
# COMMON MISTAKES:
# 1. Mixing up axis=0 (down the rows, per column) and axis=1 (across columns).
# 2. Confusing shape (rows, cols) order.
# 3. Using nested Python lists for maths instead of NumPy arrays.
# 4. Forgetting to scale features that have very different ranges (age vs income).

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Create a 3x4 matrix of numbers 1..12 (np.arange + reshape). Print its shape,
# its transpose, the second row, the last column, and the element at row 2, col 3.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Using X from the example, standardize every column (subtract mean, divide by
# standard deviation). Verify each column now has mean 0 and std 1.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Represent a batch of 8 grayscale 28x28 images as a tensor of shape
# (8, 28, 28). Flatten it to (8, 784) for a dense layer, compute per-image
# mean brightness, and per-pixel mean across the batch. Then reshape back and
# verify nothing was lost.

# YOUR CODE:

