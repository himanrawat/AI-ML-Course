# ======================================
# TOPIC: HALLUCINATION MITIGATION
# LEVEL: INTERMEDIATE
# ID: prompt-engineering.safety.hallucination-mitigation
# ======================================

# INTRODUCTION
# A support bot that invents a refund policy, or a summary that adds a number
# that wasn't in the report, destroys trust. You can't eliminate hallucinations
# completely, but you can make them much rarer and easier to catch.
#
# THEORY
# Why it happens (recap): the model produces plausible continuations; when it
# lacks information it may still produce something plausible.
# Mitigations - each addresses a cause:
# - GROUNDING: provide the source text (RAG) and instruct the model to use only
#   it. Missing knowledge is the #1 cause.
# - PERMISSION TO ABSTAIN: explicitly allow "I don't know / not in the source".
#   Without it, the most "helpful-looking" continuation is a guess.
# - QUOTES FIRST: ask the model to extract relevant quotes before answering,
#   then answer only from those quotes; for long documents this focuses it.
# - CITATIONS: require a source reference for each claim (and check them).
# - VERIFICATION: a second pass (code or a model) checks each claim against
#   the source; reject or flag unsupported claims.
# - Constrain output: structured fields with null allowed instead of free text.
# - Tools for facts that change or need precision (search, calculators, DBs).
# - Lower the stakes in UX: show sources, let users verify.
#
# REAL-WORLD ANALOGY
# A journalist's rules: only report what your sources say, quote them, say
# "unconfirmed" when you're not sure, and have a fact-checker review before
# publishing.
#
# SYNTAX:
#   "Answer only from <source>. Quote the supporting sentence for each claim.
#    If the source does not contain the answer, say 'Not in source.'"
#
# SMALL WORKING EXAMPLE:
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from course_llm import complete

SOURCE = """Acme Pro costs $29 per month. Annual billing saves 20%.
Acme Pro includes 10 user seats. Extra seats cost $5 each per month.
Refunds are available within 14 days of purchase."""

def grounded_prompt(question):
    return f"""<source>
{SOURCE}
</source>
Answer the question using ONLY the source.
Return JSON: {{"answer": "...", "quotes": ["exact sentences from the source"], "found": true/false}}
If the source does not contain the answer, return found=false and answer "Not in source."
Question: {question}"""

def verify(reply_json):
    data = json.loads(reply_json)
    sentences = {s.strip() for s in re.split(r"(?<=[.!?])\s+", SOURCE)}
    unsupported = [q for q in data["quotes"] if q.strip() not in sentences]
    numbers_in_answer = set(re.findall(r"\d+", data["answer"]))
    numbers_in_quotes = set(re.findall(r"\d+", " ".join(data["quotes"])))
    return {"found": data["found"], "unsupported_quotes": unsupported,
            "numbers_not_in_quotes": sorted(numbers_in_answer - numbers_in_quotes)}

QUESTIONS = {
    "How much do 12 seats cost per month?": json.dumps({
        "answer": "$29 for 10 seats plus 2 x $5 = $39 per month.",
        "quotes": ["Acme Pro costs $29 per month.", "Acme Pro includes 10 user seats.",
                   "Extra seats cost $5 each per month."], "found": True}),
    "Is there a student discount?": json.dumps({"answer": "Not in source.", "quotes": [], "found": False}),
    "What is the refund window?": json.dumps({
        "answer": "30 days.", "quotes": ["Refunds are available within 30 days of purchase."], "found": True}),
}
for question, offline_reply in QUESTIONS.items():
    reply = complete(grounded_prompt(question), offline=offline_reply)
    print(question, "->", json.loads(reply)["answer"], "| check:", verify(reply))

# EXPLANATION (LINE BY LINE):
# SOURCE                     -> the only allowed knowledge (grounding).
# grounded_prompt            -> source first, "ONLY the source", quotes required,
#                               explicit "Not in source." path, JSON output.
# verify()                   -> code-based checks: every quote must be an exact
#                               sentence of the source (split on . ! ?); numbers in the answer must appear in quotes
#                               (39 and 2 are flagged - derived, so a human/tool should
#                               confirm the arithmetic).
# Third offline reply        -> a planted hallucination ("30 days"): the misquote is
#                               caught because it isn't in the source.
#
# COMMON MISTAKES:
# 1. "Don't hallucinate" as the only instruction (it doesn't remove the cause).
# 2. Not giving an explicit way to say "I don't know".
# 3. Asking for citations but never checking them.
# 4. Trusting derived numbers without a calculation check.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Write two prompts for answering HR policy questions: one ungrounded, one
# grounded with abstention and quotes. List which hallucination causes the
# second one addresses.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Improve verify(): match quotes approximately (difflib.SequenceMatcher ratio
# > 0.9) to tolerate whitespace changes, and flag answers that state numbers
# with found=false. Test with 6 crafted replies.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Build a two-pass pipeline (API access needed to run): pass 1 answers with
# quotes; pass 2 is a verifier prompt that receives the source and the answer
# and returns, per claim, supported/unsupported in JSON. Measure on 15 questions
# (5 unanswerable) how often unsupported claims slip through each pass.

# YOUR CODE:

