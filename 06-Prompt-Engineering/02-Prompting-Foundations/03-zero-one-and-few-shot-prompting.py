# ======================================
# TOPIC: ZERO-SHOT, ONE-SHOT AND FEW-SHOT PROMPTING
# LEVEL: BEGINNER
# ID: prompt-engineering.foundations.shot-prompting
# ======================================

# INTRODUCTION
# Sometimes describing what you want is harder than showing it. Examples in the
# prompt steer format, tone, label boundaries and edge-case handling - this is
# in-context learning.
#
# THEORY
# - ZERO-SHOT: instructions only. Works well for common, clearly described
#   tasks. Start here.
# - ONE-SHOT: one example. Mainly fixes the OUTPUT FORMAT and style.
# - FEW-SHOT: several examples (typically 2-8). Teaches label boundaries,
#   tricky cases and consistent formatting.
# Why it works: examples shift the probability of continuations toward the
# demonstrated pattern without changing weights.
# Choosing examples (the reasoning, not a template):
# - DIVERSE: cover different categories and edge cases; similar examples make
#   the model overfit to surface features.
# - REPRESENTATIVE of real inputs; include hard cases you actually see.
# - BALANCED: an unbalanced set biases predictions toward the common label;
#   models also pick up on the order (recency) of examples.
# - CORRECT and CONSISTENT: errors in examples are copied.
# - Wrap examples in tags (<example>) so they are not confused with the input.
# - Examples cost tokens on every request; dynamic selection (pick the most
#   similar examples per input) helps at scale.
#
# REAL-WORLD ANALOGY
# Training a new labeller: a rule sheet (zero-shot), one filled-in sample form
# (one-shot), or a folder of tricky solved cases (few-shot).
#
# SYNTAX:
#   <examples><example><input>...</input><output>...</output></example>...</examples>
#
# SMALL WORKING EXAMPLE:
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from course_llm import complete

INSTRUCTION = ("Classify the customer message into exactly one label: "
               "billing, bug, feature_request, praise. Reply with the label only.")
EXAMPLES = [
    ("I was charged twice this month.", "billing"),
    ("The export button does nothing on Safari.", "bug"),
    ("Love the new dashboard, great work!", "praise"),
    ("Could you add a dark mode?", "feature_request"),
    ("Your app is great but the invoice total is wrong.", "bug"),
]

def build_prompt(message, examples):
    shots = "\n".join(
        f"<example>\n<message>{text}</message>\n<label>{label}</label>\n</example>"
        for text, label in examples)
    examples_block = f"<examples>\n{shots}\n</examples>\n\n" if examples else ""
    return f"{INSTRUCTION}\n\n{examples_block}<message>{message}</message>"

message = "Nice app, but the PDF has the wrong tax amount."
for name, shots in [("zero-shot", []), ("one-shot", EXAMPLES[:1]), ("few-shot", EXAMPLES)]:
    prompt = build_prompt(message, shots)
    print(f"--- {name}: {len(prompt.split())} words")
print(build_prompt(message, EXAMPLES))
print("label:", complete(build_prompt(message, EXAMPLES), offline="bug"))

# EXPLANATION (LINE BY LINE):
# INSTRUCTION                -> the task and the closed set of labels (zero-shot part).
# EXAMPLES                   -> one per label PLUS a hard case: praise + a real problem
#                               ("great but ... wrong") is labelled bug.
# build_prompt               -> wraps each example in tags; the new message comes last.
# Word counts                -> examples cost tokens on every call.
# The test message mixes praise and a tax error: the hard example teaches the
# model the boundary (a problem outranks praise), which instructions alone left
# ambiguous.
#
# COMMON MISTAKES:
# 1. Examples that all look alike (the model copies surface patterns).
# 2. Unbalanced labels in examples causing biased predictions.
# 3. Examples that contradict the instructions.
# 4. Adding examples before trying a clear zero-shot instruction.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Write zero-shot and few-shot prompts that convert informal dates
# ("next Friday", "end of month", "in 2 weeks") into ISO dates given today's
# date. Print both prompts and explain which ambiguities the examples resolve.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Build a 20-message labelled test set for the classifier above. With API
# access (or by reasoning through it), compare zero-shot vs few-shot accuracy
# and list the messages each version gets wrong. Then add one example that
# fixes the most common error and re-test.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Implement dynamic few-shot selection: given a pool of 30 labelled examples,
# pick the k most similar to each input (TF-IDF cosine similarity from
# scikit-learn) while ensuring every label appears at least once. Compare
# fixed vs dynamic examples on your test set and on token cost.

# YOUR CODE:

