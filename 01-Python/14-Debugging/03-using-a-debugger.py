# ======================================
# TOPIC: USING A DEBUGGER
# LEVEL: INTERMEDIATE
# ID: python.debugging.debugger
# ======================================

# INTRODUCTION
# Print statements show what you THOUGHT to print. A debugger pauses the
# program so you can inspect every variable, step line by line and test ideas
# while the program is frozen.
#
# THEORY
# - breakpoint() pauses execution and opens pdb (the built-in debugger)
#   in the terminal. Set PYTHONBREAKPOINT=0 to disable all breakpoints.
# - Key pdb commands:
#     n (next line)      s (step into a call)   c (continue)
#     p expr (print)     pp expr (pretty print) l (list code)
#     w (where: call stack)  u / d (move up/down the stack)  q (quit)
# - python -m pdb script.py starts a script under the debugger;
#   pdb.post_mortem() inspects the state after a crash.
# - VS Code: click left of a line number to add a breakpoint, press F5
#   ("Python Debugger: Current File"), then use the Variables panel,
#   Watch expressions, Step Over (F10) / Step Into (F11).
#   Conditional breakpoints pause only when an expression is true.
# - Debugging method: reproduce -> isolate -> inspect -> hypothesise -> fix
#   -> add a test so it never returns.
#
# REAL-WORLD ANALOGY
# Watching a football match replay: pause at the moment of the foul, rewind,
# and look at where every player was - instead of reading the final score.
#
# SYNTAX:
#   breakpoint()                     # pause here
#   if i == 500: breakpoint()        # pause only for a specific case
#
# SMALL WORKING EXAMPLE:
import os

DEBUG = os.environ.get("COURSE_DEBUG") == "1"

def moving_average(values, window):
    averages = []
    for i in range(len(values) - window + 1):
        chunk = values[i:i + window]
        if DEBUG and i == 2:
            breakpoint()
        averages.append(sum(chunk) / window)
    return averages

prices = [10, 12, 13, 12, 15, 18]
print(moving_average(prices, 3))
print(moving_average(prices, 6))
print(moving_average(prices, 7))

# EXPLANATION (LINE BY LINE):
# DEBUG = os.environ.get("COURSE_DEBUG") == "1"
#     -> breakpoints are off by default; run with COURSE_DEBUG=1 to pause.
# range(len(values) - window + 1) -> number of complete windows.
# if DEBUG and i == 2: breakpoint() -> a conditional breakpoint in code.
#     Try:  COURSE_DEBUG=1 python 03-using-a-debugger.py
#     then: p chunk, p i, p averages, n, c
# moving_average(prices, 7) -> window larger than the data -> [] (silently!).
#     A debugger session quickly shows range(0) produced no iterations.
#
# COMMON MISTAKES:
# 1. Leaving breakpoint() calls in committed code.
# 2. Stepping through hundreds of iterations instead of using a condition.
# 3. Changing several things at once while debugging.
# 4. Not writing a test for the bug after fixing it.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Run this file with COURSE_DEBUG=1. At the pause, print chunk, i and
# averages, step with n three times, then continue with c. Write down (in
# comments) what you observed.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# The function below has a bug. Use the VS Code debugger (breakpoint + Variables
# panel) to find it, then fix it and explain the bug in a comment.
# def median(values):
#     values.sort()
#     mid = len(values) // 2
#     return (values[mid] + values[mid + 1]) / 2 if len(values) % 2 == 0 else values[mid]

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Write a function that crashes deep inside nested calls on one input out of
# 1000. Use try/except with pdb.post_mortem (guarded by COURSE_DEBUG) to
# inspect the failing frame, and write a reusable context manager
# debug_on_error() that starts post-mortem debugging only when enabled.

# YOUR CODE:

