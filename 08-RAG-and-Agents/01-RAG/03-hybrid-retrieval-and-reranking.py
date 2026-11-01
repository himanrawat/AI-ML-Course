# ======================================
# TOPIC: HYBRID RETRIEVAL AND RERANKING
# LEVEL: ADVANCED
# ID: rag-agents.rag.hybrid-reranking
# ======================================

# INTRODUCTION
# Vector search finds meaning but can miss exact terms (error codes, product
# names, ids). Keyword search finds exact terms but misses paraphrases.
# Production RAG combines both, then re-ranks the best candidates.
#
# THEORY
# - BM25: classic keyword ranking (term frequency, inverse document frequency,
#   length normalisation). Great for exact tokens like "ERR-4012".
# - DENSE retrieval: embeddings for semantic similarity.
# - HYBRID: run both, merge rankings. RECIPROCAL RANK FUSION (RRF):
#   score(doc) = sum over rankers of 1 / (k + rank), k ~ 60. Robust because it
#   uses ranks, not incomparable raw scores.
# - RERANKING: retrieve many candidates cheaply (top 20-50), then score each
#   (query, chunk) pair with a more accurate model (cross-encoder or an LLM)
#   and keep the top few.
# - QUERY TRANSFORMATION: rewrite vague queries, expand acronyms, split
#   multi-part questions before retrieval.
#
# REAL-WORLD ANALOGY
# Hiring: a keyword filter and a recruiter's judgement each shortlist
# candidates; merge the shortlists, then a senior interviewer (re-ranker)
# interviews only the top few.
#
# SYNTAX:
#   fused = rrf([bm25_ranking, dense_ranking]); final = rerank(query, fused[:20])[:5]
#
# SMALL WORKING EXAMPLE:
import math
import re
from collections import Counter

DOCS = [
    "Error ERR-4012 means the payment gateway timed out; retry after 30 seconds.",
    "If a payment fails, check your card details and try again later.",
    "Timeouts can happen when the network is slow or the server is overloaded.",
    "To update billing details, open Settings and choose Payment methods.",
    "ERR-2201 indicates an invalid coupon code.",
]
tokenize = lambda text: re.findall(r"[a-z0-9-]+", text.lower())
tokenized = [tokenize(d) for d in DOCS]
avg_len = sum(map(len, tokenized)) / len(tokenized)

def bm25_rank(query, k1=1.5, b=0.75):
    n = len(DOCS)
    scores = []
    for i, tokens in enumerate(tokenized):
        tf = Counter(tokens)
        score = 0.0
        for term in tokenize(query):
            df = sum(term in t for t in tokenized)
            if df:
                idf = math.log(1 + (n - df + 0.5) / (df + 0.5))
                score += idf * tf[term] * (k1 + 1) / (tf[term] + k1 * (1 - b + b * len(tokens) / avg_len))
        scores.append(score)
    return sorted(range(n), key=lambda i: -scores[i])

SYNONYMS = {"failed": "fails", "payment": "payment", "timeout": "timed", "slow": "timeouts"}
def dense_rank(query):
    expanded = set(tokenize(query)) | {SYNONYMS.get(t, t) for t in tokenize(query)}
    overlap = [len(expanded & set(t)) / math.sqrt(len(t)) for t in tokenized]
    return sorted(range(len(DOCS)), key=lambda i: -overlap[i])

def rrf(rankings, k=60):
    scores = Counter()
    for ranking in rankings:
        for rank, doc in enumerate(ranking, start=1):
            scores[doc] += 1 / (k + rank)
    return [doc for doc, _ in scores.most_common()]

query = "my payment failed with ERR-4012 timeout"
for name, ranking in [("bm25", bm25_rank(query)), ("dense*", dense_rank(query)),
                      ("hybrid RRF", rrf([bm25_rank(query), dense_rank(query)]))]:
    print(f"{name:<11} top-3: {ranking[:3]}")
print("best match:", DOCS[rrf([bm25_rank(query), dense_rank(query)])[0]])

# EXPLANATION (LINE BY LINE):
# bm25_rank                  -> full BM25 formula: rare terms (ERR-4012) get a high idf.
# dense_rank (*)             -> a toy stand-in for embedding similarity using synonyms;
#                               swap in real embeddings from 07-Generative-AI.
# rrf                        -> each ranker contributes 1/(k + rank); documents ranked
#                               well by BOTH rise to the top.
# Here both rankers agree on the exact error-code document (doc 0), so fusion keeps it
# first. Further down they disagree (doc 3 vs doc 1) and RRF blends the two orders.
# With real embeddings the rankers disagree more often, which is when fusion pays off.
#
# COMMON MISTAKES:
# 1. Adding raw BM25 and cosine scores (different scales) instead of fusing ranks.
# 2. Re-ranking too few candidates (the right chunk was never retrieved).
# 3. Using only dense retrieval for queries full of ids and codes.
# 4. Skipping evaluation of each component.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Run 4 different queries (one with only an error code, one paraphrase, one
# mixed, one vague) and compare the three rankings. Which ranker wins each?

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Write an LLM re-ranker prompt that scores (query, chunk) relevance 0-3 in JSON
# for the top 5 fused candidates, with a mocked complete() offline. Re-order by
# score and explain when re-ranking is worth its latency.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Build a 30-document corpus and 15 labelled queries. Compute recall@3 and MRR
# for BM25, dense (real embeddings), RRF hybrid and hybrid + re-ranking.
# Present the results as a table and recommend a configuration.

# YOUR CODE:

