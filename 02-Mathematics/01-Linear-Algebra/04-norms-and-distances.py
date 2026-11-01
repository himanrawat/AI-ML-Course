# ======================================
# TOPIC: NORMS, DISTANCES AND COSINE SIMILARITY
# LEVEL: INTERMEDIATE
# ID: math.linear-algebra.norms-distances
# ======================================

# INTRODUCTION
# "Which documents are most similar to this question?" is the core of semantic
# search and RAG. The answer comes from distances and cosine similarity between
# embedding vectors. Norms also appear in regularization (L1/L2).
#
# THEORY
# - NORM = length of a vector.
#   L2 (Euclidean): sqrt(sum(x_i^2))     L1 (Manhattan): sum(|x_i|)
# - Euclidean distance between a and b: ||a - b||_2.
# - COSINE SIMILARITY = (a . b) / (||a|| ||b||), in [-1, 1].
#   It compares DIRECTION only, ignoring length - good for text embeddings.
# - Normalizing vectors to unit length (divide by the L2 norm) makes cosine
#   similarity equal to a plain dot product (fast in vector databases).
# - L2 regularization penalizes ||w||_2^2; L1 penalizes ||w||_1 (sparse weights).
#
# REAL-WORLD ANALOGY
# Two recipes: one for 2 people, one for 20, with the same ingredient ratios.
# Their ingredient vectors are far apart in distance, but the cosine
# similarity is 1 - they are the same dish, just scaled.
#
# SYNTAX:
#   np.linalg.norm(v);  np.linalg.norm(v, ord=1)
#   cosine = a @ b / (np.linalg.norm(a) * np.linalg.norm(b))
#
# SMALL WORKING EXAMPLE:
import numpy as np

def cosine_similarity(a, b):
    return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b)))

v = np.array([3.0, 4.0])
print("L2:", np.linalg.norm(v), "L1:", np.linalg.norm(v, ord=1))
small_recipe = np.array([2.0, 1.0, 0.5])
large_recipe = small_recipe * 10
print("distance:", round(float(np.linalg.norm(large_recipe - small_recipe)), 2))
print("cosine:", round(cosine_similarity(small_recipe, large_recipe), 3))
docs = {
    "python tutorial": np.array([0.9, 0.1, 0.0]),
    "snake facts": np.array([0.2, 0.9, 0.1]),
    "coding guide": np.array([0.8, 0.0, 0.3]),
}
query = np.array([1.0, 0.0, 0.2])
ranked = sorted(docs, key=lambda d: cosine_similarity(query, docs[d]), reverse=True)
print("ranking:", ranked)
matrix = np.stack(list(docs.values()))
unit = matrix / np.linalg.norm(matrix, axis=1, keepdims=True)
print("all scores at once:", np.round(unit @ (query / np.linalg.norm(query)), 3))

# EXPLANATION (LINE BY LINE):
# np.linalg.norm([3, 4]) -> 5 (the 3-4-5 triangle); L1 -> 7.
# small vs large recipe -> big Euclidean distance, cosine 1.0 (same direction).
# docs                  -> toy 3-dimensional "embeddings".
# sorted(..., key=cosine_similarity(query, ...)) -> semantic search in one line.
# matrix / norm(..., axis=1, keepdims=True) -> normalize every row to length 1.
# unit @ unit_query     -> cosine scores for ALL docs with one matrix product.
#
# COMMON MISTAKES:
# 1. Dividing by a zero norm (all-zero vector) -> nan.
# 2. Forgetting keepdims=True, which breaks broadcasting.
# 3. Mixing cosine similarity (higher = closer) with distance (lower = closer).
# 4. Comparing embeddings produced by DIFFERENT models.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Compute the L1 and L2 norms of [1, -2, 2] by hand and with NumPy. Compute the
# Euclidean distance between [0, 0] and [6, 8].

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Write pairwise_cosine(M) returning an (n, n) matrix of cosine similarities
# for the rows of M without Python loops. Check the diagonal is all 1 and the
# matrix is symmetric.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Build a tiny "bag of words" embedding: a vocabulary from 6 sentences, each
# sentence -> word-count vector. Implement search(query, k) returning the top-k
# sentences by cosine similarity. Then show a case where Euclidean distance and
# cosine similarity give DIFFERENT rankings and explain why.

# YOUR CODE:

