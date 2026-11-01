# ======================================
# TOPIC: SEQUENCES, EMBEDDINGS AND RECURRENT NETWORKS
# LEVEL: ADVANCED
# ID: deep-learning.architectures.sequences-embeddings
# ======================================

# INTRODUCTION
# Text is a sequence of discrete tokens. To feed it to a network, each token
# becomes a learned vector - an EMBEDDING. Recurrent networks were the first
# successful sequence models and explain why transformers replaced them.
#
# THEORY
# - Token ids are integers; one-hot vectors would be huge and carry no
#   meaning. nn.Embedding(vocab_size, dim) is a learnable lookup table:
#   id -> dense vector. Training moves similar words close together.
# - Sentence representation: average (mean-pool) the token embeddings, or
#   process them in order.
# - RNN: reads one token at a time, keeping a hidden state
#   h_t = tanh(W x_t + U h_(t-1) + b). Problems: sequential (slow, no
#   parallelism) and long-range memory fades (vanishing gradients).
# - LSTM/GRU add gates that control what to keep or forget.
# - Padding: batch sequences to the same length with a PAD id and ignore it.
# - Transformers (next section) replace recurrence with attention, processing
#   all positions in parallel.
#
# REAL-WORLD ANALOGY
# An embedding is a map of a city where similar shops are placed near each
# other. An RNN is someone reading a novel one word at a time, keeping notes
# in a small notebook that fills up and fades.
#
# SYNTAX:
#   emb = nn.Embedding(vocab_size, 16, padding_idx=0)
#   rnn = nn.GRU(16, 32, batch_first=True); outputs, h = rnn(emb(ids))
#
# SMALL WORKING EXAMPLE:
import torch
import torch.nn.functional as F
from torch import nn

torch.manual_seed(0)
texts = ["great movie loved it", "terrible plot boring", "loved the acting", "boring and terrible",
         "great acting great story", "awful boring film", "wonderful loved story", "terrible awful acting"]
labels = torch.tensor([1, 0, 1, 0, 1, 0, 1, 0])
vocab = {"<pad>": 0}
for text in texts:
    for word in text.split():
        vocab.setdefault(word, len(vocab))

def encode(text, length=5):
    ids = [vocab.get(w, 0) for w in text.split()][:length]
    return ids + [0] * (length - len(ids))

ids = torch.tensor([encode(t) for t in texts])
print("vocab size:", len(vocab), "| batch shape:", ids.shape)

class GRUClassifier(nn.Module):
    def __init__(self, vocab_size, dim=16, hidden=32):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, dim, padding_idx=0)
        self.gru = nn.GRU(dim, hidden, batch_first=True)
        self.head = nn.Linear(hidden, 2)

    def forward(self, x):
        _, last_hidden = self.gru(self.embedding(x))
        return self.head(last_hidden[-1])

model = GRUClassifier(len(vocab))
optimizer = torch.optim.Adam(model.parameters(), lr=0.02)
for step in range(150):
    optimizer.zero_grad()
    loss = F.cross_entropy(model(ids), labels)
    loss.backward()
    optimizer.step()
print("final loss:", round(loss.item(), 4))
test = torch.tensor([encode("loved this great film"), encode("awful and boring")])
print("predictions (1 = positive):", model(test).argmax(1).tolist())
E = model.embedding.weight.detach()
sim = lambda a, b: F.cosine_similarity(E[vocab[a]], E[vocab[b]], dim=0).item()
print(f"sim(great, loved)={sim('great', 'loved'):.2f}  sim(great, terrible)={sim('great', 'terrible'):.2f}")

# EXPLANATION (LINE BY LINE):
# vocab maps each word to an id; 0 is reserved for padding.
# encode(...)                    -> fixed length 5, padded with 0.
# nn.Embedding(..., padding_idx=0) -> learnable vectors; the pad vector stays 0.
# nn.GRU(batch_first=True)       -> input (batch, seq, dim); returns the last hidden state.
# head on last_hidden[-1]        -> classify the whole sequence.
# After training, words used in the same sentiment tend to get more similar
# embeddings than words of opposite sentiment (tiny data -> noisy, but visible).
#
# COMMON MISTAKES:
# 1. Forgetting padding_idx / masks so padding influences the result.
# 2. Mixing batch_first conventions.
# 3. Unknown words at test time (we map them to 0 here; real systems use
#    subword tokenization).
# 4. Expecting meaningful embeddings from tiny datasets.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Create an nn.Embedding(10, 4), look up ids [1, 2, 1], and show that the same
# id returns the same vector. Print the embedding table's shape and
# parameter count.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Replace the GRU with a mean-pooled embedding classifier (average non-pad
# embeddings, then Linear). Compare accuracy on 6 new sentences you write and
# explain what word-order information is lost.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Implement a vanilla RNN cell by hand (h = tanh(x W + h U + b)) and run it over
# sequences of length 5, 20 and 50. Backpropagate from the final hidden state
# and plot the gradient norm with respect to each time step's input to show
# vanishing gradients. Repeat with nn.LSTM and compare.

# YOUR CODE:

