# ======================================
# TOPIC: TOKENIZATION
# LEVEL: INTERMEDIATE
# ID: deep-learning.transformers.tokenization
# ======================================

# INTRODUCTION
# LLMs never see letters or words - they see TOKENS. Tokenization explains
# pricing (you pay per token), context limits, why models struggle to count
# letters, and why some languages cost more than others.
#
# THEORY
# - A tokenizer splits text into tokens from a fixed VOCABULARY and maps each
#   to an integer id. The model predicts ids; the tokenizer decodes them back.
# - Word-level: huge vocabulary, unknown words. Character-level: tiny
#   vocabulary, very long sequences.
# - SUBWORD tokenization (BPE - byte pair encoding, WordPiece, Unigram) is
#   the standard: frequent words are single tokens; rare words split into
#   pieces ("tokenization" -> "token" + "ization").
# - BPE training: start from characters (or bytes); repeatedly MERGE the most
#   frequent adjacent pair into a new token until the vocabulary is full.
# - Byte-level BPE can encode ANY text, emoji included.
# - Rough rule for English: 1 token ~ 4 characters ~ 0.75 words. Other
#   languages and code often need more tokens per word.
# - Each model family has its own tokenizer - counts differ between models.
#
# REAL-WORLD ANALOGY
# Text messages with abbreviations: common phrases get short codes ("brb"),
# rare words are spelled out piece by piece.
#
# SYNTAX:
#   see the BPE implementation below
#
# SMALL WORKING EXAMPLE:
from collections import Counter

corpus = "low lower lowest newer newest wider widest low low newer".split()

def train_bpe(words, num_merges):
    vocab = Counter(tuple(word) + ("</w>",) for word in words)
    merges = []
    for _ in range(num_merges):
        pairs = Counter()
        for symbols, freq in vocab.items():
            for pair in zip(symbols, symbols[1:]):
                pairs[pair] += freq
        if not pairs:
            break
        best = max(pairs, key=pairs.get)
        merges.append(best)
        new_vocab = Counter()
        for symbols, freq in vocab.items():
            merged, i = [], 0
            while i < len(symbols):
                if i < len(symbols) - 1 and (symbols[i], symbols[i + 1]) == best:
                    merged.append(symbols[i] + symbols[i + 1]); i += 2
                else:
                    merged.append(symbols[i]); i += 1
            new_vocab[tuple(merged)] += freq
        vocab = new_vocab
    return merges

def tokenize(word, merges):
    symbols = list(word) + ["</w>"]
    for a, b in merges:
        i = 0
        while i < len(symbols) - 1:
            if symbols[i] == a and symbols[i + 1] == b:
                symbols[i:i + 2] = [a + b]
            else:
                i += 1
    return symbols

merges = train_bpe(corpus, 10)
print("first merges:", merges[:5])
for word in ["lowest", "newest", "slowest", "xyz"]:
    print(f"{word:<8} -> {tokenize(word, merges)}")
text = "Tokenization affects cost and context length."
print("chars:", len(text), "| words:", len(text.split()), "| ~tokens (chars/4):", round(len(text) / 4))

# EXPLANATION (LINE BY LINE):
# corpus                      -> tiny training text with shared word parts.
# vocab = Counter(word as tuple of characters + end-of-word marker).
# Each loop: count adjacent symbol pairs (weighted by word frequency), merge
#   the most frequent pair everywhere, remember the merge.
# tokenize(word, merges)      -> apply learned merges IN ORDER to a new word.
# "slowest" was never seen, but it splits into known pieces ("s" + "lowest"-parts).
# "xyz" stays as characters: rare text costs more tokens.
# chars / 4                   -> the common rough estimate for English.
#
# COMMON MISTAKES:
# 1. Estimating cost by words instead of tokens.
# 2. Assuming every model uses the same tokenizer.
# 3. Expecting reliable character-level tasks (counting letters) from LLMs.
# 4. Forgetting that whitespace and capitalisation change tokenization.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Apply the trained BPE to 5 new words of your choice and count tokens per
# word. Which words are cheapest and why?

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Train the BPE on a larger English paragraph (100+ words) with 50 merges, then
# compare tokens-per-word on an English sentence vs the same sentence in
# another language or in code. Explain the difference.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Turn the BPE into a Tokenizer class with train(), encode(text) -> list of
# ids, decode(ids) -> text (exact round trip, including spaces), and a vocab
# file saved as JSON. Test the round trip on 20 sentences.

# YOUR CODE:

