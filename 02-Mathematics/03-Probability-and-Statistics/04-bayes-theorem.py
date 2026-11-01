# ======================================
# TOPIC: BAYES' THEOREM
# LEVEL: INTERMEDIATE
# ID: math.probability.bayes
# ======================================

# INTRODUCTION
# Bayes' theorem updates beliefs with evidence. It powers Naive Bayes spam
# filters, explains why rare-event detectors raise false alarms, and is the
# foundation of probabilistic ML. (Study with 04-Machine-Learning classification.)
#
# THEORY
# P(A | B) = P(B | A) * P(A) / P(B)
# - P(A): PRIOR - belief before evidence.
# - P(B | A): LIKELIHOOD - how likely the evidence is if A is true.
# - P(B): EVIDENCE - overall probability of the evidence:
#   P(B) = P(B | A) P(A) + P(B | not A) P(not A).
# - P(A | B): POSTERIOR - updated belief.
# - BASE RATE FALLACY: with a rare condition, even an accurate test produces
#   mostly false positives.
# - NAIVE BAYES assumes features are independent given the class:
#   P(class | words) proportional to P(class) * product of P(word | class).
#   Use log probabilities to avoid underflow, and Laplace smoothing (+1)
#   for unseen words.
#
# REAL-WORLD ANALOGY
# A detective: starts with suspicion levels (priors), finds a clue (evidence),
# and updates suspicion based on how well each suspect explains the clue.
#
# SYNTAX:
#   posterior = likelihood * prior / evidence
#
# SMALL WORKING EXAMPLE:
import math
from collections import Counter

prevalence = 0.01
sensitivity = 0.99
false_positive_rate = 0.05
p_positive = sensitivity * prevalence + false_positive_rate * (1 - prevalence)
p_disease_given_positive = sensitivity * prevalence / p_positive
print(f"P(disease | positive test) = {p_disease_given_positive:.3f}")

train = [
    ("win money now", "spam"), ("free prize win", "spam"), ("cheap money offer", "spam"),
    ("meeting at noon", "ham"), ("project update attached", "ham"), ("lunch money tomorrow", "ham"),
]
classes = Counter(label for _, label in train)
word_counts = {c: Counter() for c in classes}
for text, label in train:
    word_counts[label].update(text.split())
vocab = {w for counts in word_counts.values() for w in counts}

def predict(text):
    scores = {}
    for c in classes:
        log_prob = math.log(classes[c] / len(train))
        total = sum(word_counts[c].values())
        for word in text.split():
            log_prob += math.log((word_counts[c][word] + 1) / (total + len(vocab)))
        scores[c] = log_prob
    return max(scores, key=scores.get), {c: round(s, 2) for c, s in scores.items()}

print(predict("win free money"))
print(predict("project meeting tomorrow"))

# EXPLANATION (LINE BY LINE):
# prevalence 1%, test catches 99% of cases, 5% false positives.
# p_positive -> total probability of a positive test (true + false positives).
# posterior ~ 0.167 -> only 1 in 6 positives is real: the base rate fallacy.
# Naive Bayes: classes = prior counts; word_counts per class = likelihoods.
# log_prob starts with log P(class), then adds log P(word | class) per word.
# (count + 1) / (total + |vocab|) -> Laplace smoothing; unseen words don't zero out.
# max(scores, key=scores.get) -> class with the highest posterior score.
#
# COMMON MISTAKES:
# 1. Ignoring the prior (base rate).
# 2. Multiplying many small probabilities -> underflow to 0 (use logs).
# 3. No smoothing -> one unseen word makes a class impossible.
# 4. Treating Naive Bayes scores as calibrated probabilities.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# 30% of emails are spam. "Offer" appears in 60% of spam and 5% of normal
# emails. Compute P(spam | "offer") by hand and in code.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Plot how P(disease | positive) changes as prevalence goes from 0.1% to 50%
# for a test with 95% sensitivity and 95% specificity. Comment on the result.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Extend the Naive Bayes classifier into a class with fit(texts, labels) and
# predict_proba(text) that returns normalized probabilities (use the
# log-sum-exp trick). Train on 20 labelled sentences across 3 classes,
# evaluate on 6 held-out sentences, and compare with sklearn's MultinomialNB
# + CountVectorizer.

# YOUR CODE:

