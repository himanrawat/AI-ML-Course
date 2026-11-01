# ======================================
# TOPIC: PROMPT CHAINING
# LEVEL: INTERMEDIATE
# ID: prompt-engineering.reasoning.chaining
# ======================================

# INTRODUCTION
# One giant prompt that extracts, analyses, decides and writes is hard to
# debug. Prompt chaining splits the work into a pipeline of focused calls,
# with code in between to validate and route.
#
# THEORY
# - Each step has ONE job, a clear input and a structured output that the next
#   step consumes.
# - Benefits: each prompt is simpler (better quality), steps can be tested and
#   improved independently, you can validate between steps, use cheaper/faster
#   models for easy steps, and run independent steps in parallel.
# - Code between steps can: validate output, branch (route to different
#   prompts), stop early, retry, or call non-LLM tools.
# - Costs: more calls (latency), errors can propagate - so validate at each
#   boundary.
# - Common chains: extract -> transform -> generate; draft -> critique ->
#   revise; classify -> route -> specialised handler.
#
# REAL-WORLD ANALOGY
# A newspaper: a reporter gathers facts, an editor checks them, a copy-editor
# polishes the text. Each person does one job well, and errors are caught
# between stages.
#
# SYNTAX:
#   facts = step1(input); validate(facts); draft = step2(facts); final = step3(draft)
#
# SMALL WORKING EXAMPLE:
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from course_llm import complete

REVIEW = ("Ordered the X200 headphones. Sound is fantastic, but the left ear cup "
          "cracked after a week and support hasn't replied in 5 days. Very disappointed.")

def step_extract(review):
    prompt = ("Extract from the product review. Return JSON with keys: product (string), "
              "positives (list), problems (list), sentiment (positive|negative|mixed).\n"
              f"<review>{review}</review>")
    reply = complete(prompt, offline=json.dumps({
        "product": "X200 headphones", "positives": ["sound quality"],
        "problems": ["left ear cup cracked after a week", "no support reply for 5 days"],
        "sentiment": "mixed"}))
    data = json.loads(reply)
    assert data["sentiment"] in {"positive", "negative", "mixed"}, "invalid sentiment"
    return data

def step_route(facts):
    if any("crack" in p or "broken" in p for p in facts["problems"]):
        return "warranty"
    return "thank_you" if facts["sentiment"] == "positive" else "general"

def step_write(facts, route):
    prompt = (f"Write a 3-sentence public reply to a {facts['sentiment']} review of {facts['product']}.\n"
              f"Acknowledge: {facts['positives']}. Address: {facts['problems']}.\n"
              f"Reply type: {route} (for warranty: offer a free replacement via support@acme.test).")
    return complete(prompt, offline=(
        "Thank you for sharing - we're glad you love the X200's sound! A cracked ear cup after a week "
        "isn't acceptable, and we're sorry support hasn't replied yet. Please email support@acme.test "
        "and we'll send a free replacement right away."))

facts = step_extract(REVIEW)
print("1. extracted:", facts)
route = step_route(facts)
print("2. route:", route)
print("3. reply:", step_write(facts, route))

# EXPLANATION (LINE BY LINE):
# step_extract               -> LLM step 1: structured facts only, validated in code.
# assert on sentiment        -> a boundary check; a bad value stops the chain early.
# step_route                 -> plain Python decides the path (no LLM needed).
# step_write                 -> LLM step 2 gets only the clean facts + route, not raw text.
# Each step can now be tested and improved separately.
#
# COMMON MISTAKES:
# 1. Passing raw, unvalidated LLM output to the next step.
# 2. Using an LLM for steps that simple code does better (routing rules).
# 3. Chains so long that latency becomes unacceptable.
# 4. Not logging intermediate outputs (impossible to debug).

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Draw (as comments) a 3-step chain for turning a meeting transcript into an
# email with action items. Define each step's input and output format.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Implement a draft -> critique -> revise chain for writing a LinkedIn post:
# the critique step must return JSON with a list of issues and a score; skip
# the revise step if the score is >= 8. Use mocked responses offline.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Build a ChainRunner that executes a list of steps (functions), records each
# step's input, output, latency and errors, supports retries per step, and can
# run independent steps concurrently with asyncio. Run the review chain on 5
# reviews and print a per-step timing table.

# YOUR CODE:

