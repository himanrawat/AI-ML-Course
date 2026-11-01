# ======================================
# TOPIC: MATCH-CASE (STRUCTURAL PATTERN MATCHING)
# LEVEL: INTERMEDIATE
# ID: python.conditions.match-case
# ======================================

# INTRODUCTION
# When you must react differently to many shapes of data - commands, API
# events, tool calls from an AI agent - match-case is cleaner than a long
# chain of elifs.
#
# THEORY
# match subject:
#     case pattern: ...
# Patterns can be:
# - Literals: case 200:      - Alternatives: case 401 | 403:
# - Capture names: case x:   (binds the value to x; acts as a catch-all!)
# - Wildcard: case _:        (matches anything, binds nothing - the "default")
# - Sequences: case [first, *rest]:
# - Mappings: case {"type": "click", "x": x}:  (extra keys are allowed)
# - Class patterns: case Point(x=0, y=y):
# - Guards: case n if n < 0:
# Only the FIRST matching case runs. Requires Python 3.10+.
#
# REAL-WORLD ANALOGY
# A mail sorting room: parcels are matched by shape and label - "small
# envelope", "box addressed to Delhi", "anything else goes to the desk".
#
# SYNTAX:
#   match value:
#       case 1 | 2:
#           ...
#       case {"key": captured}:
#           ...
#       case _:
#           ...
#
# SMALL WORKING EXAMPLE:
def handle(event):
    match event:
        case {"type": "message", "text": str(text)} if text.strip():
            return f"message: {text}"
        case {"type": "tool_call", "name": name, "args": [*args]}:
            return f"call {name} with {len(args)} args"
        case {"type": "error", "code": 401 | 403}:
            return "auth problem"
        case {"type": str(kind)}:
            return f"unhandled type {kind}"
        case _:
            return "not an event"

print(handle({"type": "message", "text": "hi"}))
print(handle({"type": "tool_call", "name": "search", "args": ["python", 5]}))
print(handle({"type": "error", "code": 403}))
print(handle({"type": "ping"}))
print(handle([1, 2]))

# EXPLANATION (LINE BY LINE):
# match event:                     -> the subject to compare against each pattern.
# case {"type": "message", "text": str(text)} if text.strip():
#     -> dict with type "message" and a str text; the guard rejects blank text.
# case {"type": "tool_call", "name": name, "args": [*args]}:
#     -> captures name and requires args to be a sequence.
# case {"type": "error", "code": 401 | 403}: -> alternatives inside a pattern.
# case {"type": str(kind)}:        -> any other dict with a string type.
# case _:                          -> default when nothing else matched.
#
# COMMON MISTAKES:
# 1. Writing case status: to compare with a variable - it CAPTURES instead.
#    Use dotted constants (case Status.OK:) or a guard.
# 2. Putting case _ first, so later cases never run.
# 3. Expecting mapping patterns to require an exact key set (extra keys pass).
# 4. Using match on Python < 3.10.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Write http_message(status) using match-case: 200 -> "OK",
# 404 -> "Not Found", 500 | 502 | 503 -> "Server Error", anything else -> "Unknown".

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Write a calculator(command) where command is a list like ["add", 2, 3],
# ["neg", 5] or ["sum", 1, 2, 3, 4]. Use sequence patterns and guards to
# reject non-numeric arguments.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# An LLM agent returns actions as dicts. Write dispatch(action) supporting:
# {"action": "search", "query": q}, {"action": "calculate", "expression": e},
# {"action": "final_answer", "answer": a}, and anything else -> an error dict.
# Use a dataclass (or simple class) for one pattern via a class pattern.
# Test with 5 actions, including malformed ones.

# YOUR CODE:

