# ======================================
# TOPIC: VECTOR SEARCH AND VECTOR DATABASES
# LEVEL: ADVANCED
# ID: generative-ai.embeddings.vector-search
# ======================================

# INTRODUCTION
# With millions of embeddings, comparing the query to every vector is too
# slow. Vector databases store embeddings with metadata and find nearest
# neighbours quickly - the retrieval engine behind RAG.
#
# THEORY
# - EXACT search (brute force): score every vector; perfect recall, O(n) per
#   query. Fine up to ~100k vectors with NumPy.
# - APPROXIMATE nearest neighbour (ANN) indexes trade a little recall for big
#   speed-ups: HNSW (graph-based, most common), IVF (cluster then search a few
#   clusters), product quantisation (compression).
# - Vector databases: pgvector (Postgres extension), Qdrant, Weaviate, Milvus,
#   Chroma, Pinecone; libraries: FAISS. They add persistence, METADATA
#   FILTERING (e.g. tenant_id, date), updates/deletes and scaling.
# - Measure ANN quality with RECALL@k against exact search.
# - Filtering + multi-tenancy are security features: never let a query return
#   another customer's documents.
#
# REAL-WORLD ANALOGY
# Finding a book: checking every shelf is exact but slow; going straight to
# the right section (cluster) and checking only nearby shelves is much faster
# and almost always finds it.
#
# SYNTAX:
#   scores = matrix @ query; top_k = np.argpartition(-scores, k)[:k]
#
# SMALL WORKING EXAMPLE:
import time

import numpy as np
from sklearn.cluster import KMeans

rng = np.random.default_rng(0)
n, d = 20_000, 64
topics = rng.normal(size=(300, d))
vectors = (topics[rng.integers(0, 300, n)] + rng.normal(scale=0.35, size=(n, d))).astype(np.float32)
vectors /= np.linalg.norm(vectors, axis=1, keepdims=True)
tenants = rng.choice(["acme", "globex"], size=n)

def exact_search(query, k=5, mask=None):
    scores = vectors @ query
    if mask is not None:
        scores = np.where(mask, scores, -np.inf)
    top = np.argpartition(-scores, k)[:k]
    return top[np.argsort(-scores[top])]

class IVFIndex:
    def __init__(self, data, n_clusters=64):
        self.kmeans = KMeans(n_clusters=n_clusters, n_init=1, random_state=0).fit(data)
        self.lists = {c: np.flatnonzero(self.kmeans.labels_ == c) for c in range(n_clusters)}

    def search(self, query, k=5, n_probe=8):
        centroid_scores = self.kmeans.cluster_centers_ @ query
        probe = np.argsort(-centroid_scores)[:n_probe]
        candidates = np.concatenate([self.lists[c] for c in probe])
        scores = vectors[candidates] @ query
        return candidates[np.argsort(-scores)[:k]], len(candidates)

index = IVFIndex(vectors)
queries = vectors[rng.choice(n, 50)] + rng.normal(scale=0.3, size=(50, d)).astype(np.float32)
recall, checked = [], []
start = time.perf_counter()
for q in queries:
    exact = set(exact_search(q))
    approx, n_checked = index.search(q)
    recall.append(len(exact & set(approx)) / 5)
    checked.append(n_checked)
print(f"IVF recall@5 {np.mean(recall):.2f} while scoring {np.mean(checked) / n:.0%} of vectors")
hits = exact_search(queries[0], mask=(tenants == "acme"))
print("tenant-filtered results all acme:", set(tenants[hits]) == {"acme"})

# EXPLANATION (LINE BY LINE):
# 20,000 vectors grouped around 300 "topics" stand in for document embeddings
#   (real embeddings are clustered like this; pure random data is the worst case
#   for IVF). Each vector has a tenant.
# exact_search               -> brute-force dot products; argpartition finds top-k fast;
#                               an optional mask implements metadata filtering.
# IVFIndex                   -> k-means clusters the vectors; search only the n_probe
#                               closest clusters' members.
# recall@5                   -> fraction of the true top-5 found by the ANN index,
#                               while scoring only a fraction of all vectors.
# Tenant mask                -> filtering guarantees no cross-tenant results.
#
# COMMON MISTAKES:
# 1. Using ANN without measuring recall.
# 2. Filtering AFTER retrieving top-k (may return nothing or leak data) instead of
#    filtering inside the search.
# 3. Re-indexing everything on each small update.
# 4. Storing embeddings without the model name/version.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Vary n_probe (1, 4, 8, 16, 32) and print recall@5 and fraction scored for
# each. Describe the trade-off.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Write a small VectorStore class: add(ids, vectors, metadata), delete(id),
# search(query, k, where={"tenant": "acme"}), and save/load to .npz + JSON.
# Test it with 1,000 vectors.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Install faiss-cpu or run Qdrant/pgvector locally (Docker). Index 100k
# vectors with HNSW, measure query latency and recall@10 vs exact search for
# different index parameters, and write up which settings you'd choose.

# YOUR CODE:

