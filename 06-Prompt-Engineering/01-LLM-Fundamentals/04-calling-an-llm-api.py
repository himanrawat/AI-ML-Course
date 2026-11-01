# ======================================
# TOPIC: CALLING AN LLM API
# LEVEL: BEGINNER
# ID: prompt-engineering.fundamentals.calling-api
# ======================================

# INTRODUCTION
# To write, test and evaluate prompts systematically, you call the model from
# code - not from a chat window. This topic shows the Anthropic Python SDK and
# the course helper used in all later topics.
#
# THEORY
# - Install: pip install anthropic (already in the course .venv).
# - Credentials: the SDK reads ANTHROPIC_API_KEY (or an `ant auth login`
#   profile). Never hard-code keys.
# - A request (Messages API) has:
#   model        which model (here "claude-opus-5-5")
#   max_tokens   maximum OUTPUT tokens
#   system       optional system prompt (instructions about behaviour/role)
#   messages     the conversation: [{"role": "user", "content": "..."},
#                {"role": "assistant", ...}, ...] alternating roles
# - The response contains content blocks; collect the "text" blocks. Check
#   stop_reason: "end_turn" (finished), "max_tokens" (cut off), "refusal"
#   (declined by safety classifiers).
# - usage.input_tokens / usage.output_tokens tell you what you paid for.
# - The course helper: course_llm.complete(prompt, system=..., offline=...)
#   runs OFFLINE with a sample reply unless COURSE_USE_LLM=1 is set.
#
# REAL-WORLD ANALOGY
# Sending a well-formatted letter: an envelope (model, limits), a cover note
# about how to respond (system), and the letter itself (messages).
#
# SYNTAX:
#   client = anthropic.Anthropic()
#   response = client.messages.create(model=..., max_tokens=..., system=..., messages=[...])
#
# SMALL WORKING EXAMPLE:
import os

from anthropic import Anthropic


def ask(question, system="You are a concise tutor. Answer in at most two sentences."):
    client = Anthropic()
    response = client.messages.create(
        model="claude-opus-5-5",
        max_tokens=1024,
        system=system,
        messages=[{"role": "user", "content": question}],
    )
    if response.stop_reason == "refusal":
        return "[the model declined this request]"
    text = "".join(block.text for block in response.content if block.type == "text")
    usage = response.usage
    return f"{text}\n(tokens in/out: {usage.input_tokens}/{usage.output_tokens}, stop: {response.stop_reason})"


conversation = [
    {"role": "user", "content": "What is a Python list?"},
    {"role": "assistant", "content": "An ordered, mutable collection of items."},
    {"role": "user", "content": "And how is a tuple different?"},
]
print("Conversation payload sent on turn 2:")
for message in conversation:
    print(f"  {message['role']:>9}: {message['content']}")
if os.environ.get("COURSE_USE_LLM") == "1":
    print(ask("What is the difference between a list and a tuple in Python?"))
else:
    print("Offline: set COURSE_USE_LLM=1 and ANTHROPIC_API_KEY to make a real call.")

# EXPLANATION (LINE BY LINE):
# from anthropic import Anthropic  -> the official SDK client.
# client = Anthropic()             -> credentials come from the environment.
# messages.create(...)             -> one request: model, output cap, system, messages.
# stop_reason == "refusal"         -> always check before reading content.
# "".join(block.text ...)          -> responses are lists of blocks; keep the text ones.
# response.usage                   -> input/output tokens actually billed.
# conversation                     -> multi-turn chat = resend the whole history
#                                     with alternating user/assistant roles.
# COURSE_USE_LLM guard             -> the file runs offline unless you opt in.
#
# COMMON MISTAKES:
# 1. Committing API keys to Git.
# 2. Assuming response.content[0] is always text.
# 3. Not checking stop_reason (silently truncated or refused outputs).
# 4. Two consecutive messages with the same role.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Set up your API key in your shell (not in code), run this file with
# COURSE_USE_LLM=1, and paste the answer and token usage as comments.
# If you have no key yet, write down the exact commands you will use.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Build a tiny command-line chat loop: keep a messages list, read user input,
# call the API with the full history, append the assistant reply, and print
# running token totals. Type "exit" to quit.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Write a robust ask_many(questions, concurrency=3) using AsyncAnthropic with
# a semaphore, catching anthropic.RateLimitError and anthropic.APIConnectionError
# separately, recording latency and token usage per call, and returning a
# summary table. Test it on 6 questions (or mock the client offline).

# YOUR CODE:

