# ======================================
# TOPIC: SELF-ATTENTION
# LEVEL: ADVANCED
# ID: deep-learning.transformers.self-attention
# ======================================

# INTRODUCTION
# Attention is the mechanism at the heart of transformers and therefore of
# every modern LLM. It lets each token look at every other token and decide
# which ones matter for its meaning.
# (Maths: dot products, matrix multiplication, softmax.)
#
# THEORY
# - Each token embedding x is projected into three vectors:
#   QUERY q = x Wq ("what am I looking for?"), KEY k = x Wk ("what do I
#   contain?"), VALUE v = x Wv ("what information do I pass on?").
# - Attention weights: scores = Q K^T / sqrt(d_k); weights = softmax(scores)
#   along each row. Output = weights @ V: each token's new vector is a
#   weighted mix of all value vectors.
# - Dividing by sqrt(d_k) keeps scores from growing with dimension (which
#   would make softmax too peaky).
# - CAUSAL MASK: in GPT-style (decoder) models a token may only attend to
#   itself and EARLIER tokens - future positions get -infinity before softmax.
# - MULTI-HEAD attention runs several attention operations in parallel with
#   different projections, each free to focus on different relationships.
# - Cost grows with the SQUARE of the sequence length - a key reason context
#   windows are expensive.
#
# REAL-WORLD ANALOGY
# In a meeting, each person (token) has a question (query). Everyone wears a
# name badge describing their expertise (key). You listen most to people whose
# badges match your question and take notes on what they say (values).
#
# SYNTAX:
#   weights = softmax(Q @ K.T / sqrt(d_k) + mask); output = weights @ V
#
# SMALL WORKING EXAMPLE:
import math

import torch
import torch.nn.functional as F

torch.manual_seed(0)
tokens = ["the", "cat", "sat", "on", "mat"]
seq_len, d_model, d_k = len(tokens), 8, 4
x = torch.randn(seq_len, d_model)
Wq, Wk, Wv = (torch.randn(d_model, d_k) for _ in range(3))
Q, K, V = x @ Wq, x @ Wk, x @ Wv
scores = Q @ K.T / math.sqrt(d_k)
causal_mask = torch.triu(torch.ones(seq_len, seq_len), diagonal=1).bool()
scores = scores.masked_fill(causal_mask, float("-inf"))
weights = F.softmax(scores, dim=-1)
output = weights @ V
print("attention weights (rows = query token):")
print("      " + " ".join(f"{t:>5}" for t in tokens))
for token, row in zip(tokens, weights):
    print(f"{token:>5} " + " ".join(f"{w:5.2f}" for w in row.tolist()))
print("output shape:", tuple(output.shape))
reference = F.scaled_dot_product_attention(Q[None], K[None], V[None], is_causal=True)[0]
print("matches PyTorch's built-in:", torch.allclose(output, reference, atol=1e-5))

# EXPLANATION (LINE BY LINE):
# x: 5 tokens, each an 8-dimensional embedding (random here; learned in practice).
# Q, K, V = x @ Wq, x @ Wk, x @ Wv -> three learned projections to 4 dimensions.
# Q @ K.T / sqrt(d_k)          -> (5, 5) similarity score of every query with every key.
# torch.triu(..., diagonal=1)  -> True above the diagonal = future positions.
# masked_fill(-inf)            -> softmax gives those positions weight 0.
# softmax(dim=-1)              -> each row sums to 1.
# Row "the" attends only to itself; row "mat" can attend to all 5 tokens.
# weights @ V                  -> each token's output mixes the values it attends to.
# F.scaled_dot_product_attention -> PyTorch's optimised version gives the same result.
#
# COMMON MISTAKES:
# 1. Softmax over the wrong dimension (columns instead of rows).
# 2. Forgetting the causal mask in a generative model (it can "see the future").
# 3. Forgetting the 1/sqrt(d_k) scaling.
# 4. Believing attention weights fully explain model decisions.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Remove the causal mask and print the weights again. Verify every row sums to
# 1 in both versions, and explain which version an LLM uses during generation.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Show why scaling matters: for d_k = 4, 64 and 512, compute softmax over
# random q.k scores with and without dividing by sqrt(d_k), and report the
# maximum weight (how "peaky" the distribution is).

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Implement MultiHeadAttention(d_model, n_heads) as an nn.Module: one Linear
# for Q, K, V, split into heads with view/transpose, attention per head with a
# causal mask, concatenate, and an output Linear. Check shapes for a batch of
# (2, 10, 32) and compare outputs with torch.nn.MultiheadAttention given the
# same weights.

# YOUR CODE:

