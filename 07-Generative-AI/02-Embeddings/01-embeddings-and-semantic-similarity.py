# ======================================
# TOPIC: TEXT EMBEDDINGS AND SEMANTIC SIMILARITY
# LEVEL: INTERMEDIATE
# ID: generative-ai.embeddings.semantic-similarity
# ======================================

# INTRODUCTION
# Embeddings turn text into vectors so that similar MEANINGS are close
# together. They power semantic search, RAG retrieval, deduplication,
# clustering and recommendations.
# (Maths: vectors, cosine similarity - 02-Mathematics/01-Linear-Algebra.)
#
# THEORY
# - An embedding model maps text -> fixed-size vector (e.g. 384-3072 dims).
#   Trained so paraphrases are close and unrelated texts are far apart.
# - Similarity: cosine similarity (or dot product of normalised vectors).
# - Sources: embedding APIs (e.g. Voyage AI - Anthropic's recommended
#   embeddings provider - OpenAI, Cohere) or open models
#   (sentence-transformers). Use the SAME model for documents and queries.
# - Keyword methods (TF-IDF, BM25) match exact words; embeddings match
#   meaning ("car" ~ "automobile"). Production search often combines both.
# - Practical concerns: embedding cost (one-off for documents), dimension vs
#   storage, re-embedding everything when you change models, multilingual
#   support, max input length per text.
# - Here we build a small LSA embedding (TF-IDF + SVD) offline to illustrate
#   the idea; real neural embeddings capture meaning much better.
#
# REAL-WORLD ANALOGY
# A map of a library where books on similar subjects are shelved near each
# other: finding related books means looking at the nearby shelves.
#
# SYNTAX:
#   vectors = embed(texts)   # (n, d)
#   scores = normalize(vectors) @ normalize(query_vector)
#
# SMALL WORKING EXAMPLE:
import numpy as np
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer

corpus = [
    "How do I reset my password?", "I forgot my login password", "Change account password steps",
    "What is your refund policy?", "Can I get my money back?", "Return an item for a refund",
    "Shipping takes how many days?", "When will my package arrive?", "Track my delivery status",
]
embedder = make_pipeline(TfidfVectorizer(), TruncatedSVD(n_components=3, random_state=0), Normalizer())
vectors = embedder.fit_transform(corpus)
print("embedding shape:", vectors.shape)

def search(query, k=3):
    q = embedder.transform([query])[0]
    scores = vectors @ q
    top = np.argsort(scores)[::-1][:k]
    return [(corpus[i], round(float(scores[i]), 3)) for i in top]

for query in ["refund money", "password reset help", "where is my parcel"]:
    print(query, "->", search(query))

# EXPLANATION (LINE BY LINE):
# corpus                     -> 9 short texts in 3 topics.
# TfidfVectorizer            -> sparse word-weight vectors.
# TruncatedSVD(3)            -> compresses to 3 "concept" dimensions (latent semantic
#                               analysis), grouping co-occurring words.
# Normalizer                 -> unit length, so dot product = cosine similarity.
# search()                   -> embed the query with the SAME pipeline, score all texts.
# "where is my parcel"       -> shares no words with the shipping texts: the top three
#                               scores TIE (0.68) between shipping and refund texts, so the
#                               "right" first result is luck. Neural embeddings fix exactly
#                               this (they know parcel ~ package ~ delivery).
#
# COMMON MISTAKES:
# 1. Using different models for queries and documents.
# 2. Comparing un-normalised vectors with the dot product.
# 3. Assuming embeddings capture negation or exact numbers well.
# 4. Forgetting to re-embed the corpus after changing the embedding model.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Add 6 sentences about a new topic (e.g. billing) and re-run search with 3
# queries. Which queries succeed and which fail, and why?

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Install sentence-transformers in the course venv, embed the same corpus with
# "all-MiniLM-L6-v2", and compare top-3 results with the LSA version for 5
# queries that use synonyms. Report where neural embeddings win.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Use embeddings to deduplicate 50 FAQ questions (find pairs above a cosine
# threshold), choose the threshold by labelling 20 pairs yourself and computing
# precision/recall at several thresholds.

# YOUR CODE:

