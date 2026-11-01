# ======================================
# TOPIC: PROBABILITY BASICS
# LEVEL: BEGINNER
# ID: math.probability.basics
# ======================================

# INTRODUCTION
# Classifiers output probabilities ("92% spam"), and language models choose
# the next token from a probability distribution. Probability is the
# language of uncertainty.
#
# THEORY
# - Probability P(A) is a number in [0, 1]. All outcomes sum to 1.
# - Complement: P(not A) = 1 - P(A).
# - Joint probability P(A and B). If A and B are INDEPENDENT: P(A)P(B).
# - Union: P(A or B) = P(A) + P(B) - P(A and B).
# - CONDITIONAL probability P(A | B) = P(A and B) / P(B): probability of A
#   given that B happened.
# - Random variables and EXPECTED VALUE: E[X] = sum(x * P(x)).
# - Law of large numbers: averages of many random trials approach the
#   expected value - so we can estimate probabilities by simulation.
#
# REAL-WORLD ANALOGY
# Weather forecasts: "70% chance of rain" means that across many days like
# this one, it rains on about 7 out of 10.
#
# SYNTAX:
#   rng = np.random.default_rng(seed)
#   rng.random(n) < p       # simulate n events with probability p
#   rng.choice(options, p=probs)
#
# SMALL WORKING EXAMPLE:
import numpy as np

rng = np.random.default_rng(0)
rolls = rng.integers(1, 7, size=100_000)
print("P(six) ~", round(np.mean(rolls == 6), 4), "exact", round(1 / 6, 4))
print("E[roll] ~", round(rolls.mean(), 3), "exact 3.5")
die1, die2 = rng.integers(1, 7, size=(2, 100_000))
both_six = np.mean((die1 == 6) & (die2 == 6))
print("P(both six) ~", round(both_six, 4), "exact", round(1 / 36, 4))
total = die1 + die2
given_first_six = total[die1 == 6]
print("P(total >= 10 | first is 6) ~", round(np.mean(given_first_six >= 10), 3), "exact 0.5")
tokens = ["the", "a", "cat", "dog"]
probs = [0.5, 0.3, 0.15, 0.05]
samples = rng.choice(tokens, size=10_000, p=probs)
values, counts = np.unique(samples, return_counts=True)
print(dict(zip(values.tolist(), (counts / counts.sum()).round(3).tolist())))

# EXPLANATION (LINE BY LINE):
# rng.integers(1, 7, size=100_000)  -> 100k simulated dice rolls (7 excluded).
# np.mean(rolls == 6)               -> fraction of sixes ~ 1/6 (law of large numbers).
# rolls.mean()                      -> close to the expected value 3.5.
# (die1 == 6) & (die2 == 6)         -> joint event for two independent dice: 1/36.
# total[die1 == 6]                  -> keep only rolls where the first die is 6
#                                      (conditioning = restricting the sample).
# P(total >= 10 | first is 6)       -> second die must be 4, 5 or 6 -> 0.5.
# rng.choice(tokens, p=probs)       -> sampling the "next token" from a distribution.
#
# COMMON MISTAKES:
# 1. Multiplying probabilities of events that are NOT independent.
# 2. Confusing P(A | B) with P(B | A).
# 3. Forgetting to subtract the overlap in P(A or B).
# 4. Trusting simulations with too few trials.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# A bag has 5 red, 3 blue and 2 green balls. Compute (by hand and by
# simulation) P(red), P(not green), and P(two reds in a row without replacement).

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Simulate the birthday problem: for group sizes 5..60, estimate the
# probability that at least two people share a birthday. Find the smallest
# group size where it exceeds 50%, and compare with the exact formula.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Given a table of 1,000 emails with columns (contains_free, is_spam) that you
# simulate with known probabilities, estimate P(spam), P(free | spam),
# P(free | not spam) and P(spam | free) from counts. Check your estimate of
# P(spam | free) against Bayes' theorem.

# YOUR CODE:

