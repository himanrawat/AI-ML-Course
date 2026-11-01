# ======================================
# TOPIC: PYTHON DATA TYPES
# LEVEL: BEGINNER
# ID: python.variables.data-types
# ======================================

# INTRODUCTION
# Every value in Python has a type. The type decides what you can do with it:
# you can add two numbers, but you cannot divide a sentence by three.
#
# THEORY
# Core built-in types:
#   int     whole numbers            42, -7, 1_000_000
#   float   decimal numbers          3.14, -0.5, 1e6
#   bool    truth values             True, False
#   str     text                     "hello", 'hi'
#   NoneType  "no value"             None
# Collection types (covered in 02-Data-Structures): list, tuple, set, dict.
#
# Python is DYNAMICALLY typed: the type belongs to the value, not the name.
# Python is STRONGLY typed: it will not silently mix types ("3" + 4 is an error).
# type(x) tells you the type. isinstance(x, int) checks it.
# ints have unlimited size. floats are approximations (0.1 + 0.2 != 0.3 exactly).
#
# REAL-WORLD ANALOGY
# Types are like containers in a kitchen: a jug holds liquid, a box holds dry goods.
# You can pour from jug to jug, but pouring a box into a jug needs a conversion step.
#
# SYNTAX:
#   type(value)
#   isinstance(value, type_or_tuple_of_types)
#
# SMALL WORKING EXAMPLE:
count = 42
price = 19.99
is_active = True
title = "Data Science"
result = None
for value in (count, price, is_active, title, result):
    print(repr(value), "->", type(value).__name__)
print(isinstance(price, (int, float)))
print(0.1 + 0.2)
print(2 ** 100)

# EXPLANATION (LINE BY LINE):
# count = 42 ... result = None -> five variables, five different types.
# for value in (...):          -> visit each value in turn (loops come later).
# repr(value)                  -> shows the value the way you would type it (quotes for str).
# type(value).__name__         -> the type's name as text, e.g. "int".
# isinstance(price, (int, float)) -> True if price is an int OR a float.
# print(0.1 + 0.2)             -> 0.30000000000000004: floats are binary approximations.
# print(2 ** 100)              -> a huge exact integer; Python ints never overflow.
#
# COMMON MISTAKES:
# 1. Writing true/false/none in lowercase - Python uses True, False, None.
# 2. Comparing floats with == (use math.isclose(a, b) instead).
# 3. Using type(x) == int instead of isinstance(x, int) (breaks with subclasses).
# 4. Forgetting that bool is a subclass of int: True + True == 2.
# 5. Expecting "5" + 5 to work - Python raises TypeError.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Create one variable of each type: int, float, bool, str, None.
# Print each value together with its type.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Write a function describe(value) that returns a string such as
# "42 is an int" or "hello is a str", and returns "unknown type" for anything
# that is not int, float, bool, str or None. Remember bool is a subclass of int -
# make sure True is described as a bool. Test it on several values.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Show the float precision problem: add 0.1 ten times and compare with 1.0.
# Then solve it two ways: with math.isclose and with decimal.Decimal.
# Print a short explanation of why ML libraries usually accept tiny float errors.

# YOUR CODE:

