# ======================================
# TOPIC: FOR LOOPS
# LEVEL: BEGINNER
# ID: python.loops.for-loops
# ======================================

# INTRODUCTION
# Repeating work over data is the heart of programming: every row, every
# file, every training epoch. The for loop visits each item of a collection.
#
# THEORY
# - for item in iterable: visits each item of a list, str, tuple, dict, file...
# - range(stop), range(start, stop, step) produce numbers; stop is excluded.
# - enumerate(items, start=0) gives (index, item) pairs - no manual counters.
# - zip(a, b) pairs items from several iterables (stops at the shortest;
#   zip(..., strict=True) raises if lengths differ).
# - Looping a dict gives keys; use .items() for key/value pairs.
# - reversed() and sorted() let you loop in other orders.
#
# REAL-WORLD ANALOGY
# A teacher marking a stack of exam papers: take the top paper, mark it,
# move to the next, until the stack is empty.
#
# SYNTAX:
#   for item in items:
#       ...
#   for i, item in enumerate(items, start=1): ...
#   for a, b in zip(list_a, list_b): ...
#
# SMALL WORKING EXAMPLE:
epochs = 3
for epoch in range(1, epochs + 1):
    print("epoch", epoch)
labels = ["cat", "dog", "bird"]
for i, label in enumerate(labels):
    print(i, label)
predictions = ["cat", "cat", "bird"]
correct = 0
for predicted, actual in zip(predictions, labels, strict=True):
    if predicted == actual:
        correct += 1
print(f"accuracy: {correct / len(labels):.2f}")
prices = {"apple": 40, "mango": 90}
for fruit, price in prices.items():
    print(f"{fruit}: {price}")
for n in range(10, 0, -3):
    print(n, end=" ")
print()

# EXPLANATION (LINE BY LINE):
# range(1, epochs + 1)          -> 1, 2, 3 (stop value excluded, so + 1).
# enumerate(labels)             -> (0, "cat"), (1, "dog"), (2, "bird").
# zip(predictions, labels, strict=True) -> pairs items; raises if lengths differ.
# if predicted == actual: correct += 1  -> count matches.
# correct / len(labels)         -> 2/3 = 0.67 accuracy.
# prices.items()                -> key/value pairs from a dict.
# range(10, 0, -3)              -> 10, 7, 4, 1 counting down.
# print(n, end=" ")             -> keep printing on the same line.
#
# COMMON MISTAKES:
# 1. Using for i in range(len(items)) when enumerate is clearer.
# 2. Off-by-one errors with range's excluded stop value.
# 3. Modifying a list while iterating over it.
# 4. Expecting zip to warn about different lengths (use strict=True).

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Print the multiplication table of 7 from 7 x 1 to 7 x 10.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Given two lists, names and scores, print a ranked leaderboard
# ("1. Asha - 95") sorted from highest to lowest score using zip,
# sorted and enumerate.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Compute a confusion matrix for labels ["cat", "dog", "bird"] from two lists
# y_true and y_pred (10 items each) using nested dicts and for loops.
# Print it as an aligned table, then compute precision and recall for "cat".

# YOUR CODE:

