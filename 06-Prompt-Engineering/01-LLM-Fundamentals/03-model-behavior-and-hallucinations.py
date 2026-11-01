# ======================================
# TOPIC: MODEL BEHAVIOUR, LIMITATIONS AND WHY HALLUCINATIONS HAPPEN
# LEVEL: BEGINNER
# ID: prompt-engineering.fundamentals.model-behavior
# ======================================

# INTRODUCTION
# Good prompt engineers know where models are strong and where they fail.
# Most prompt failures come from asking the model to do something its nature
# makes unreliable - without giving it the means to succeed.
#
# THEORY
# Strengths: language understanding and generation, summarisation,
# classification, extraction, translation, code, reasoning over provided text.
# Limitations and their causes:
# - HALLUCINATION: the model generates fluent, plausible text even when it lacks
#   the facts - next-token prediction rewards plausibility. Risk is highest for
#   specific details: citations, numbers, names, dates, niche facts.
# - KNOWLEDGE CUTOFF: no knowledge of events after training unless you provide it.
# - No access to your private data unless you put it in the context.
# - Precise computation, counting characters, long exact arithmetic: better
#   done with code/tools.
# - Sensitivity to phrasing, ordering and examples.
# - Sycophancy: may agree with a confidently stated wrong premise.
# Practical rule: give the model the information it needs (context), the
# permission to say "I don't know", a way to verify (quotes, tools), and a
# clear output format.
#
# REAL-WORLD ANALOGY
# A brilliant new employee on day one: articulate and quick, but if you ask
# about a meeting they never attended, they may give a confident guess unless
# you hand them the minutes and tell them guessing is not OK.
#
# SYNTAX:
#   prompt = context + task + "If the answer is not in the context, say 'Not found'."
#
# SMALL WORKING EXAMPLE:
TASKS = [
    ("Summarise this pasted article", "strong", "all information is in the prompt"),
    ("What is our refund policy?", "risky", "private data - must be provided in context"),
    ("Who won yesterday's match?", "risky", "after the knowledge cutoff - needs search/tools"),
    ("Count the letter 'r' in 'strawberry'", "risky", "character-level task - tokens hide letters; use code"),
    ("Multiply 48213 by 9127", "risky", "exact arithmetic - use a calculator tool"),
    ("Classify this review as positive/negative", "strong", "pattern recognition on given text"),
    ("Give me 3 academic citations on topic X", "risky", "specific references are easy to fabricate"),
]
for task, rating, reason in TASKS:
    print(f"[{rating:^6}] {task:<45} -> {reason}")

def grounded_prompt(question, context):
    return (
        "Answer the question using ONLY the context below.\n"
        "If the context does not contain the answer, reply exactly: Not found in the provided context.\n\n"
        f"<context>\n{context}\n</context>\n\n"
        f"Question: {question}"
    )

print(grounded_prompt("What is the refund window?", "Refunds are accepted within 30 days of delivery."))
print("check with code instead of the model:", "strawberry".count("r"), 48213 * 9127)

# EXPLANATION (LINE BY LINE):
# TASKS                      -> each task rated by how well it fits model strengths,
#                               with the underlying REASON (not a memorised rule).
# grounded_prompt            -> supplies the missing information (context),
#                               restricts the source, and gives an explicit way out.
# <context> tags             -> clear delimiters separate data from instructions.
# "strawberry".count / 48213 * 9127 -> deterministic work belongs in code or tools.
#
# COMMON MISTAKES:
# 1. Asking for facts the model cannot know and trusting the answer.
# 2. Not allowing "I don't know" - the model fills the gap with a guess.
# 3. Using the model for arithmetic or counting that code does perfectly.
# 4. Treating confident tone as evidence of correctness.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# List 5 tasks from your own work (frontend or otherwise). For each, rate it
# strong/risky for an LLM and write the reason, like the TASKS table.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Write a prompt with a false premise ("Since Python 4 removed the GIL in
# 2019, explain...") and a revised prompt that invites the model to check
# premises. If you have API access, run both and compare. Explain the result.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Design a small "hallucination probe" set: 8 questions where the correct
# answer is "I don't know / not in context" mixed with 8 answerable ones, all
# with a provided context. Write a scoring function that measures how often a
# model answers when it should abstain. Run it with a real model if available.

# YOUR CODE:

