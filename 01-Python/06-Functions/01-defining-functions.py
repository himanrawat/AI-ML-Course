# ======================================
# TOPIC: DEFINING FUNCTIONS
# LEVEL: BEGINNER
# ID: python.functions.defining
# ======================================

# INTRODUCTION
# Functions package a piece of logic under a name so you can reuse it,
# test it and reason about it. Every ML pipeline is a chain of functions.
#
# THEORY
# - def name(parameters): defines a function. The body is indented.
# - return sends a value back and ends the function. Without return, the
#   function returns None.
# - Parameters are the names in the definition; arguments are the values passed.
# - A docstring (first string in the body) documents what the function does;
#   help(func) shows it.
# - Functions are objects: you can store them in variables, lists and dicts.
# - A good function does ONE thing, has a clear name (verb), and avoids
#   changing global state.
#
# REAL-WORLD ANALOGY
# A coffee machine: you put in inputs (beans, water), press a button, and get
# an output (coffee). You do not need to know the internals each time.
#
# SYNTAX:
#   def function_name(param1, param2):
#       """What it does."""
#       return result
#
# SMALL WORKING EXAMPLE:
def bmi(weight_kg, height_m):
    """Return body-mass index rounded to one decimal place."""
    return round(weight_kg / height_m ** 2, 1)

def bmi_category(value):
    if value < 18.5:
        return "underweight"
    if value < 25:
        return "normal"
    return "overweight"

def log(message):
    print(f"[log] {message}")

score = bmi(70, 1.75)
print(score, bmi_category(score))
result = log("done")
print(result)
print(bmi.__doc__)
operations = {"bmi": bmi, "category": bmi_category}
print(operations["category"](30))

# EXPLANATION (LINE BY LINE):
# def bmi(weight_kg, height_m):  -> two parameters.
# """Return ..."""               -> docstring documenting the function.
# return round(...)              -> compute and return the result.
# bmi_category uses early returns -> each return ends the function immediately.
# def log(message): print(...)   -> no return statement...
# result = log("done"); print(result) -> ...so it returns None.
# bmi.__doc__                    -> functions carry their docstring.
# operations["category"](30)     -> functions stored in a dict and called later.
#
# COMMON MISTAKES:
# 1. Printing inside a function instead of returning (result can't be reused).
# 2. Forgetting the parentheses: bmi instead of bmi(70, 1.75).
# 3. Code after return that never runs.
# 4. Functions that silently modify global variables.
# 5. Defining a function after the line that calls it (at module level).

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Write celsius_to_fahrenheit(c) and fahrenheit_to_celsius(f) with docstrings.
# Check that converting back and forth returns the original value.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Write normalize(values) that returns a new list scaled to 0..1
# using (x - min) / (max - min). Handle the case where all values are equal.
# Do not modify the input.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Build a mini text-processing pipeline from small functions:
# lowercase(text), remove_punctuation(text), tokenize(text), remove_stopwords(tokens).
# Write pipeline(text, steps) that applies a list of functions in order.
# Show that changing the order of steps changes (or breaks) the result.

# YOUR CODE:

