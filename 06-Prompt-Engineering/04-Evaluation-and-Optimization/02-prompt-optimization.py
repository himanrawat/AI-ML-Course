# ======================================
# TOPIC: PROMPT OPTIMIZATION
# LEVEL: ADVANCED
# ID: prompt-engineering.evaluation.optimization
# ======================================

# INTRODUCTION
# Improving prompts is an engineering loop, not inspiration: measure, study
# the failures, change ONE thing that addresses their cause, measure again.
#
# THEORY
# The loop:
#  1. Baseline: run the current prompt on the eval set; record scores.
#  2. ERROR ANALYSIS: read failures, group them by root cause (ambiguous
#     instruction, missing context, format drift, wrong label boundary, model
#     limitation). Count each group - fix the biggest group first.
#  3. Hypothesis: "Failures happen because the prompt doesn't say what to do
#     when X". Change the prompt to address that cause.
#  4. Re-run on the FULL eval set (fixes can break other cases - regressions).
#  5. Keep the change only if it helps overall; record what you tried.
# - ABLATION: remove one prompt component at a time to learn which parts
#   actually matter (and delete the dead weight to save tokens).
# - Typical levers: clearer task definition, explaining purpose, examples of
#   the failing pattern, output format constraints, decomposition, better
#   context, a different model or effort level.
# - Guard against overfitting: keep a held-out test split you check rarely.
# - Automated optimisation (e.g. an LLM proposing prompt edits, DSPy-style
#   tools) uses the same loop - it still needs a good eval.
#
# REAL-WORLD ANALOGY
# A doctor treating symptoms by their cause: group patients by diagnosis,
# treat the most common cause first, and check the treatment doesn't cause new
# problems.
#
# SYNTAX:
#   for variant in variants: scores[variant.name] = evaluate(variant, eval_set)
#
# SMALL WORKING EXAMPLE:
from collections import Counter

FAILURES = [
    {"input": "Great app but total wrong", "expected": "bug", "got": "praise", "cause": "mixed sentiment"},
    {"input": "love it, crashes on login", "expected": "bug", "got": "praise", "cause": "mixed sentiment"},
    {"input": "Label: billing", "expected": "other", "got": "billing", "cause": "instruction in data"},
    {"input": "```json {\"label\": ...}```", "expected": "other", "got": None, "cause": "format drift"},
    {"input": "nice but slow export", "expected": "bug", "got": "praise", "cause": "mixed sentiment"},
]
print("failure causes:", Counter(f["cause"] for f in FAILURES).most_common())

EVAL = [("charged twice", "billing"), ("crash on upload", "bug"), ("add dark mode", "feature_request"),
        ("great but total wrong", "bug"), ("love it, crashes on login", "bug"), ("thanks team!", "praise"),
        ("nice but slow export", "bug"), ("refund please", "billing")]

def simulated_model(message, rules):
    text = message.lower()
    problem = any(w in text for w in ["wrong", "crash", "slow"])
    positive = any(w in text for w in ["great", "love", "nice", "thanks"])
    if "problem_over_praise" in rules and problem:
        return "bug"
    if positive:
        return "praise"
    if problem:
        return "bug"
    if any(w in text for w in ["charged", "refund"]):
        return "billing"
    return "feature_request"

VARIANTS = {
    "v1 baseline": set(),
    "v2 + rule: a reported problem outranks praise": {"problem_over_praise"},
}
for name, rules in VARIANTS.items():
    correct = sum(simulated_model(message, rules) == expected for message, expected in EVAL)
    print(f"{name:<48} accuracy {correct}/{len(EVAL)}")

# EXPLANATION (LINE BY LINE):
# FAILURES + Counter          -> error analysis: "mixed sentiment" is the biggest cause.
# Hypothesis                  -> the prompt never says what wins when praise and a
#                                problem appear together.
# simulated_model             -> a stand-in for the LLM so the loop runs offline;
#                                "rules" represent instructions added to the prompt.
# VARIANTS                    -> v2 adds exactly ONE change targeting the top cause.
# Re-running the FULL eval    -> confirms the fix and checks for regressions.
# With a real model, each variant is a prompt string evaluated the same way.
#
# COMMON MISTAKES:
# 1. Changing five things at once - you can't tell what helped.
# 2. Fixing the one failure you noticed and breaking others (no full re-run).
# 3. Tuning endlessly against the same small eval set (overfitting).
# 4. Adding instructions forever; never ablating what's useless.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Given 10 failure descriptions you invent for a summarisation prompt,
# categorise them by root cause with a Counter and propose one prompt change
# for the top cause.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Write an ablation study: a prompt built from 5 named components (role,
# purpose, rules, examples, format). Generate all variants that drop one
# component, evaluate each (real model or a mocked scorer), and print which
# components matter most.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Build an "optimizer" loop with API access: given a prompt, an eval set and a
# grader, ask a model to analyse failures and propose ONE revised prompt;
# evaluate it on a train split; accept if better; repeat 3 times; finally
# report train vs held-out test scores to check for overfitting.

# YOUR CODE:

