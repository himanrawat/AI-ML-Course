# ======================================
# TOPIC: DEBUGGING AND OPTIMIZING AI SYSTEMS
# LEVEL: ADVANCED
# ID: mlops.production.debugging-ai-systems
# ======================================

# INTRODUCTION
# When an AI product gives a bad answer, the cause could be data, retrieval,
# the prompt, the model, a tool, or plain code. Systematic debugging finds the
# failing COMPONENT instead of randomly tweaking prompts.
#
# THEORY
# A debugging method for AI pipelines:
#  1. REPRODUCE: capture the exact input, versions (model, prompt, index,
#     code) and trace of the failing request.
#  2. LOCALISE: inspect each stage's output in the trace - input parsing ->
#     retrieval -> prompt assembly -> model output -> post-processing -> tools.
#     The first stage with wrong output is the culprit.
#  3. CLASSIFY the root cause (data, retrieval, instruction, model capability,
#     integration bug) and count causes across many failures (error analysis).
#  4. FIX the biggest cause; add the case to the eval set (regression test).
#  5. VERIFY on the full eval set; watch production metrics after release.
# OPTIMISING: measure first, then improve the worst of quality/cost/latency
# with the levers from earlier modules (caching, retrieval, model choice,
# effort, batching, smaller outputs). Judge cost per completed task.
#
# REAL-WORLD ANALOGY
# A plumber tracing a leak: check each joint along the pipe in order instead
# of replacing every pipe in the house.
#
# SYNTAX:
#   first_bad_stage = next(s for s in stages if not s.check(trace[s.name]))
#
# SMALL WORKING EXAMPLE:
from collections import Counter

TRACES = [
    {"id": 1, "question": "refund window?", "retrieved_relevant": True, "prompt_has_context": True,
     "output_valid_json": True, "answer_correct": True},
    {"id": 2, "question": "ERR-4012 meaning?", "retrieved_relevant": False, "prompt_has_context": True,
     "output_valid_json": True, "answer_correct": False},
    {"id": 3, "question": "seat price?", "retrieved_relevant": True, "prompt_has_context": False,
     "output_valid_json": True, "answer_correct": False},
    {"id": 4, "question": "cancel plan?", "retrieved_relevant": True, "prompt_has_context": True,
     "output_valid_json": False, "answer_correct": False},
    {"id": 5, "question": "SSO setup?", "retrieved_relevant": False, "prompt_has_context": True,
     "output_valid_json": True, "answer_correct": False},
    {"id": 6, "question": "tax on invoices?", "retrieved_relevant": True, "prompt_has_context": True,
     "output_valid_json": True, "answer_correct": False},
]
STAGES = [
    ("retrieval", "retrieved_relevant", "improve chunking/hybrid search for ids and codes"),
    ("prompt assembly", "prompt_has_context", "bug: context dropped when over token budget"),
    ("output format", "output_valid_json", "use native structured outputs + retry"),
    ("generation", "answer_correct", "error analysis on answers with good context"),
]

def first_failing_stage(trace):
    for name, key, _ in STAGES:
        if not trace[key]:
            return name
    return None

causes = Counter(first_failing_stage(t) for t in TRACES if not t["answer_correct"])
print("failures by first failing stage:", causes.most_common())
top_stage = causes.most_common(1)[0][0]
print("fix first:", top_stage, "->", next(fix for name, _, fix in STAGES if name == top_stage))

# EXPLANATION (LINE BY LINE):
# TRACES                     -> per-request records with a check for each pipeline stage
#                               (from observability logs + eval labels).
# STAGES                     -> ordered pipeline stages, the trace field that verifies each,
#                               and a candidate fix.
# first_failing_stage        -> walks the pipeline in order; the first broken stage is the
#                               root cause (later stages fail as a consequence).
# Counter                    -> error analysis: retrieval causes the most failures here, so
#                               improving the prompt wording would not help them.
#
# COMMON MISTAKES:
# 1. Tweaking the prompt for problems caused by retrieval or data.
# 2. Debugging without the exact versions involved.
# 3. Fixing one example and not adding it to the eval set.
# 4. Optimising cost before quality is acceptable.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Add 6 more traces covering every stage and re-run the analysis. Does the top
# cause change?

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Take your RAG pipeline from 08-RAG-and-Agents and add a trace record to every
# stage (retrieved ids + scores, prompt length, raw output, parse status).
# Run 10 questions and use first_failing_stage to analyse failures.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Run a full optimisation cycle on one of your projects: baseline eval (quality,
# p95 latency, cost per task), error analysis, two targeted fixes, re-evaluate,
# and write a short incident-style report (problem, root cause, fix, results,
# follow-ups) as a multi-line string saved to Markdown.

# YOUR CODE:

