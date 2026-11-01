# ======================================
# TOPIC: COMPREHENSIONS
# LEVEL: INTERMEDIATE
# ID: python.data-structures.comprehensions
# ======================================

# INTRODUCTION
# Data work constantly transforms and filters collections. Comprehensions do
# that in one readable line, and they are everywhere in Python code.
#
# THEORY
# A comprehension builds a new collection from an iterable:
#   [expression for item in iterable if condition]      -> list
#   {key: value for item in iterable if condition}      -> dict
#   {expression for item in iterable}                   -> set
#   (expression for item in iterable)                   -> generator (lazy)
# The "if" at the end FILTERS. An if/else in the expression TRANSFORMS:
#   [x if x > 0 else 0 for x in nums]
# Nested loops read left to right like nested for statements.
# Keep comprehensions short; use a normal loop when logic gets complex.
#
# REAL-WORLD ANALOGY
# A factory conveyor belt: items come in, a filter removes bad ones,
# a machine reshapes the rest, and a box collects the results.
#
# SYNTAX:
#   squares = [n * n for n in range(5)]
#   evens = [n for n in nums if n % 2 == 0]
#   lookup = {name: len(name) for name in names}
#
# SMALL WORKING EXAMPLE:
temps_c = [21.5, -3.0, 30.2, 15.0]
temps_f = [round(c * 9 / 5 + 32, 1) for c in temps_c]
freezing = [c for c in temps_c if c <= 0]
clipped = [c if c >= 0 else 0 for c in temps_c]
names = ["asha", "ben", "chen"]
name_lengths = {name: len(name) for name in names}
first_letters = {name[0] for name in names + ["anil"]}
pairs = [(x, y) for x in range(2) for y in "ab"]
total = sum(c * c for c in temps_c)
print(temps_f, freezing, clipped)
print(name_lengths, sorted(first_letters))
print(pairs, round(total, 2))

# EXPLANATION (LINE BY LINE):
# [... for c in temps_c]            -> convert every temperature to Fahrenheit.
# [c for c in temps_c if c <= 0]    -> keep only freezing values (filter).
# [c if c >= 0 else 0 for c in ...] -> transform: negatives become 0 (no filtering).
# {name: len(name) for ...}         -> dict comprehension.
# {name[0] for ...}                 -> set comprehension; duplicates removed.
# [(x, y) for x ... for y ...]      -> nested loops: x is the outer loop.
# sum(c * c for c in temps_c)       -> generator expression: no list is built.
#
# COMMON MISTAKES:
# 1. Putting if/else at the end: [x for x in a if x > 0 else 0] -> SyntaxError.
# 2. Writing huge, nested comprehensions nobody can read.
# 3. Using a comprehension only for side effects ([print(x) for x in a]).
# 4. Forgetting that (x for x in a) is a one-time generator, not a tuple.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Using comprehensions, build: the squares of 1..10, only the odd squares,
# and a dict mapping each number 1..5 to its cube.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Given matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]], use comprehensions to
# flatten it into one list and to transpose it (rows become columns).

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Given a list of user dicts with "name", "age" and "email" (some emails are
# None or invalid - no "@"), use comprehensions to produce:
# 1) a dict email -> name for valid emails only, lowercased;
# 2) a set of the decades represented (20s, 30s...);
# 3) a list of names sorted by age, oldest first.
# Then rewrite (1) as a normal for loop and comment on which is clearer.

# YOUR CODE:

