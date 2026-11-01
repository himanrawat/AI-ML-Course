# ======================================
# TOPIC: PROMPT VERSIONING AND A/B TESTING
# LEVEL: ADVANCED
# ID: prompt-engineering.evaluation.versioning-ab
# ======================================

# INTRODUCTION
# In production, prompts change often and affect real users. You need to know
# which prompt version produced each output, roll back bad changes, and prove
# that a new version is actually better with real traffic.
#
# THEORY
# VERSIONING:
# - Treat prompts as code: store them in version control with semantic
#   versions (MAJOR.MINOR.PATCH), a changelog, an owner, and the model +
#   settings they were tested with.
# - Log the prompt version (and model) with every request.
# - Changes go through: eval set (offline) -> review -> staged rollout.
# - Changing the MODEL is also a version change - re-run evals.
# A/B TESTING (online experiments):
# - Randomly assign users (consistently, e.g. by hashing user id) to variant A
#   or B; measure a predefined metric (resolution rate, thumbs-up rate,
#   conversion, escalation rate).
# - Decide sample size and success metric BEFORE starting; check statistical
#   significance (two-proportion z-test); watch guardrail metrics (cost,
#   latency, complaints) too.
# - Offline evals catch regressions; A/B tests measure real user impact.
#   Use both.
#
# REAL-WORLD ANALOGY
# A restaurant testing a new recipe: they keep the old recipe card (version
# control), serve the new dish to half the tables chosen at random, and
# compare how many plates come back empty before changing the menu.
#
# SYNTAX:
#   variant = "B" if int(sha256(user_id).hexdigest(), 16) % 100 < 50 else "A"
#   z = (p_b - p_a) / sqrt(p * (1 - p) * (1/n_a + 1/n_b))
#
# SMALL WORKING EXAMPLE:
import hashlib
import math
import random

PROMPTS = {
    "support_reply@1.4.0": {"model": "claude-opus-5-5", "changelog": "baseline"},
    "support_reply@1.5.0": {"model": "claude-opus-5-5", "changelog": "explain next steps explicitly"},
}

def assign_variant(user_id, experiment="reply-v15", percent_b=50):
    digest = hashlib.sha256(f"{experiment}:{user_id}".encode()).hexdigest()
    return "support_reply@1.5.0" if int(digest, 16) % 100 < percent_b else "support_reply@1.4.0"

def two_proportion_z_test(successes_a, n_a, successes_b, n_b):
    p_a, p_b = successes_a / n_a, successes_b / n_b
    pooled = (successes_a + successes_b) / (n_a + n_b)
    se = math.sqrt(pooled * (1 - pooled) * (1 / n_a + 1 / n_b))
    z = (p_b - p_a) / se
    p_value = math.erfc(abs(z) / math.sqrt(2))
    return p_a, p_b, z, p_value

print("user-42 always gets:", {assign_variant("user-42") for _ in range(5)})
random.seed(0)
true_rate = {"support_reply@1.4.0": 0.62, "support_reply@1.5.0": 0.66}
counts = {v: [0, 0] for v in PROMPTS}
for i in range(4000):
    version = assign_variant(f"user-{i}")
    counts[version][1] += 1
    counts[version][0] += random.random() < true_rate[version]
(a_s, a_n), (b_s, b_n) = counts["support_reply@1.4.0"], counts["support_reply@1.5.0"]
p_a, p_b, z, p_value = two_proportion_z_test(a_s, a_n, b_s, b_n)
print(f"A resolved {p_a:.3f} (n={a_n}) | B resolved {p_b:.3f} (n={b_n}) | z={z:.2f} p={p_value:.4f}")
print("decision:", "ship 1.5.0" if p_value < 0.05 and p_b > p_a else "keep 1.4.0 / collect more data")

# EXPLANATION (LINE BY LINE):
# PROMPTS                    -> versioned prompt ids with model and changelog.
# assign_variant             -> hashing (experiment + user id) gives a stable, random-like
#                               split: the same user always sees the same version.
# two_proportion_z_test      -> is the difference in success rates bigger than chance?
#                               math.erfc gives the two-sided p-value.
# Simulation                 -> 4,000 users, B is truly 4 points better.
# decision                   -> ship only when significant AND in the right direction.
#
# COMMON MISTAKES:
# 1. Editing prompts in place with no version id in logs.
# 2. Random assignment per request (the same user flips between variants).
# 3. Stopping the test as soon as it "looks significant" (peeking).
# 4. Measuring only quality and ignoring cost/latency guardrails.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Write a CHANGELOG entry format for prompts and fill in three entries
# (a patch, a minor and a major change). Explain what makes a change "major".

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Simulate how many users you need to detect a 2-point improvement (60% -> 62%)
# with 80% probability: repeat the simulated experiment 200 times for several
# sample sizes and report how often p < 0.05.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Build a PromptStore backed by a JSON file: register(name, version, text,
# model, eval_score), get(name, version="latest"), rollback(name), and an
# audit log. Refuse to register a version whose eval_score is below the current
# production version unless force=True. Write tests for each behaviour.

# YOUR CODE:

