# ======================================
# TOPIC: SCOPE AND CLOSURES
# LEVEL: INTERMEDIATE
# ID: python.functions.scope-closures
# ======================================

# INTRODUCTION
# Where a variable is visible, and how long it lives, decides many subtle bugs.
# Closures let functions remember state - the basis of decorators and callbacks.
#
# THEORY
# Python looks up names in LEGB order:
#   Local (inside the current function) -> Enclosing (outer functions)
#   -> Global (module level) -> Built-in (print, len...).
# - Assigning to a name inside a function makes it LOCAL to that function
#   (for the whole function), unless declared global or nonlocal.
# - global x: assign to the module-level x (avoid; prefer returning values).
# - nonlocal x: assign to x in the nearest enclosing function.
# - A CLOSURE is an inner function that remembers variables from its enclosing
#   function even after the outer function has returned.
# - Late binding: closures created in a loop see the variable's FINAL value.
#
# REAL-WORLD ANALOGY
# A backpack: when a hiker (inner function) leaves home (outer function),
# they carry the backpack (enclosed variables) and can still use what is inside.
#
# SYNTAX:
#   def outer():
#       count = 0
#       def inner():
#           nonlocal count
#           count += 1
#           return count
#       return inner
#
# SMALL WORKING EXAMPLE:
threshold = 0.5

def classify(p):
    return "positive" if p >= threshold else "negative"

def make_counter():
    count = 0
    def increment():
        nonlocal count
        count += 1
        return count
    return increment

def make_multiplier(factor):
    def multiply(x):
        return x * factor
    return multiply

counter = make_counter()
counter()
counter()
print(classify(0.7), counter())
double = make_multiplier(2)
print(double(21))
late = [lambda: i for i in range(3)]
fixed = [lambda i=i: i for i in range(3)]
print([f() for f in late], [f() for f in fixed])

# EXPLANATION (LINE BY LINE):
# threshold = 0.5             -> a global variable.
# classify reads threshold    -> reading a global is fine (G in LEGB).
# make_counter: count = 0     -> local to make_counter.
# nonlocal count; count += 1  -> modify the enclosing count, not a new local.
# return increment            -> return the inner function itself (not called).
# counter = make_counter(); counter() x3 -> count remembered: 1, 2, 3.
# make_multiplier(2)          -> a closure that remembers factor=2.
# late = [lambda: i ...]      -> every lambda sees the final i (2) -> [2, 2, 2].
# lambda i=i: i               -> default arguments capture the value now -> [0, 1, 2].
#
# COMMON MISTAKES:
# 1. UnboundLocalError: reading a global then assigning it in the same function.
# 2. Using global variables as hidden inputs/outputs.
# 3. Late-binding bugs with closures created in loops.
# 4. Shadowing built-ins (list, sum, id) with your own variables.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Create a global variable and a function with a local variable of the same
# name. Print both inside and outside the function to show they are separate.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Write make_accumulator() returning a function add(x) that keeps a running
# total and returns it. Create two accumulators and show they are independent.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Write make_rate_limiter(max_calls) that returns a function allow() which
# returns True for the first max_calls calls and False afterwards, plus a
# reset() function sharing the same state (return both as a tuple).
# Then write memoize(func) as a closure with a dict cache and use it on
# a slow recursive fibonacci. Compare call counts with and without memoization.

# YOUR CODE:

