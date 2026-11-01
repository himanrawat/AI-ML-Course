# ======================================
# TOPIC: PROMPT ENGINEERING VS CONTEXT ENGINEERING VS FINE-TUNING
# LEVEL: ADVANCED
# ID: prompt-engineering.strategy.prompt-context-finetuning
# ======================================

# INTRODUCTION
# When a model isn't doing what you need, there are three very different
# levers. Choosing the wrong one wastes weeks; choosing the right one is a
# core skill of an AI engineer. None of them replaces understanding ML and how
# models behave.
#
# THEORY
# PROMPT ENGINEERING - shape the instructions and examples of a call.
# - Changes: wording, structure, examples, output format, decomposition.
# - Best for: task definition, format, tone, label boundaries.
# - Cost: cheap, instant to iterate. Limit: can't add knowledge the prompt
#   doesn't contain; long prompts cost tokens on every call.
# CONTEXT ENGINEERING - decide WHAT information the model sees, across a system.
# - Changes: retrieved documents (RAG), tool definitions and results, memory,
#   conversation history management, user/profile data, ordering and
#   compression of context within the window.
# - Best for: private, fresh or large knowledge; agents; personalisation.
# - Cost: engineering effort (retrieval, data pipelines). Limit: quality depends
#   on retrieval; more context isn't always better.
# FINE-TUNING - change the model's WEIGHTS with training examples.
# - Changes: behaviour learned from hundreds to thousands of examples
#   (LoRA/QLoRA for open models; vendor fine-tuning APIs where offered).
# - Best for: consistent style/format at scale, narrow specialised tasks,
#   shrinking prompts, making a smaller cheaper model match a larger one.
# - Cost: data collection, training, evaluation, re-training when base models
#   update. Limit: poor at injecting frequently changing FACTS (use RAG).
# Default order: prompt -> context -> fine-tune, each justified by evals.
#
# REAL-WORLD ANALOGY
# Hiring a consultant: prompt engineering is a better brief; context
# engineering is giving them access to your files and systems; fine-tuning is
# sending them on a months-long training course to change how they work.
#
# SYNTAX:
#   decision = choose_approach(problem_profile)
#
# SMALL WORKING EXAMPLE:
def choose_approach(problem):
    reasons = []
    if problem["needs_private_or_fresh_knowledge"]:
        reasons.append(("context engineering (RAG/tools)", "knowledge the model can't have"))
    if problem["failures_are_instructions_or_format"]:
        reasons.append(("prompt engineering", "task definition/format issues are fixed in the prompt"))
    if (problem["labelled_examples"] >= 500 and problem["prompt_approaches_plateaued"]
            and problem["high_volume"]):
        reasons.append(("fine-tuning", "stable task, enough data, prompts plateaued, volume justifies it"))
    if not reasons:
        reasons.append(("prompt engineering", "start with the cheapest lever and measure"))
    return reasons

CASES = {
    "support bot answering from a 300-page policy manual": dict(
        needs_private_or_fresh_knowledge=True, failures_are_instructions_or_format=False,
        labelled_examples=0, prompt_approaches_plateaued=False, high_volume=True),
    "JSON extraction keeps missing optional fields": dict(
        needs_private_or_fresh_knowledge=False, failures_are_instructions_or_format=True,
        labelled_examples=50, prompt_approaches_plateaued=False, high_volume=False),
    "10M daily classifications, 20k labels, prompt accuracy stuck at 91%": dict(
        needs_private_or_fresh_knowledge=False, failures_are_instructions_or_format=False,
        labelled_examples=20_000, prompt_approaches_plateaued=True, high_volume=True),
}
for name, profile in CASES.items():
    print(name)
    for approach, why in choose_approach(profile):
        print(f"   -> {approach}: {why}")

# EXPLANATION (LINE BY LINE):
# choose_approach             -> encodes the reasoning, not a fixed rule: each lever
#                                is matched to the CAUSE of the problem.
# Missing knowledge           -> context engineering (fine-tuning facts is brittle).
# Instruction/format failures -> prompt engineering.
# Fine-tuning only when       -> lots of labelled data, prompts plateaued, and high
#                                volume makes training and maintenance worth it.
# The default                 -> start cheap, measure with evals, escalate when justified.
#
# COMMON MISTAKES:
# 1. Fine-tuning to teach facts that change monthly.
# 2. Stuffing an entire knowledge base into the prompt instead of retrieving.
# 3. Skipping evals, so you can't tell which lever helped.
# 4. Believing prompt engineering replaces understanding ML, data and model limits.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# For 5 scenarios you invent (e.g. legal clause finder, brand-voice writer,
# code reviewer), pick the first lever to try and justify it in one sentence.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Extend choose_approach with cost estimates: prompt tokens per call x volume
# vs one-off fine-tuning cost + cheaper model inference. Find the break-even
# daily volume for a scenario you define.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Write a one-page decision record (as a multi-line string) for a real problem
# from your work or portfolio: problem, eval results for prompt-only and a RAG
# prototype (real or projected), the decision, risks, and what evidence would
# make you switch to fine-tuning.

# YOUR CODE:

