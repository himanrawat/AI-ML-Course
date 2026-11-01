# ======================================
# TOPIC: TASK DECOMPOSITION AND CHAIN-OF-THOUGHT
# LEVEL: INTERMEDIATE
# ID: prompt-engineering.reasoning.decomposition-cot
# ======================================

# INTRODUCTION
# Multi-step problems (calculations, policy decisions, debugging) fail when
# the model must jump straight to an answer. Letting it work through steps -
# or splitting the task yourself - makes complex reasoning far more reliable.
#
# THEORY
# - Each generated token is computed with a fixed amount of work. Writing out
#   intermediate steps gives the model more computation and lets later tokens
#   build on earlier results - that is why CHAIN-OF-THOUGHT (CoT) helps on
#   multi-step problems.
# - Prompted CoT: "Think through this step by step before answering."
#   Better: describe WHICH steps matter ("first list the relevant policy
#   clauses, then check each condition, then decide").
# - Separate reasoning from the final answer (e.g. <reasoning> and <answer>
#   tags) so your code can extract the answer.
# - REASONING MODELS / extended thinking: current models (including Claude
#   Opus 5.5) think internally before answering; you control depth with an
#   effort setting rather than prompting "think step by step". Prompted CoT is
#   still useful for smaller/faster settings and for making reasoning visible.
# - TASK DECOMPOSITION: break a big task into sub-tasks you can check
#   (extract facts -> apply rules -> write reply). Can be in one prompt or a
#   chain of prompts (see 06-prompt-chaining).
# - Costs: more tokens and latency. Don't use CoT for simple lookups.
# - The written reasoning is not guaranteed to be the "true" internal process;
#   verify answers, not just explanations.
#
# REAL-WORLD ANALOGY
# Long division on paper: you could guess the answer in your head, but writing
# each step catches mistakes and lets a teacher see where you went wrong.
#
# SYNTAX:
#   "First ..., then ..., finally ... Put your reasoning in <reasoning> tags
#    and only the final answer in <answer> tags."
#
# SMALL WORKING EXAMPLE:
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from course_llm import complete

POLICY = """Refunds: full refund within 30 days of delivery if unused.
Opened items: 50% refund within 14 days of delivery.
Sale items: store credit only, never cash refunds."""
CASE = "Bought a blender on sale, delivered 10 days ago, opened once. Customer wants cash back."

direct_prompt = f"{POLICY}\n\nCase: {CASE}\nWhat refund applies?"
structured_prompt = f"""<policy>
{POLICY}
</policy>
<case>{CASE}</case>

Decide what the customer is entitled to. Work through these steps inside <reasoning> tags:
1. List each fact from the case (sale item? days since delivery? opened?).
2. For each policy clause, state whether it applies and why.
3. Resolve conflicts between clauses (the most specific clause wins).
Then give the decision in one sentence inside <answer> tags."""

def extract_answer(text):
    match = re.search(r"<answer>(.*?)</answer>", text, re.DOTALL)
    return match.group(1).strip() if match else None

reply = complete(structured_prompt, offline=(
    "<reasoning>Facts: sale item; delivered 10 days ago; opened. Clause 1 does not apply (opened). "
    "Clause 2 would give 50% (within 14 days) but clause 3 is more specific: sale items get store credit "
    "only.</reasoning>\n<answer>Store credit only - no cash refund, because it was a sale item.</answer>"))
print(structured_prompt)
print("extracted answer:", extract_answer(reply))

# EXPLANATION (LINE BY LINE):
# POLICY + CASE              -> a decision with interacting rules: easy to get wrong
#                               in one jump (a model may answer "50% refund").
# direct_prompt              -> asks for the answer immediately.
# structured_prompt          -> names the steps that matter: facts, clause-by-clause
#                               check, conflict resolution.
# <reasoning>/<answer> tags  -> reasoning is visible for debugging, the answer is
#                               machine-extractable.
# extract_answer             -> parse only the final answer for your application.
#
# COMMON MISTAKES:
# 1. Using CoT for trivial tasks (slower, costlier, no gain).
# 2. Showing reasoning to end users when only the answer is wanted.
# 3. Trusting a plausible-looking reasoning chain without checking the answer.
# 4. Generic "think step by step" when you know which steps matter.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Write a direct prompt and a step-by-step prompt for: "A train leaves at 9:40
# and the trip takes 2h 35m with a 15-minute delay. When does it arrive?"
# Add answer tags and write the extraction function call.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Create 8 refund cases with known correct answers (including tricky
# combinations). With API access, compare direct_prompt vs structured_prompt
# accuracy. Without it, write the evaluation loop with a mocked complete().

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Decompose "write a weekly status report from raw Jira ticket JSON" into 4
# sub-tasks. For each: write the sub-prompt, its input/output format, and a
# programmatic check that validates its output before the next step runs.

# YOUR CODE:

