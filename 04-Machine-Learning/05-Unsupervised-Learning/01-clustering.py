# ======================================
# TOPIC: CLUSTERING
# LEVEL: INTERMEDIATE
# ID: ml.unsupervised.clustering
# ======================================

# INTRODUCTION
# Without labels you can still find structure: customer segments, topics in
# documents, groups of similar support tickets. Clustering groups similar items.
#
# THEORY
# K-MEANS:
# - Choose k. Initialise k centroids. Repeat: assign each point to its nearest
#   centroid; move each centroid to the mean of its points. Stop when stable.
# - Minimises INERTIA (within-cluster squared distances). Sensitive to scale
#   and initialisation (use k-means++ and several n_init).
# - Assumes roughly round, similarly sized clusters.
# CHOOSING k: elbow method (inertia vs k), SILHOUETTE score
# (-1..1; higher = better separated).
# DBSCAN: groups dense regions, finds arbitrary shapes, marks outliers as
#   noise (-1); parameters eps and min_samples; no k needed.
# HIERARCHICAL (agglomerative): merges closest clusters step by step; a
#   dendrogram shows the hierarchy.
# Clusters are hypotheses - interpret and validate them with domain knowledge.
#
# REAL-WORLD ANALOGY
# Sorting a pile of mixed Lego bricks without instructions: you naturally
# group by colour and shape, deciding how many piles make sense.
#
# SYNTAX:
#   KMeans(n_clusters=k, n_init=10, random_state=0).fit_predict(X_scaled)
#   silhouette_score(X_scaled, labels); DBSCAN(eps=0.3, min_samples=5)
#
# SMALL WORKING EXAMPLE:
import numpy as np
from sklearn.cluster import DBSCAN, KMeans
from sklearn.datasets import make_blobs, make_moons
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

X, true_labels = make_blobs(n_samples=600, centers=4, cluster_std=1.0, random_state=3)
X = StandardScaler().fit_transform(X)
for k in range(2, 7):
    km = KMeans(n_clusters=k, n_init=10, random_state=0).fit(X)
    print(f"k={k}: inertia {km.inertia_:7.1f}  silhouette {silhouette_score(X, km.labels_):.3f}")
km = KMeans(n_clusters=4, n_init=10, random_state=0).fit(X)
print("cluster sizes:", np.bincount(km.labels_).tolist())
moons, _ = make_moons(n_samples=400, noise=0.06, random_state=0)
km_moons = KMeans(n_clusters=2, n_init=10, random_state=0).fit_predict(moons)
db_moons = DBSCAN(eps=0.2, min_samples=5).fit_predict(moons)
print("k-means silhouette on moons:", round(silhouette_score(moons, km_moons), 3))
print("DBSCAN clusters found:", len(set(db_moons) - {-1}), "| noise points:", int(np.sum(db_moons == -1)))

# EXPLANATION (LINE BY LINE):
# make_blobs with 4 centres     -> data with a known group structure.
# StandardScaler                -> distance-based methods need comparable scales.
# Loop over k                   -> inertia always falls as k grows (elbow near 4);
#                                  silhouette peaks at the best k.
# np.bincount(labels)           -> how many points fell into each cluster.
# make_moons                    -> two crescent shapes (not round).
# K-means splits the moons with a straight boundary (wrong shape assumption).
# DBSCAN follows the dense crescents and finds 2 clusters (+ any noise points).
#
# COMMON MISTAKES:
# 1. Clustering unscaled features.
# 2. Using inertia alone to choose k.
# 3. Using k-means for non-convex shapes or very different cluster sizes.
# 4. Treating cluster IDs as meaningful labels without interpretation.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Cluster the Iris features (without labels) with k-means (k=3). Compare the
# clusters with the true species using pd.crosstab.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Implement k-means from scratch (random init from data points, assign,
# update, stop on convergence). Run it on make_blobs, plot each iteration's
# centroids, and compare inertia with sklearn.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Simulate a customer dataset (recency, frequency, monetary value) with 3
# hidden segments plus outliers. Compare k-means, DBSCAN and
# AgglomerativeClustering, choose one with silhouette + your judgement, and
# write a short profile of each segment (mean features) as comments.

# YOUR CODE:

