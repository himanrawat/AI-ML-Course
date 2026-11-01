# ======================================
# TOPIC: COMPARISON AND LOGICAL OPERATORS
# LEVEL: BEGINNER
# ID: python.operators.comparison-logical
# ======================================

# INTRODUCTION
# Programs make decisions: is accuracy above the threshold? Is the input
# valid AND not empty? Comparison and logical operators produce those answers.
#
# THEORY
# Comparison operators return True/False: ==  !=  <  <=  >  >=
# Comparisons can be CHAINED: 0 <= x < 10 means (0 <= x) and (x < 10).
# Logical operators: and, or, not.
# - They SHORT-CIRCUIT: and stops at the first falsy value, or at the first truthy.
# - and/or return one of their OPERANDS, not necessarily True/False:
#     "" or "default" -> "default";   0 and 5 -> 0.
# Strings compare alphabetically by Unicode code point ("B" < "a").
# Comparing different incompatible types with < raises TypeError ("1" < 2).
#
# REAL-WORLD ANALOGY
# A club entrance: you need a ticket AND ID. The guard stops checking the
# moment one is missing (short-circuit).
#
# SYNTAX:
#   a == b, a != b, a < b <= c
#   cond1 and cond2, cond1 or cond2, not cond
#
# SMALL WORKING EXAMPLE:
accuracy = 0.87
loss = 0.31
print(accuracy > 0.85 and loss < 0.4)
print(0.8 <= accuracy < 0.9)
print(not accuracy > 0.9)
username = ""
display_name = username or "Guest"
print(display_name)
print(0 and 5, 3 and 5, None or 0 or "fallback")
print("apple" < "banana", "B" < "a")

def expensive_check():
    print("expensive_check ran")
    return True

print(False and expensive_check())

# EXPLANATION (LINE BY LINE):
# accuracy > 0.85 and loss < 0.4 -> both comparisons True -> True.
# 0.8 <= accuracy < 0.9          -> chained comparison, reads like maths.
# not accuracy > 0.9             -> not applies to the whole comparison -> True.
# username or "Guest"            -> "" is falsy, so or returns "Guest".
# 0 and 5 -> 0; 3 and 5 -> 5     -> and returns the first falsy value or the last one.
# None or 0 or "fallback"        -> or returns the first truthy value.
# "B" < "a"                      -> True: uppercase letters have lower code points.
# False and expensive_check()    -> short-circuit: the function is never called.
#
# COMMON MISTAKES:
# 1. Using & and | (bitwise) instead of and / or for booleans.
# 2. Writing x == 1 or 2 (always truthy) instead of x in (1, 2).
# 3. Using "x or default" when 0 or "" are valid values.
# 4. Comparing floats with == directly.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Given age and has_ticket, print whether a person can enter a cinema
# (age >= 18 and has a ticket). Try four combinations.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Write is_valid_password(pw): at least 8 chars, contains a digit, contains an
# uppercase letter, and does not contain spaces. Use any() and logical operators.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Write is_leap_year(year) as ONE boolean expression. Then write a function
# should_deploy(model) that returns True only if accuracy >= 0.9, latency_ms
# < 200, AND (approved_by is not None or is_hotfix). Show a case where
# short-circuiting avoids an error (e.g. checking a key exists before using it).

# YOUR CODE:

