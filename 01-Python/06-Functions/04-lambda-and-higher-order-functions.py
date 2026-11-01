# ======================================
# TOPIC: LAMBDA AND HIGHER-ORDER FUNCTIONS
# LEVEL: INTERMEDIATE
# ID: python.functions.lambda-higher-order
# ======================================

# INTRODUCTION
# Sorting records by a field, applying a transformation to every row,
# passing a callback to a library: all of these pass functions as values.
#
# THEORY
# - A higher-order function takes a function as an argument or returns one.
# - lambda creates a small anonymous function with ONE expression:
#     lambda x: x * 2
#   It cannot contain statements (no assignments, loops, return).
# - Built-ins that take functions: sorted(key=), min/max(key=), map, filter.
# - functools.reduce combines items pairwise; functools.partial pre-fills args.
# - operator.itemgetter / attrgetter are fast, readable key functions.
# - Prefer comprehensions over map/filter with lambda when it reads better.
#
# REAL-WORLD ANALOGY
# Giving a sorting instruction card to an assistant: "sort these files by
# date". The card (function) tells them HOW; they do the work.
#
# SYNTAX:
#   sorted(items, key=lambda item: item["score"], reverse=True)
#   list(map(func, items)); list(filter(predicate, items))
#   functools.partial(func, fixed_arg)
#
# SMALL WORKING EXAMPLE:
from functools import partial, reduce
from operator import itemgetter

models = [
    {"name": "svm", "accuracy": 0.88, "latency": 12},
    {"name": "cnn", "accuracy": 0.94, "latency": 40},
    {"name": "tree", "accuracy": 0.81, "latency": 2},
]
by_accuracy = sorted(models, key=itemgetter("accuracy"), reverse=True)
print([m["name"] for m in by_accuracy])
fastest = min(models, key=lambda m: m["latency"])
print(fastest["name"])
good = list(filter(lambda m: m["accuracy"] > 0.85, models))
names_upper = list(map(lambda m: m["name"].upper(), good))
print(names_upper)
product = reduce(lambda a, b: a * b, [1, 2, 3, 4])
print(product)

def power(base, exponent):
    return base ** exponent

square = partial(power, exponent=2)
print(square(9))

def apply_twice(func, value):
    return func(func(value))

print(apply_twice(square, 3))

# EXPLANATION (LINE BY LINE):
# sorted(models, key=itemgetter("accuracy"), reverse=True)
#   -> itemgetter("accuracy") is like lambda m: m["accuracy"].
# min(models, key=lambda m: m["latency"]) -> the record with the lowest latency.
# filter(lambda ..., models)  -> keeps records where the lambda returns True.
# map(lambda ..., good)       -> transforms each record; list() collects results.
# reduce(lambda a, b: a * b, [1,2,3,4]) -> ((1*2)*3)*4 = 24.
# partial(power, exponent=2)  -> a new function with exponent fixed.
# apply_twice(square, 3)      -> square(square(3)) = 81: a function as an argument.
#
# COMMON MISTAKES:
# 1. Assigning lambdas to names (square = lambda x: ...) - use def instead.
# 2. Forgetting that map/filter return lazy iterators (wrap with list()).
# 3. Writing unreadable nested lambdas.
# 4. Calling the function when passing it: key=len() instead of key=len.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Sort a list of words by length, then by alphabetical order for ties,
# using sorted with a lambda that returns a tuple.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Write compose(*funcs) returning a function that applies funcs right to left:
# compose(f, g)(x) == f(g(x)). Use it to build a text cleaner from str.strip,
# str.lower and a custom function.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Implement your own my_map, my_filter and my_reduce (with an optional
# initial value) using loops, and verify they match the built-ins on several
# inputs. Then use reduce to merge a list of dicts of word counts into one.

# YOUR CODE:

