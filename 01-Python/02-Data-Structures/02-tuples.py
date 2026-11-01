# ======================================
# TOPIC: TUPLES
# LEVEL: BEGINNER
# ID: python.data-structures.tuples
# ======================================

# INTRODUCTION
# A tuple is a fixed group of values that belong together, such as a
# coordinate (x, y) or the shape of a data array (rows, columns).
#
# THEORY
# - Ordered and indexable like a list, but IMMUTABLE: no append, no item assignment.
# - Created with commas; parentheses are for readability. (5,) is a 1-item tuple.
# - Unpacking: x, y = point. Star-unpacking: first, *rest = values.
# - Because they are immutable (and hashable when their items are),
#   tuples can be dictionary keys and set members. Lists cannot.
# - Functions return multiple values as a tuple: return mean, std.
# - collections.namedtuple gives fields names: Point(x=1, y=2).
#
# REAL-WORLD ANALOGY
# A sealed envelope with a date of birth: day, month, year.
# The parts belong together and should never be edited separately.
#
# SYNTAX:
#   point = (3, 4)
#   single = (5,)
#   a, b = point
#   head, *tail = (1, 2, 3, 4)
#
# SMALL WORKING EXAMPLE:
from collections import namedtuple

def min_max(values):
    return min(values), max(values)

shape = (128, 64)
rows, cols = shape
low, high = min_max([4, 9, 1, 7])
first, *middle, last = (10, 20, 30, 40, 50)
distances = {("Delhi", "Mumbai"): 1400}
Point = namedtuple("Point", ["x", "y"])
p = Point(3, 4)
print(rows * cols, low, high, middle, last)
print(distances[("Delhi", "Mumbai")], p.x, p._asdict())
print(type((5)), type((5,)))

# EXPLANATION (LINE BY LINE):
# def min_max(...): return min(...), max(...)  -> returns ONE tuple of two values.
# rows, cols = shape         -> unpack the tuple into two names.
# low, high = min_max(...)   -> unpack the returned tuple directly.
# first, *middle, last = ... -> star collects everything in between into a LIST.
# distances = {(a, b): ...}  -> a tuple used as a dictionary key.
# namedtuple("Point", ...)   -> creates a small tuple class with named fields.
# p.x, p._asdict()           -> access by name; convert to a dict.
# type((5)) vs type((5,))    -> int vs tuple: the COMMA makes the tuple.
#
# COMMON MISTAKES:
# 1. Writing (5) and expecting a tuple - you need (5,).
# 2. Trying t[0] = 1 -> TypeError.
# 3. Unpacking with the wrong number of names -> ValueError.
# 4. Assuming a tuple containing a list is fully immutable (the list can change).

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Create a tuple with your birth day, month and year. Unpack it into three
# variables and print a sentence using them.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Write stats(numbers) that returns (count, total, mean) as a tuple.
# Call it and unpack the result. Handle an empty list by returning (0, 0, None).

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Represent 2D points as a namedtuple Point(x, y). Given a list of points,
# return the pair of points that are closest together (use math.dist).
# Use a dict keyed by (point_a, point_b) tuples to cache distances.

# YOUR CODE:

