# ======================================
# TOPIC: NUMPY ARRAYS AND DTYPES
# LEVEL: BEGINNER
# ID: data-science.numpy.arrays
# ======================================

# INTRODUCTION
# NumPy is the foundation of the Python data and ML stack: pandas, scikit-learn
# and PyTorch all build on its array model. Its arrays are fast because the
# heavy work runs in compiled C code.
#
# THEORY
# - np.ndarray: an n-dimensional grid of values of ONE data type (dtype).
# - Key attributes: .shape, .ndim, .size, .dtype.
# - Creation: np.array(list), np.zeros, np.ones, np.full, np.arange,
#   np.linspace, np.eye, rng = np.random.default_rng(seed) for random data.
# - dtypes: int64, float64 (default floats), float32 (common in deep learning,
#   half the memory), bool, str. .astype() converts.
# - reshape(rows, cols) changes the shape without copying when possible;
#   -1 means "infer this dimension".
# - Arrays are much faster and smaller than lists for numeric work.
#
# REAL-WORLD ANALOGY
# An egg carton: a fixed grid of identical slots, each holding the same kind
# of thing. A Python list is a shopping bag - flexible but slow to search.
#
# SYNTAX:
#   a = np.array([1, 2, 3], dtype=np.float32)
#   np.arange(0, 10, 2); np.linspace(0, 1, 5); a.reshape(-1, 1)
#
# SMALL WORKING EXAMPLE:
import time

import numpy as np

a = np.array([[1, 2, 3], [4, 5, 6]])
print(a.shape, a.ndim, a.size, a.dtype)
print(np.zeros((2, 3)), np.linspace(0, 1, 5), sep="\n")
grid = np.arange(12).reshape(3, -1)
print(grid)
weights = grid.astype(np.float32)
print(weights.dtype, weights.nbytes, "bytes vs", grid.nbytes)
rng = np.random.default_rng(42)
print(rng.normal(size=3).round(3))
values = list(range(1_000_000))
array = np.arange(1_000_000)
start = time.perf_counter(); sum(v * v for v in values); t_list = time.perf_counter() - start
start = time.perf_counter(); int((array * array).sum()); t_np = time.perf_counter() - start
print(f"list: {t_list:.3f}s  numpy: {t_np:.4f}s")

# EXPLANATION (LINE BY LINE):
# np.array([[...], [...]])  -> 2x3 array; dtype int64.
# shape (2, 3), ndim 2, size 6.
# np.zeros((2, 3))          -> array of zeros (float64).
# np.linspace(0, 1, 5)      -> 5 evenly spaced values including both ends.
# np.arange(12).reshape(3, -1) -> 3 rows; -1 lets NumPy compute 4 columns.
# astype(np.float32)        -> 4 bytes per value instead of 8.
# default_rng(42)           -> reproducible random numbers.
# Timing: vectorised NumPy is many times faster than a Python loop.
#
# COMMON MISTAKES:
# 1. Mixing types in np.array (everything becomes strings or objects).
# 2. Integer arrays silently truncating: a = np.array([1, 2]); a[0] = 2.7 -> 2.
# 3. Using np.random.seed global state instead of default_rng.
# 4. Reshaping to incompatible sizes -> ValueError.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Create: a 1D array 0..9, a 3x3 array of 7s, 5 evenly spaced values between
# 10 and 20, and a 4x4 identity matrix. Print shape and dtype for each.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Create a random (1000, 20) float64 array, convert it to float32 and float16,
# and report memory usage and the maximum absolute difference from the
# original for each. When would you accept float16?

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Explore views vs copies: show that slicing returns a VIEW (modifying it
# changes the original), fancy indexing returns a COPY, and use np.shares_memory
# to prove each. Show how reshape can return a view and when .copy() is needed.

# YOUR CODE:

