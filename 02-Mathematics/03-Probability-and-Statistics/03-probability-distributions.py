# ======================================
# TOPIC: PROBABILITY DISTRIBUTIONS
# LEVEL: INTERMEDIATE
# ID: math.probability.distributions
# ======================================

# INTRODUCTION
# Weights are initialised from distributions, noise is modelled with them,
# and classifiers output them. Knowing the common shapes helps you choose
# models, losses and sanity checks.
#
# THEORY
# Discrete:
# - BERNOULLI(p): one yes/no trial (spam or not).
# - BINOMIAL(n, p): number of successes in n trials.
# - CATEGORICAL: one of K classes with probabilities (softmax output, next token).
# - POISSON(lambda): count of events in an interval (requests per minute).
# Continuous:
# - UNIFORM(a, b): every value equally likely.
# - NORMAL / GAUSSIAN(mu, sigma): bell curve; ~68% within 1 sigma, ~95% within
#   2 sigma, ~99.7% within 3 sigma.
# - EXPONENTIAL: waiting times.
# - CENTRAL LIMIT THEOREM: averages of many independent samples are
#   approximately normal, whatever the original distribution.
# - SOFTMAX turns any vector of scores into a categorical distribution:
#   softmax(z)_i = exp(z_i) / sum(exp(z_j)).
#
# REAL-WORLD ANALOGY
# Heights of adults cluster around an average with fewer very tall or very
# short people (normal); the number of customers per minute at a shop varies
# around a typical rate (Poisson).
#
# SYNTAX:
#   rng.normal(mu, sigma, size), rng.binomial(n, p, size),
#   rng.poisson(lam, size), rng.uniform(a, b, size)
#
# SMALL WORKING EXAMPLE:
import numpy as np

rng = np.random.default_rng(3)
heights = rng.normal(170, 10, size=100_000)
within = [np.mean(np.abs(heights - 170) < k * 10) for k in (1, 2, 3)]
print("within 1/2/3 sigma:", np.round(within, 3))
print("binomial(10, 0.5) mean:", rng.binomial(10, 0.5, size=10_000).mean())
print("poisson(4) mean, var:", np.round([rng.poisson(4, 10_000).mean(), rng.poisson(4, 10_000).var()], 2))
skewed = rng.exponential(1.0, size=(10_000, 50))
means = skewed.mean(axis=1)
print("CLT: mean of means", round(means.mean(), 3), "std", round(means.std(), 3), "expected std", round(1 / np.sqrt(50), 3))

def softmax(z):
    z = z - np.max(z)
    e = np.exp(z)
    return e / e.sum()

logits = np.array([2.0, 1.0, 0.1])
print("softmax:", softmax(logits).round(3), "sum:", softmax(logits).sum())
print("stable for huge logits:", softmax(np.array([1000.0, 999.0])).round(3))

# EXPLANATION (LINE BY LINE):
# rng.normal(170, 10, ...)     -> simulated heights; the 68-95-99.7 rule holds.
# binomial(10, 0.5) mean ~ 5   -> n * p.
# Poisson: mean and variance both ~ lambda = 4.
# exponential data is skewed, but the means of 50 samples are ~normal
#   with std ~ sigma / sqrt(n) (central limit theorem).
# softmax subtracts max(z) first -> avoids overflow in exp for large logits.
# softmax output sums to 1     -> a valid probability distribution.
#
# COMMON MISTAKES:
# 1. Assuming all data is normal (incomes, counts and latencies are usually not).
# 2. Implementing softmax without subtracting the max (overflow -> nan).
# 3. Confusing the standard deviation of data with the std of the mean.
# 4. Using the wrong distribution for counts (normal instead of Poisson).

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Simulate 10,000 coin flips (Bernoulli 0.5) and 10,000 values from
# uniform(0, 1). Print their means and plot both histograms.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Plot the probability mass function of Binomial(20, p) for p = 0.2, 0.5, 0.8
# (use np.bincount on simulations or the exact formula with math.comb).
# Mark the mean of each.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Implement temperature sampling: softmax(logits / T). For logits of 6 tokens,
# show the distribution for T = 0.2, 0.7, 1.0, 2.0, sample 1,000 tokens at each
# T, and compute the entropy of each distribution. Explain how temperature
# changes model output.

# YOUR CODE:

