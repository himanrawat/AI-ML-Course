# ======================================
# TOPIC: ARITHMETIC OPERATORS
# LEVEL: BEGINNER
# ID: python.operators.arithmetic
# ======================================

# INTRODUCTION
# Machine learning is mostly arithmetic done at scale. Before matrices and
# gradients, you need to be precise with Python's basic maths operators.
#
# THEORY
#   +  add        -  subtract     *  multiply     /  true division (always float)
#   // floor division (rounds DOWN, toward negative infinity)
#   %  modulo (remainder; result has the sign of the divisor)
#   ** power      divmod(a, b) -> (a // b, a % b)
# Precedence (high to low): **, unary -, * / // %, + -. Use parentheses to be clear.
# Note: -2 ** 2 is -4 because ** binds tighter than unary minus.
# The math module adds sqrt, log, exp, floor, ceil, isclose, pi, e.
#
# REAL-WORLD ANALOGY
# Sharing 17 sweets among 5 children: each gets 17 // 5 = 3 sweets,
# and 17 % 5 = 2 sweets are left over.
#
# SYNTAX:
#   a + b, a - b, a * b, a / b, a // b, a % b, a ** b
#
# SMALL WORKING EXAMPLE:
import math

sweets, children = 17, 5
print(sweets / children, sweets // children, sweets % children)
print(divmod(sweets, children))
print(-7 // 2, -7 % 2)
print(2 ** 10, -2 ** 2, (-2) ** 2)
print(math.sqrt(16), math.log(math.e), math.exp(0))
seconds = 3725
hours, rest = divmod(seconds, 3600)
minutes, secs = divmod(rest, 60)
print(f"{hours}h {minutes}m {secs}s")

# EXPLANATION (LINE BY LINE):
# 17 / 5 -> 3.4 (float), 17 // 5 -> 3, 17 % 5 -> 2.
# divmod(17, 5)        -> (3, 2) in one call.
# -7 // 2 -> -4        -> floor division rounds DOWN, not toward zero.
# -7 % 2 -> 1          -> so that (-7 // 2) * 2 + (-7 % 2) == -7.
# -2 ** 2 -> -4        -> power happens before the minus sign.
# math.log(math.e)     -> natural log, 1.0. math.exp(0) -> 1.0.
# divmod(seconds, 3600) -> converts seconds into hours + remaining seconds.
#
# COMMON MISTAKES:
# 1. Expecting / to give an int (it always returns float).
# 2. Assuming // truncates toward zero for negative numbers.
# 3. Writing x^2 for power (^ is bitwise XOR) - use x ** 2.
# 4. Dividing by zero -> ZeroDivisionError.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Given a bill of 2350 rupees shared by 4 friends with a 10% tip,
# print the total and each person's share rounded to 2 decimals.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Write is_even(n), last_digit(n) and digit_sum(n) using only arithmetic
# operators (no string conversion). Make them work for negative numbers.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Implement compound_interest(principal, annual_rate, years, times_per_year)
# and the continuous version principal * e ** (rate * years).
# Print a table for years 1..5 comparing both. Then implement mean and
# standard deviation of a list using only arithmetic and math.sqrt.

# YOUR CODE:

