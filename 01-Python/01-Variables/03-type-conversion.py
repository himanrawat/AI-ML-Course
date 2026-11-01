# ======================================
# TOPIC: TYPE CONVERSION
# LEVEL: BEGINNER
# ID: python.variables.type-conversion
# ======================================

# INTRODUCTION
# Data rarely arrives in the type you need. Text from a file, a form or an API
# often has to become numbers before you can calculate with it.
#
# THEORY
# Explicit conversion uses the type as a function:
#   int("42") -> 42        float("3.5") -> 3.5      str(10) -> "10"
#   bool(0) -> False       int(3.9) -> 3 (truncates toward zero, does NOT round)
# Implicit conversion only happens between numbers: 1 + 2.0 -> 3.0 (int becomes float).
# Invalid conversions raise ValueError: int("abc"), int("3.5").
#
# Truthiness: bool() of an empty value is False:
#   0, 0.0, "", [], {}, set(), None -> False; almost everything else -> True.
#
# REAL-WORLD ANALOGY
# Currency exchange: you explicitly convert rupees to dollars before paying abroad.
# If you hand over a note that is not money at all, the exchange refuses (ValueError).
#
# SYNTAX:
#   int(x), float(x), str(x), bool(x)
#   int("ff", 16)   # convert from another base
#   round(x, ndigits)
#
# SMALL WORKING EXAMPLE:
raw_age = "29"
raw_height = "1.75"
age = int(raw_age)
height = float(raw_height)
print(age + 1, height * 100)
print(int(7.9), round(7.9), round(2.5), round(3.5))
print(bool(""), bool("False"), bool([]), bool(0.0))
try:
    int("3.5")
except ValueError as error:
    print("Cannot convert:", error)
print(int(float("3.5")))

# EXPLANATION (LINE BY LINE):
# raw_age = "29"            -> looks like a number but is a string.
# age = int(raw_age)        -> now a real integer, so age + 1 is 30.
# height = float(...)       -> "1.75" becomes 1.75.
# int(7.9)                  -> 7: int() cuts off the decimal part.
# round(2.5), round(3.5)    -> 2 and 4: Python rounds halves to the nearest EVEN number.
# bool("False")             -> True! Any non-empty string is truthy.
# try / except ValueError   -> int("3.5") fails; we catch and print the error.
# int(float("3.5"))         -> convert in two steps when the text has decimals.
#
# COMMON MISTAKES:
# 1. Expecting int() to round. It truncates.
# 2. Expecting bool("False") to be False.
# 3. Forgetting that input() always returns a str.
# 4. Converting user data without handling ValueError.
# 5. Concatenating "Age: " + 30 instead of "Age: " + str(30) or an f-string.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Given price = "499" and quantity = "3" (both strings),
# convert them and print the total cost.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Write a function to_number(text) that returns an int if the text is a whole
# number, a float if it has decimals, and None if it is not a number at all.
# Test: "42", "-3.5", "1e3", "abc", "  7  ".

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# You receive a row from a CSV file as strings:
# row = {"id": "17", "score": "88.5", "passed": "yes", "notes": ""}
# Write clean_row(row) that returns properly typed values:
# id -> int, score -> float, passed -> bool ("yes"/"true"/"1" are True,
# case-insensitive), notes -> None when empty. Raise ValueError with a clear
# message if id or score is invalid.

# YOUR CODE:

