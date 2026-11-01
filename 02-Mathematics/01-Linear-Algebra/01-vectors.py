# ======================================
# TOPIC: VECTORS
# LEVEL: BEGINNER
# ID: math.linear-algebra.vectors
# ======================================

# INTRODUCTION
# In ML, every data point is a vector: a house is [area, rooms, age], a word is
# an embedding of 1,536 numbers. Vector maths is how models compare and combine
# data. (Learn this right before/with 03-Data-Science NumPy arrays.)
#
# THEORY
# - A vector is an ordered list of numbers; its length is its DIMENSION.
#   Geometrically it is an arrow from the origin to a point.
# - Addition: add element by element. Scalar multiplication: scale every element.
# - DOT PRODUCT: a . b = sum(a_i * b_i). It measures how much two vectors point
#   the same way: a . b = |a| |b| cos(theta).
#   - Positive: similar direction; 0: perpendicular (unrelated); negative: opposite.
# - The dot product is the core of linear models (w . x + b) and of attention.
# - In NumPy: np.array, a + b, 3 * a, a @ b or np.dot(a, b).
#
# REAL-WORLD ANALOGY
# Directions on a map: "3 km east, 4 km north" is a vector. Two walkers
# heading in similar directions have a large positive dot product.
#
# SYNTAX:
#   a = np.array([1, 2, 3])
#   a + b, 2 * a, a @ b
#
# SMALL WORKING EXAMPLE:
import numpy as np

house = np.array([120.0, 3.0, 10.0])
weights = np.array([0.5, 10.0, -1.0])
bias = 20.0
price = house @ weights + bias
print("predicted price:", price)
a = np.array([1.0, 0.0])
b = np.array([0.0, 1.0])
c = np.array([-1.0, 0.0])
print("a.b =", a @ b, "| a.a =", a @ a, "| a.c =", a @ c)
print("sum:", a + b, "scaled:", 3 * a)
manual = sum(x * w for x, w in zip(house, weights))
print("manual dot equals numpy:", np.isclose(manual, house @ weights))

# EXPLANATION (LINE BY LINE):
# house = [area, rooms, age]           -> one data point as a vector.
# weights                              -> how much each feature affects price.
# house @ weights + bias               -> 120*0.5 + 3*10 + 10*(-1) + 20 = 100:
#                                         exactly what linear regression computes.
# a @ b = 0                            -> perpendicular vectors (unrelated).
# a @ a = 1                            -> a vector with itself: its squared length.
# a @ c = -1                           -> opposite directions.
# sum(x * w ...)                       -> the dot product written out by hand.
#
# COMMON MISTAKES:
# 1. Using * (element-wise product) when you need @ (dot product).
# 2. Adding Python lists ([1] + [2] concatenates!) instead of NumPy arrays.
# 3. Dot product of vectors with different lengths -> ValueError.
# 4. Forgetting that the dot product depends on length as well as direction.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Create vectors u = [2, 3, 1] and v = [1, -1, 4]. Compute u + v, u - v,
# 2u + 3v and u . v by hand (in a comment) and with NumPy.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Represent 4 students as vectors of [maths, science, english] scores.
# Using the dot product with a weights vector, compute each student's
# weighted score and rank them. Implement dot(a, b) yourself and compare.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Generate 1,000 random 300-dimensional vectors. Show empirically that random
# high-dimensional vectors are almost perpendicular: compute the distribution
# of cosine values between random pairs (mean, std, min, max). Explain why
# this matters for embeddings.

# YOUR CODE:

