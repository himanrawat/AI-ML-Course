# ======================================
# TOPIC: THE TRANSFORMER BLOCK AND A TINY GPT
# LEVEL: ADVANCED
# ID: deep-learning.transformers.tiny-gpt
# ======================================

# INTRODUCTION
# GPT-style LLMs are stacks of identical transformer blocks trained to predict
# the next token. Building a tiny one demystifies what happens inside the
# models you will prompt and build applications with.
#
# THEORY
# A decoder-only transformer:
#  1. Token embedding + POSITIONAL embedding (attention itself has no notion
#     of order).
#  2. N BLOCKS, each:  x = x + Attention(LayerNorm(x))   (causal, multi-head)
#                      x = x + MLP(LayerNorm(x))         (Linear-GELU-Linear)
#     The "x + ..." are RESIDUAL connections - they keep gradients flowing in
#     deep stacks. LayerNorm stabilises activations.
#  3. Final LayerNorm + Linear to vocabulary size -> LOGITS for the next token.
# - Training: next-token prediction with cross-entropy, on all positions at once
#   (targets are the input shifted by one).
# - Generation: feed the prompt, take the logits of the LAST position, sample a
#   token (greedy, temperature, top-k/top-p), append it, repeat.
# - Real LLMs: same recipe at massive scale (billions of parameters, trillions
#   of tokens), then instruction tuning and preference tuning.
#
# REAL-WORLD ANALOGY
# An autocomplete that has read a library: each layer refines its
# understanding of the sentence so far, and the last layer guesses the next word.
#
# SYNTAX:
#   logits = model(ids)                 # (batch, seq, vocab)
#   loss = F.cross_entropy(logits.view(-1, vocab), targets.view(-1))
#
# SMALL WORKING EXAMPLE:
import torch
import torch.nn.functional as F
from torch import nn

torch.manual_seed(0)
text = "hello world. hello there. hello transformer world. " * 20
chars = sorted(set(text))
stoi = {c: i for i, c in enumerate(chars)}
data = torch.tensor([stoi[c] for c in text])
vocab_size, block_size, d_model = len(chars), 16, 48

class Block(nn.Module):
    def __init__(self):
        super().__init__()
        self.ln1, self.ln2 = nn.LayerNorm(d_model), nn.LayerNorm(d_model)
        self.attn = nn.MultiheadAttention(d_model, num_heads=4, batch_first=True)
        self.mlp = nn.Sequential(nn.Linear(d_model, 4 * d_model), nn.GELU(), nn.Linear(4 * d_model, d_model))

    def forward(self, x):
        T = x.size(1)
        mask = torch.triu(torch.ones(T, T, dtype=torch.bool), diagonal=1)
        h = self.ln1(x)
        x = x + self.attn(h, h, h, attn_mask=mask, need_weights=False)[0]
        return x + self.mlp(self.ln2(x))

class TinyGPT(nn.Module):
    def __init__(self):
        super().__init__()
        self.tok = nn.Embedding(vocab_size, d_model)
        self.pos = nn.Embedding(block_size, d_model)
        self.blocks = nn.Sequential(Block(), Block())
        self.ln = nn.LayerNorm(d_model)
        self.head = nn.Linear(d_model, vocab_size)

    def forward(self, ids):
        x = self.tok(ids) + self.pos(torch.arange(ids.size(1)))
        return self.head(self.ln(self.blocks(x)))

    @torch.no_grad()
    def generate(self, ids, steps, temperature=0.8):
        for _ in range(steps):
            logits = self(ids[:, -block_size:])[:, -1, :] / temperature
            next_id = torch.multinomial(F.softmax(logits, dim=-1), 1)
            ids = torch.cat([ids, next_id], dim=1)
        return ids

model = TinyGPT()
optimizer = torch.optim.AdamW(model.parameters(), lr=3e-3)
for step in range(300):
    starts = torch.randint(0, len(data) - block_size - 1, (32,))
    x = torch.stack([data[s:s + block_size] for s in starts])
    y = torch.stack([data[s + 1:s + block_size + 1] for s in starts])
    loss = F.cross_entropy(model(x).reshape(-1, vocab_size), y.reshape(-1))
    optimizer.zero_grad(); loss.backward(); optimizer.step()
    if step % 100 == 0 or step == 299:
        print(f"step {step:>3}: loss {loss.item():.3f}")
prompt = torch.tensor([[stoi[c] for c in "hello "]])
print("generated:", repr("".join(chars[i] for i in model.generate(prompt, 30)[0].tolist())))
print("parameters:", sum(p.numel() for p in model.parameters()))

# EXPLANATION (LINE BY LINE):
# Character-level "tokenizer": each character is a token (stoi = string to id).
# Block: pre-LayerNorm, causal multi-head attention, residual add, then MLP + residual.
# attn_mask=mask (True = blocked) -> each position sees only earlier positions.
# TinyGPT: token + position embeddings -> 2 blocks -> LayerNorm -> vocab logits.
# Training: random windows x, targets y = x shifted by one character.
# cross_entropy over every position at once (reshape to (batch*seq, vocab)).
# generate(): take the last position's logits, apply temperature, sample, append.
# After 300 steps the model produces text resembling its tiny training corpus.
#
# COMMON MISTAKES:
# 1. Forgetting positional information (the model can't tell order).
# 2. Off-by-one targets (y must be x shifted by one).
# 3. Feeding sequences longer than block_size to position embeddings.
# 4. Confusing training (all positions in parallel) with generation (one token
#    at a time).

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Generate text with temperature 0.2, 0.8 and 1.5 from the trained model and
# describe how the outputs differ.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Train TinyGPT on a longer text of your choice (a few paragraphs). Add a
# held-out validation split, report validation loss every 100 steps, and try
# 1 vs 4 blocks. Count parameters for each configuration.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Replace nn.MultiheadAttention with your own MultiHeadAttention from the
# self-attention topic, add dropout, implement top-k and top-p (nucleus)
# sampling in generate(), and plot the attention weights of one head for a
# generated sequence.

# YOUR CODE:

