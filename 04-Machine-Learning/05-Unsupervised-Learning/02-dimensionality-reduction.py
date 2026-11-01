# ======================================
# TOPIC: DIMENSIONALITY REDUCTION (PCA AND VISUALISING EMBEDDINGS)
# LEVEL: ADVANCED
# ID: ml.unsupervised.dimensionality-reduction
# ======================================

# INTRODUCTION
# Embeddings have hundreds of dimensions; images have thousands of pixels.
# Dimensionality reduction compresses data, removes noise, speeds up models
# and lets you SEE high-dimensional data in 2D.
# (Maths: 02-Mathematics/01-Linear-Algebra/05-eigenvectors-and-pca-intuition.)
#
# THEORY
# - PCA finds orthogonal directions of maximum variance; keep the top k.
#   explained_variance_ratio_ tells how much information each keeps.
#   Choose k to keep e.g. 95% of variance: PCA(n_components=0.95).
# - PCA is LINEAR and preserves global structure; scale features first.
# - t-SNE and UMAP are NON-LINEAR methods for VISUALISATION: they preserve
#   local neighbourhoods (similar points stay together) but distances between
#   far-apart clusters and cluster sizes are not meaningful.
# - The "curse of dimensionality": in high dimensions points become far apart
#   and distances less informative - reduction can help models.
#
# REAL-WORLD ANALOGY
# A shadow puppet: a 3D hand becomes a 2D shadow. Choose the light's angle
# well and the shadow still clearly shows a bird.
#
# SYNTAX:
#   PCA(n_components=2).fit_transform(X_scaled)
#   TSNE(n_components=2, perplexity=30).fit_transform(X)
#
# SMALL WORKING EXAMPLE:
import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import load_digits
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.manifold import TSNE
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

X, y = load_digits(return_X_y=True)
print("original shape:", X.shape)
pca = PCA().fit(StandardScaler().fit_transform(X))
cumulative = np.cumsum(pca.explained_variance_ratio_)
print("components for 80% / 95% variance:", int(np.argmax(cumulative >= 0.8)) + 1,
      "/", int(np.argmax(cumulative >= 0.95)) + 1)
for k in (5, 20, 40):
    model = make_pipeline(StandardScaler(), PCA(n_components=k), LogisticRegression(max_iter=2000))
    print(f"PCA {k:>2} components -> CV accuracy {cross_val_score(model, X, y, cv=3).mean():.3f}")
X_pca = PCA(n_components=2).fit_transform(StandardScaler().fit_transform(X))
X_tsne = TSNE(n_components=2, perplexity=30, random_state=0).fit_transform(X[:600])
fig, axes = plt.subplots(1, 2, figsize=(11, 5))
axes[0].scatter(X_pca[:, 0], X_pca[:, 1], c=y, cmap="tab10", s=6)
axes[0].set_title("PCA (linear)")
points = axes[1].scatter(X_tsne[:, 0], X_tsne[:, 1], c=y[:600], cmap="tab10", s=6)
axes[1].set_title("t-SNE (non-linear, visualisation only)")
fig.colorbar(points, ax=axes[1], label="digit")
fig.tight_layout()
plt.show()

# EXPLANATION (LINE BY LINE):
# load_digits                   -> 8x8 images = 64 features per sample.
# PCA().fit(...)                -> all components; cumulative explained variance.
# argmax(cumulative >= 0.95)+1  -> fewest components keeping 95% of variance.
# PCA inside a pipeline         -> accuracy with 20-40 components is close to all 64.
# 2D PCA scatter                -> digit classes overlap: linear projection is limited.
# t-SNE scatter                 -> clear digit clusters (local structure preserved).
#
# COMMON MISTAKES:
# 1. Forgetting to scale before PCA.
# 2. Interpreting t-SNE cluster sizes or distances between clusters.
# 3. Using t-SNE output as model features (it has no transform for new data).
# 4. Fitting PCA on all data before cross-validation (leakage).

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Apply PCA to the scaled Iris data, print explained_variance_ratio_, and plot
# the first two components coloured by species.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Use PCA to compress and reconstruct digits images with 5, 15 and 40
# components (inverse_transform). Show originals vs reconstructions in a grid
# and report the mean reconstruction error.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Create "sentence embeddings" with TfidfVectorizer for 30 sentences on 3
# topics, reduce with TruncatedSVD to 2D (PCA for sparse data), plot them
# coloured by topic, and cluster them with k-means. Report how well clusters
# match topics (adjusted_rand_score).

# YOUR CODE:

