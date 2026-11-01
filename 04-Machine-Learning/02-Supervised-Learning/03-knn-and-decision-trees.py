# ======================================
# TOPIC: K-NEAREST NEIGHBOURS AND DECISION TREES
# LEVEL: INTERMEDIATE
# ID: ml.supervised.knn-trees
# ======================================

# INTRODUCTION
# Two intuitive, non-linear models: k-NN predicts from similar examples (the
# same idea as retrieval in RAG); decision trees learn readable if/else rules
# and are the base of the strongest tabular models (random forests, boosting).
#
# THEORY
# k-NEAREST NEIGHBOURS:
# - No training: store the data. To predict, find the k closest training
#   points (distance metric) and vote (classification) or average (regression).
# - Small k: flexible, noisy (overfit). Large k: smooth (underfit).
# - Distances need SCALED features. Slow on big data (unless indexed).
# DECISION TREES:
# - Recursively split the data on the feature/threshold that makes child
#   nodes most PURE. Impurity: GINI = 1 - sum(p_k^2), or ENTROPY =
#   -sum(p_k log2 p_k). Regression trees minimise variance.
# - Hyperparameters controlling overfitting: max_depth, min_samples_leaf.
# - No scaling needed; captures non-linearity and interactions; interpretable;
#   but a single deep tree overfits and is unstable.
#
# REAL-WORLD ANALOGY
# k-NN: guessing a house price from the 5 most similar houses nearby.
# Decision tree: a doctor's flowchart - "fever? -> yes: rash? -> ...".
#
# SYNTAX:
#   KNeighborsClassifier(n_neighbors=5)
#   DecisionTreeClassifier(max_depth=3, min_samples_leaf=5)
#   export_text(tree, feature_names=...)
#
# SMALL WORKING EXAMPLE:
import numpy as np
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier, export_text

def gini(labels):
    _, counts = np.unique(labels, return_counts=True)
    p = counts / counts.sum()
    return 1 - np.sum(p ** 2)

print("gini pure:", gini([1, 1, 1, 1]), "| gini 50/50:", gini([0, 1, 0, 1]))
X, y = make_moons(n_samples=400, noise=0.3, random_state=0)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)
for k in (1, 15, 151):
    knn = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=k)).fit(X_train, y_train)
    print(f"k={k:>3}: train {knn.score(X_train, y_train):.2f} test {knn.score(X_test, y_test):.2f}")
for depth in (2, 5, None):
    tree = DecisionTreeClassifier(max_depth=depth, random_state=0).fit(X_train, y_train)
    print(f"depth={depth}: train {tree.score(X_train, y_train):.2f} test {tree.score(X_test, y_test):.2f} leaves={tree.get_n_leaves()}")
small_tree = DecisionTreeClassifier(max_depth=2, random_state=0).fit(X_train, y_train)
print(export_text(small_tree, feature_names=["x1", "x2"]))

# EXPLANATION (LINE BY LINE):
# gini([1,1,1,1]) = 0 (pure); gini([0,1,0,1]) = 0.5 (maximally mixed for 2 classes).
# make_moons                     -> two interleaving half-circles: non-linear data.
# k=1   -> train 1.00: it memorises every training point (the train/test GAP of 0.10
#          is the overfitting signal, even though test accuracy is similar here).
# k=151 -> very smooth: training accuracy drops to 0.83 - heading toward underfitting.
# depth=None -> the tree grows until leaves are pure: overfits.
# depth=2/5  -> limited depth generalises better.
# export_text                    -> the learned rules as readable if/else text.
#
# COMMON MISTAKES:
# 1. Using k-NN without feature scaling.
# 2. Letting trees grow unlimited.
# 3. Reading feature_importances_ of one unstable tree as truth.
# 4. Using k-NN on large, high-dimensional data without approximate indexes.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Train a depth-3 decision tree on Iris, print its rules with export_text, and
# predict the species for two flowers you describe.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Implement k-NN classification from scratch (NumPy distances + majority vote)
# and compare accuracy with sklearn's KNeighborsClassifier on make_moons for
# k = 1, 5, 25. Plot test accuracy vs k.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Implement best_split(X, y) that tries every feature and threshold and
# returns the split with the largest Gini decrease. Use it to build a
# recursive decision tree (max_depth, min_samples) as nested dicts with a
# predict function. Compare with sklearn on make_moons.

# YOUR CODE:

