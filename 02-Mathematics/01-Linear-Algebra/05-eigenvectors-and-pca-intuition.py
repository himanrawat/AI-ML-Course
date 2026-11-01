# ======================================
# TOPIC: EIGENVECTORS, EIGENVALUES AND PCA INTUITION
# LEVEL: ADVANCED
# ID: math.linear-algebra.eigen-pca
# ======================================

# INTRODUCTION
# High-dimensional data often varies mostly along a few directions.
# Eigenvectors find those directions; PCA (Principal Component Analysis) uses
# them to compress data. (Study together with 04-Machine-Learning
# unsupervised learning.)
#
# THEORY
# - An EIGENVECTOR v of a square matrix A is a direction that A only stretches:
#   A @ v = lambda * v. The scale factor lambda is its EIGENVALUE.
# - For the COVARIANCE matrix of centered data, eigenvectors are the directions
#   of maximum variance and eigenvalues tell how much variance each captures.
# - PCA steps: 1) center the data, 2) covariance matrix C = X.T @ X / (n - 1),
#   3) eigen-decompose C, 4) sort by eigenvalue, 5) project X onto the top k
#   eigenvectors.
# - Explained variance ratio = eigenvalue / sum of eigenvalues.
# - Use np.linalg.eigh for symmetric matrices (like covariance). In practice
#   PCA is computed with SVD (np.linalg.svd), which is more stable.
#
# REAL-WORLD ANALOGY
# Photographing a long, thin cigar: from the side you see its full shape;
# from the end you see a tiny circle. PCA finds the "side view" - the angle
# that shows the most spread.
#
# SYNTAX:
#   values, vectors = np.linalg.eigh(C)   # columns of vectors are eigenvectors
#
# SMALL WORKING EXAMPLE:
import numpy as np

A = np.array([[2.0, 0.0], [0.0, 0.5]])
v = np.array([1.0, 0.0])
print("A @ v =", A @ v, "= 2 * v")
rng = np.random.default_rng(42)
t = rng.normal(size=200)
X = np.column_stack([t, 0.5 * t + rng.normal(scale=0.1, size=200)])
Xc = X - X.mean(axis=0)
C = Xc.T @ Xc / (len(Xc) - 1)
values, vectors = np.linalg.eigh(C)
order = np.argsort(values)[::-1]
values, vectors = values[order], vectors[:, order]
print("eigenvalues:", np.round(values, 3))
print("explained variance ratio:", np.round(values / values.sum(), 3))
print("first principal direction:", np.round(vectors[:, 0], 3))
Z = Xc @ vectors[:, :1]
X_back = Z @ vectors[:, :1].T + X.mean(axis=0)
print("1D compression error:", round(float(np.mean((X - X_back) ** 2)), 4))

# EXPLANATION (LINE BY LINE):
# A stretches the x-axis by 2: [1, 0] is an eigenvector with eigenvalue 2.
# X: 200 points lying near the line y = 0.5x (plus small noise).
# Xc = X - mean -> PCA needs centered data.
# C = covariance matrix (2 x 2, symmetric).
# np.linalg.eigh(C) -> eigenvalues ascending; we re-sort descending.
# explained variance ratio -> the first direction captures ~99% of the variance.
# vectors[:, 0] -> roughly (-0.89, -0.45): the direction of the line (the sign is
#                  arbitrary - (0.89, 0.45) is the same direction; see Question 3).
# Z = projection onto 1 component; X_back = reconstruction -> tiny error.
#
# COMMON MISTAKES:
# 1. Forgetting to center (and usually scale) the data before PCA.
# 2. Reading eigenvectors as ROWS instead of COLUMNS of the returned matrix.
# 3. Assuming eigh returns values sorted from largest to smallest (it does not).
# 4. Interpreting principal components as original features.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# For A = [[4, 1], [2, 3]], use np.linalg.eig to find eigenvalues and
# eigenvectors, and verify A @ v == lambda * v for each pair.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Implement pca(X, k) returning (projected, components, explained_ratio) using
# eigh. Apply it to 3D data that mostly lies on a plane and show 2 components
# explain almost all variance.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Re-implement PCA with np.linalg.svd and show it matches your eigh version
# (up to sign). Compare against sklearn.decomposition.PCA on the same data.
# Explain in comments why the sign of a component is arbitrary.

# YOUR CODE:

