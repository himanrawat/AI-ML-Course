# ======================================
# TOPIC: ANATOMY OF AN EFFECTIVE PROMPT
# LEVEL: BEGINNER
# ID: prompt-engineering.foundations.anatomy
# ======================================

# INTRODUCTION
# A prompt is a specification for a probabilistic system. Most bad outputs
# come from missing information: the model had to guess the goal, audience,
# constraints or format. This topic gives you a checklist for WHY prompts work.
#
# THEORY
# Building blocks (not all are always needed):
# 1. TASK: what to do, stated directly ("Summarise", "Classify", "Extract").
# 2. CONTEXT: background the model cannot know - who the user is, why the
#    output is needed, what it will be used for. Explaining the PURPOSE helps
#    the model make good judgement calls on everything you did not specify.
# 3. INPUT DATA: the text/document to work on, clearly delimited
#    (XML-style tags like <document>...</document> work well).
# 4. CONSTRAINTS: length, tone, audience, what to include/exclude.
# 5. OUTPUT FORMAT: exact structure (bullets, JSON, headings).
# 6. EXAMPLES (optional): show, don't just tell.
# Principles:
# - Be explicit and specific; the model is not a mind reader.
# - Say what TO do, not only what not to do.
# - Separate instructions from data so the model doesn't confuse them.
# - Put long documents first and the question/instructions after them.
# - Test the prompt like code - prompts fail in ways you don't predict.
#
# REAL-WORLD ANALOGY
# Briefing a talented freelancer who has never met you: a one-line brief gets
# a generic result; a brief with purpose, audience, examples and deliverable
# format gets what you actually need.
#
# SYNTAX:
#   prompt = f"""<document>{doc}</document>
#   Task: ... Audience: ... Constraints: ... Output format: ..."""
#
# SMALL WORKING EXAMPLE:
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from course_llm import complete

release_notes = "v2.3: added dark mode; fixed login timeout bug; export to CSV now 3x faster; removed IE11 support."

weak_prompt = f"Summarise this: {release_notes}"
strong_prompt = f"""<release_notes>
{release_notes}
</release_notes>

Write a short "What's new" message for NON-TECHNICAL customers of our invoicing app.
Purpose: it appears in an in-app banner, so it must be scannable in 5 seconds.
Constraints:
- At most 3 bullet points, each under 12 words.
- Lead with the change customers will notice most.
- Mention removed IE11 support plainly, with a suggestion to use a modern browser.
- No version numbers or internal jargon ("bug", "export pipeline").
Output format: only the bullet points, each starting with "- "."""

checklist = {
    "task": "Write" in strong_prompt,
    "context/purpose": "Purpose:" in strong_prompt,
    "delimited data": "<release_notes>" in strong_prompt,
    "constraints": "Constraints:" in strong_prompt,
    "output format": "Output format:" in strong_prompt,
}
print("weak prompt has", len(weak_prompt.split()), "words; strong prompt has", len(strong_prompt.split()))
print("strong prompt checklist:", checklist)
print(complete(strong_prompt, offline=(
    "- Dark mode is here for easier night-time use\n"
    "- Exporting your invoices to CSV is now much faster\n"
    "- Internet Explorer 11 is no longer supported - please use a modern browser")))

# EXPLANATION (LINE BY LINE):
# weak_prompt                 -> the model must guess audience, length and style.
# strong_prompt               -> data first inside tags, then task, purpose,
#                                constraints and an exact output format.
# "Purpose: ... banner"       -> explains WHY, so the model can infer things like
#                                "keep it scannable" even for cases not listed.
# Positive instructions       -> "Lead with..." instead of only "Don't...".
# checklist                   -> a quick self-review of the prompt's components.
# complete(...)               -> offline sample unless COURSE_USE_LLM=1.
#
# COMMON MISTAKES:
# 1. Writing prompts like search queries ("summary release notes customers").
# 2. Omitting the audience and purpose.
# 3. Mixing instructions inside the data without delimiters.
# 4. Never testing the prompt on varied inputs.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Rewrite this weak prompt using all six building blocks:
# "Write an email about the meeting." Invent the missing context.
# Print both versions.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Write a prompt_linter(prompt) function that flags missing components:
# no delimiters around long data, no output format, only negative instructions
# ("don't"/"never" without positive alternatives), no stated audience. Test it
# on 4 prompts.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Take one task (e.g. summarising a bug report for a manager). Write three
# prompt versions of increasing specificity. With API access, run each on the
# same 3 bug reports and score outputs against a 4-point rubric you define
# (written before seeing outputs). Write which components made the biggest
# difference and why.

# YOUR CODE:

