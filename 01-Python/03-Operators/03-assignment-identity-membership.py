# ======================================
# TOPIC: ASSIGNMENT, IDENTITY AND MEMBERSHIP OPERATORS
# LEVEL: BEGINNER
# ID: python.operators.assignment-identity-membership
# ======================================

# INTRODUCTION
# Three small groups of operators that appear in almost every program:
# updating a value, checking whether two names point to the same object,
# and checking whether a value is inside a collection.
#
# THEORY
# Augmented assignment: +=, -=, *=, /=, //=, %=, **= (Python has no ++ or --).
# Walrus := assigns inside an expression: if (n := len(data)) > 10: ...
# Identity: "is" / "is not" ask "same object in memory?" (id(a) == id(b)).
#   Use "is" ONLY for None, True, False and sentinel objects.
# Equality: == asks "same value?". Two different lists can be == but not "is".
# Membership: "in" / "not in" work on strings, lists, tuples, sets, dict KEYS.
#
# REAL-WORLD ANALOGY
# Two identical twins are "equal" (==) in appearance but are not the
# same person ("is"). "in" is checking whether a name is on the attendance list.
#
# SYNTAX:
#   total += 5
#   if value is None: ...
#   if key in mapping: ...
#
# SMALL WORKING EXAMPLE:
total = 10
total += 5
total *= 2
print(total)
a = [1, 2, 3]
b = [1, 2, 3]
c = a
print(a == b, a is b, a is c)
result = None
print(result is None)
config = {"lr": 0.01, "epochs": 5}
print("lr" in config, 0.01 in config, 0.01 in config.values())
print("gpt" in "chatgpt", 4 not in a)
data = [3, 8, 1, 9, 4]
if (n := len(data)) > 3:
    print(f"{n} items is enough")

# EXPLANATION (LINE BY LINE):
# total += 5; total *= 2   -> 15, then 30.
# a == b -> True           -> same contents.
# a is b -> False          -> two separate list objects.
# a is c -> True           -> c is another name for the same object.
# result is None           -> the correct way to test for None.
# "lr" in config           -> membership on a dict checks KEYS.
# 0.01 in config.values()  -> use .values() to search values.
# "gpt" in "chatgpt"       -> substring test.
# (n := len(data)) > 3     -> compute, store and test in one expression.
#
# COMMON MISTAKES:
# 1. Using "is" to compare numbers or strings (works sometimes by accident).
# 2. Writing x == None instead of x is None.
# 3. Expecting "in" on a dict to search values.
# 4. Trying x++ - Python has no increment operator (it is a SyntaxError).

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Start a counter at 0, add 10, multiply by 3, subtract 5, integer-divide by 2.
# Print the value after each step using augmented assignment.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Write check_access(user, allowed_roles, banned_users) where user is a dict
# with "name" and "role". Return a reason string using in / not in / is None
# checks (missing role, banned user, role not allowed, or "ok").

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Demonstrate why "is" is wrong for value comparison: build two equal large
# integers at runtime (e.g. int("1000") and 999 + 1) and compare with is / ==.
# Then use the walrus operator in a while loop that reads chunks from a list
# of lines until an empty chunk appears.

# YOUR CODE:

