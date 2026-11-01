# ======================================
# TOPIC: PYTHON VARIABLES
# LEVEL: BEGINNER
# ID: python.variables.basics
# ======================================

# INTRODUCTION
# Every program needs to remember things: a user's name, a price, a score.
# Variables are how Python remembers values while a program runs.
#
# THEORY
# A variable is a name that refers to a value stored in memory.
# You create a variable by assigning a value to a name with "=".
# Python works out the type of the value by itself (no type declaration).
# You can re-assign a variable at any time, even to a different type.
#
# Naming rules:
# - Letters, digits and underscores only; cannot start with a digit.
# - Case-sensitive: age and Age are different variables.
# - Convention: lowercase_with_underscores (called snake_case).
# - Constants (values that should not change) use UPPER_CASE by convention.
#
# REAL-WORLD ANALOGY
# A variable is a labelled sticky note attached to a box.
# The label (name) lets you find the box; the box holds the value.
# Re-assigning moves the sticky note to a different box.
#
# SYNTAX:
#   name = value
#   a, b = 1, 2          # assign several variables at once
#   x = y = 0            # give several names the same value
#
# SMALL WORKING EXAMPLE:
name = "Himanshu"
age = 25
MAX_LOGIN_ATTEMPTS = 3
city, country = "Delhi", "India"
print(name)
print(age)
print(city, country)
age = age + 1
print("Next year:", age)

# EXPLANATION (LINE BY LINE):
# name = "Himanshu"          -> the name "name" now refers to a string.
# age = 25                   -> "age" refers to an integer.
# MAX_LOGIN_ATTEMPTS = 3     -> UPPER_CASE signals "treat this as a constant".
# city, country = ...        -> multiple assignment: first value to city, second to country.
# print(name) / print(age)   -> print() displays a value on the screen.
# print(city, country)       -> print() separates multiple values with a space.
# age = age + 1              -> right side is calculated first (26), then stored in age.
# print("Next year:", age)   -> prints a label and the updated value.
#
# COMMON MISTAKES:
# 1. Using a variable before assigning it -> NameError.
# 2. Starting a name with a digit (1st_name) or using spaces (first name).
# 3. Confusing "=" (assignment) with "==" (comparison).
# 4. Using built-in names as variables (list = [1, 2]) hides the built-in list().
# 5. Thinking UPPER_CASE makes a value unchangeable - it is only a convention.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Create variables for your name, age and salary.
# Print all three values.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Create three variables a, b and c with different values.
# Rotate their values so that a gets b's value, b gets c's value
# and c gets a's original value - in ONE line, without a temporary variable.
# Print the values before and after.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Create an employee information program using multiple variables
# of different data types: full name (str), employee id (int),
# monthly salary (float), is_manager (bool), skills (list of str).
# Calculate the annual salary, then print a neatly aligned report
# with one labelled field per line. Use a constant for MONTHS_PER_YEAR.

# YOUR CODE:

