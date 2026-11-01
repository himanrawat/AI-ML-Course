# ======================================
# TOPIC: LISTS
# LEVEL: BEGINNER
# ID: python.data-structures.lists
# ======================================

# INTRODUCTION
# A list stores many values in order: a batch of scores, rows of data,
# the messages in a chat. It is Python's most used collection.
#
# THEORY
# - Ordered: items keep their position; indexes start at 0.
# - Mutable: you can add, remove and change items in place.
# - Can hold mixed types, including other lists (nested lists).
# - Slicing works like strings: nums[1:4], nums[::-1].
# - Key methods: append, extend, insert, pop, remove, sort, reverse, index, count.
# - sorted(lst) returns a NEW sorted list; lst.sort() sorts IN PLACE and returns None.
# - Assigning b = a does NOT copy: both names point to the same list.
#   Use a.copy() or a[:] for a shallow copy, copy.deepcopy for nested lists.
#
# REAL-WORLD ANALOGY
# A train of numbered carriages. You can add carriages, remove them,
# or swap the cargo in carriage 3 without building a new train.
#
# SYNTAX:
#   items = [1, 2, 3]
#   items.append(4); items[0] = 10; del items[1]
#   new_list = sorted(items, key=..., reverse=True)
#
# SMALL WORKING EXAMPLE:
scores = [72, 95, 88]
scores.append(60)
scores.extend([91, 77])
scores[0] = 75
highest = max(scores)
top_three = sorted(scores, reverse=True)[:3]
alias = scores
backup = scores.copy()
scores.pop()
print(scores, highest, top_three)
print("alias sees the change:", alias)
print("backup does not:", backup)
names = ["Zara", "amit", "Bea"]
print(sorted(names), sorted(names, key=str.lower))

# EXPLANATION (LINE BY LINE):
# scores = [72, 95, 88]     -> create a list of three ints.
# .append(60)               -> add ONE item at the end.
# .extend([91, 77])         -> add EACH item from another list.
# scores[0] = 75            -> replace the first item in place.
# max(scores)               -> built-in that works on any iterable.
# sorted(...)[:3]           -> new sorted list, then slice the first three.
# alias = scores            -> second name for the SAME list (no copy).
# backup = scores.copy()    -> an independent shallow copy.
# scores.pop()              -> removes and returns the last item; alias changes too.
# sorted(names, key=str.lower) -> sort case-insensitively using a key function.
#
# COMMON MISTAKES:
# 1. new = lst.sort() -> new is None. Use sorted(lst) for a new list.
# 2. Using b = a and being surprised that changing b changes a.
# 3. Removing items from a list while looping over it (skips items).
# 4. Using append when you meant extend (creates a nested list).
# 5. IndexError from accessing lst[len(lst)].

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Create a list of 5 favourite topics. Add one, remove one, change one,
# then print the list, its length, and the first and last items.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Write remove_duplicates(items) that returns a new list without duplicates
# while KEEPING the original order. [3, 1, 3, 2, 1] -> [3, 1, 2].
# Do not modify the input list.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Write chunk(items, size) that splits a list into batches of the given size
# (the last batch may be smaller). chunk([1..7], 3) -> [[1,2,3],[4,5,6],[7]].
# Then demonstrate the shallow-copy trap with a nested list:
# grid = [[0] * 3] * 3 and explain (in a comment) why changing one cell
# changes three, then build the grid correctly.

# YOUR CODE:

