# ======================================
# TOPIC: PROJECT 7 - PROMPT EVALUATION AND COMPARISON HARNESS
# LEVEL: ADVANCED
# ID: prompt-engineering.projects.eval-harness
# ======================================

# INTRODUCTION
# Build a reusable harness that runs several prompt variants over an eval set,
# grades them with pluggable graders, and produces a comparison report - the
# tool you'll use for every later LLM project.
#
# THEORY
# Skills used: evaluation (04/01), optimization (04/02), versioning (04/03),
# async concurrency (01-Python/12), cost tracking (04/04).
# Design decisions and WHY:
# - Separate VARIANTS (prompt + model settings), CASES (inputs + expectations)
#   and GRADERS (functions) -> mix and match without rewriting code.
# - Run every variant on the SAME cases; record outputs, scores, latency,
#   tokens -> fair comparison including cost.
# - Repeat runs (n > 1) to see output variance; report mean and spread.
# - Save results to disk (JSONL) with variant versions -> reproducible history.
# - Pairwise comparison per case shows WHERE a variant wins or loses.
# Deliverables: harness module, 3 graders (exact, schema, LLM judge),
# comparison of 3 variants on 20 cases, saved report.
#
# REAL-WORLD ANALOGY
# A blind taste test kitchen: every recipe (variant) is cooked for the same
# judges (graders) with the same ingredients (cases), and scores are recorded.
#
# SYNTAX:
#   report = run_comparison(variants, cases, graders)
#
# SMALL WORKING EXAMPLE:
import statistics
import time
from dataclasses import dataclass
from typing import Callable

@dataclass
class Variant:
    name: str
    run: Callable[[str], str]

@dataclass
class Case:
    input: str
    expected: str

def exact_match(case, output):
    return float(output.strip().lower() == case.expected)

def concise(case, output):
    return float(len(output.split()) <= 3)

def run_comparison(variants, cases, graders):
    report = {}
    for variant in variants:
        scores = {g.__name__: [] for g in graders}
        latencies = []
        for case in cases:
            start = time.perf_counter()
            output = variant.run(case.input)
            latencies.append((time.perf_counter() - start) * 1000)
            for grader in graders:
                scores[grader.__name__].append(grader(case, output))
        report[variant.name] = {name: round(statistics.mean(v), 3) for name, v in scores.items()}
        report[variant.name]["p50_ms"] = round(statistics.median(latencies), 3)
    return report

CASES = [Case("2+2", "4"), Case("capital of japan", "tokyo"), Case("opposite of hot", "cold"),
         Case("largest planet", "jupiter")]
ANSWERS = {"2+2": "4", "capital of japan": "Tokyo", "opposite of hot": "cold", "largest planet": "Jupiter"}
VARIANTS = [
    Variant("v1 chatty", lambda q: f"Great question! The answer is {ANSWERS[q]}."),
    Variant("v2 answer-only", lambda q: ANSWERS[q]),
]
for name, metrics in run_comparison(VARIANTS, CASES, [exact_match, concise]).items():
    print(f"{name:<16} {metrics}")

# EXPLANATION (LINE BY LINE):
# Variant / Case             -> data classes separating what runs from what's tested.
# Graders                    -> plain functions (case, output) -> score in [0, 1].
# run_comparison             -> every variant x every case x every grader, plus latency.
# Offline variants           -> deterministic stand-ins; with API access each variant's
#                               run() calls complete() with its own prompt template.
# Result                     -> v1 is correct in content but fails exact_match and
#                               concise: format instructions matter for automation.
#
# COMMON MISTAKES:
# 1. Comparing variants on different cases or different days' data.
# 2. A single run per case when outputs vary.
# 3. Not storing outputs, so you can't inspect why scores changed.
# 4. Ignoring cost/latency in the comparison.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Add a third grader contains_expected (expected answer appears anywhere in
# the output) and explain when it is a better metric than exact_match.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Make variants real prompts using complete() (API access) with three prompt
# styles for the same task, run each case 3 times, report mean and standard
# deviation per grader, and save every output to results/<timestamp>.jsonl.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Add an async runner with a concurrency limit, an LLM-judge grader with a
# rubric, token/cost tracking per variant, and a pairwise win/loss table
# (per case: which variant scored higher). Produce a Markdown report file.

# YOUR CODE:

