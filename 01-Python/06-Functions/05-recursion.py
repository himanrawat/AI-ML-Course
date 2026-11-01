# ======================================
# TOPIC: RECURSION
# LEVEL: INTERMEDIATE
# ID: python.functions.recursion
# ======================================

# INTRODUCTION
# Some data is naturally nested: folders inside folders, JSON inside JSON,
# decision trees. Recursion - a function calling itself - handles such data.
#
# THEORY
# A recursive function has:
#   1. A BASE CASE that returns without recursing (stops the recursion).
#   2. A RECURSIVE CASE that calls itself on a SMALLER problem.
# Each call gets its own frame on the call stack. Python's default limit is
# about 1000 frames (sys.getrecursionlimit()) -> RecursionError if exceeded.
# Python does not optimise tail calls, so deep recursion should become a loop.
# Memoization (functools.lru_cache / cache) avoids repeated sub-problems.
#
# REAL-WORLD ANALOGY
# Russian nesting dolls: to find the smallest doll, open the doll; if there is
# another doll inside, repeat; when a doll does not open, you are done.
#
# SYNTAX:
#   def solve(problem):
#       if is_simple(problem):
#           return answer
#       return combine(solve(smaller(problem)))
#
# SMALL WORKING EXAMPLE:
from functools import cache

def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

def count_leaves(node):
    if not isinstance(node, (list, dict)):
        return 1
    children = node.values() if isinstance(node, dict) else node
    return sum(count_leaves(child) for child in children)

@cache
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)

print(factorial(5))
config = {"model": {"layers": [64, 32], "dropout": 0.2}, "seed": 42}
print(count_leaves(config))
print(fib(80))

# EXPLANATION (LINE BY LINE):
# factorial: base case n <= 1 returns 1; otherwise n * factorial(n - 1).
#   factorial(5) -> 5 * 4 * 3 * 2 * 1 = 120.
# count_leaves: a non-container is one leaf (base case).
#   For dicts we recurse into values, for lists into items, and add up the counts.
#   config has 64, 32, 0.2 and 42 -> 4 leaves.
# @cache on fib -> each fib(n) is computed once, so fib(80) is instant
#   instead of taking longer than the age of the universe.
#
# COMMON MISTAKES:
# 1. Missing or unreachable base case -> RecursionError.
# 2. Not making the problem smaller each call.
# 3. Exponential time from repeated sub-problems (no memoization).
# 4. Using recursion for simple iteration where a loop is clearer.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Write a recursive sum_list(numbers) and a recursive count_down(n) that
# prints n down to 1.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Write flatten(nested) that turns [1, [2, [3, 4]], 5] into [1, 2, 3, 4, 5]
# recursively. Then write binary_search(sorted_list, target) recursively.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Write find_keys(data, key) that returns every value stored under a given
# key anywhere in a deeply nested JSON-like structure (dicts and lists).
# Then write an iterative version using an explicit stack and confirm both
# give the same results. Explain in a comment when you would prefer each.

# YOUR CODE:

