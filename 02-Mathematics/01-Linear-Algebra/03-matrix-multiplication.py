# ======================================
# TOPIC: MATRIX MULTIPLICATION
# LEVEL: INTERMEDIATE
# ID: math.linear-algebra.matrix-multiplication
# ======================================

# INTRODUCTION
# A neural network layer is one matrix multiplication plus a bias:
# outputs = inputs @ W + b. GPUs exist largely to do this operation fast.
#
# THEORY
# - (m, n) @ (n, p) -> (m, p). The INNER dimensions must match.
# - Each output element C[i, j] is the dot product of row i of A and column j of B.
# - Not commutative: A @ B != B @ A in general (often not even defined).
# - Associative: (A @ B) @ C == A @ (B @ C).
# - (A @ B).T == B.T @ A.T.
# - A matrix as a TRANSFORMATION: multiplying a vector by a matrix can rotate,
#   scale or project it.
# - Applying a linear layer to a batch: X (batch, in) @ W (in, out) -> (batch, out).
# - INVERSE A^-1 satisfies A @ A^-1 = I (only for square, non-singular matrices).
#   In practice use np.linalg.solve instead of computing the inverse.
#
# REAL-WORLD ANALOGY
# A recipe matrix (dishes x ingredients) times a price vector (ingredient
# prices) gives the cost of each dish: every dish row "dots" with the prices.
#
# SYNTAX:
#   C = A @ B;  np.linalg.solve(A, b);  np.linalg.inv(A)
#
# SMALL WORKING EXAMPLE:
import numpy as np

recipes = np.array([[2, 1, 0], [1, 0, 3]])
prices = np.array([[30], [50], [10]])
print("cost per dish:\n", recipes @ prices)
rng = np.random.default_rng(0)
batch = rng.normal(size=(4, 3))
W = rng.normal(size=(3, 2))
b = np.array([0.1, -0.2])
outputs = batch @ W + b
print("layer output shape:", outputs.shape)
C = np.zeros((4, 2))
for i in range(4):
    for j in range(2):
        C[i, j] = batch[i] @ W[:, j]
print("loop version matches:", np.allclose(C, batch @ W))
theta = np.pi / 2
rotate = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
print("rotate (1, 0) by 90 degrees:", np.round(rotate @ np.array([1.0, 0.0]), 3))
A = np.array([[3.0, 1.0], [1.0, 2.0]])
y = np.array([9.0, 8.0])
print("solve A x = y:", np.linalg.solve(A, y))

# EXPLANATION (LINE BY LINE):
# recipes (2 dishes x 3 ingredients) @ prices (3 x 1) -> (2 x 1) dish costs.
# batch (4 x 3) @ W (3 x 2) + b -> a dense layer: 4 inputs, 3 features -> 2 outputs.
# The double loop computes each C[i, j] as a dot product: same result as @.
# rotate @ [1, 0] -> [0, 1]: a matrix can be a geometric transformation.
# np.linalg.solve(A, y) -> x with A @ x = y (here x = [2, 3]).
#
# COMMON MISTAKES:
# 1. Shape mismatch errors - always write shapes down: (4,3)@(3,2) -> (4,2).
# 2. Using * (element-wise) instead of @.
# 3. Assuming A @ B == B @ A.
# 4. Using np.linalg.inv to solve systems (slower and less accurate).

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Multiply A (2x3) by B (3x2) by hand for small integers (write the steps as
# comments), then verify with NumPy. Show that B @ A has a different shape.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Implement matmul(A, B) with pure Python loops (lists of lists), raise a clear
# error on shape mismatch, and compare its speed with NumPy for 200x200
# matrices using time.perf_counter.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Build a 2-layer network forward pass with NumPy only: X (5, 4) -> W1 (4, 8)
# -> ReLU -> W2 (8, 3) -> softmax. Print every intermediate shape. Verify that
# (A @ B).T == B.T @ A.T and that two stacked linear layers WITHOUT the ReLU
# are equivalent to a single matrix (W1 @ W2). Explain why non-linearity matters.

# YOUR CODE:

