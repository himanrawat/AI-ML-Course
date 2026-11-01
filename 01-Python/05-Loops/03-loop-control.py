# ======================================
# TOPIC: LOOP CONTROL (BREAK, CONTINUE, ELSE, PASS)
# LEVEL: BEGINNER
# ID: python.loops.loop-control
# ======================================

# INTRODUCTION
# Real loops need finer control: skip a bad record, stop at the first match,
# or report when nothing was found.
#
# THEORY
# - break: leave the loop immediately.
# - continue: skip the rest of this iteration and go to the next one.
# - else on a loop: runs only if the loop finished WITHOUT break.
#   Read it as "no break". Useful for search loops.
# - pass: a placeholder that does nothing (an empty block is a syntax error).
# - break only exits the innermost loop. To exit nested loops, put them in a
#   function and return.
#
# REAL-WORLD ANALOGY
# Searching drawers for keys: skip drawers that are locked (continue), stop
# when you find the keys (break), and if you checked every drawer without
# finding them, say "keys not found" (else).
#
# SYNTAX:
#   for x in items:
#       if bad(x): continue
#       if found(x): break
#   else:
#       ...  # no break happened
#
# SMALL WORKING EXAMPLE:
records = [{"id": 1, "age": 30}, {"id": 2, "age": None}, {"id": 3, "age": 17}]
for record in records:
    if record["age"] is None:
        print("skipping", record["id"])
        continue
    if record["age"] < 18:
        print("found a minor:", record["id"])
        break
else:
    print("no minors found")

def find_pair(numbers, target):
    for i, a in enumerate(numbers):
        for b in numbers[i + 1:]:
            if a + b == target:
                return a, b
    return None

print(find_pair([2, 7, 11, 15], 9))
for _ in range(3):
    pass

# EXPLANATION (LINE BY LINE):
# if record["age"] is None: continue -> skip incomplete records.
# if record["age"] < 18: break       -> stop at the first minor.
# else: print("no minors found")     -> runs only when the loop did NOT break.
# def find_pair(...)                 -> nested loops inside a function.
# return a, b                        -> exits BOTH loops at once.
# return None                        -> nothing found.
# for _ in range(3): pass            -> "_" means "I don't need the value"; pass does nothing.
#
# COMMON MISTAKES:
# 1. Thinking loop-else means "if the loop never ran" - it actually runs
#    whenever there was no break (including empty loops).
# 2. Expecting break to exit all nested loops.
# 3. Using continue in a while loop BEFORE updating the counter -> infinite loop.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Loop from 1 to 20: skip multiples of 3 with continue, and stop completely
# when you reach a number greater than 15 with break. Print the numbers kept.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Write is_prime(n) using a for loop with else (no flags), then print all
# primes below 50.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Given a 2D grid (list of lists) of characters, write find_word_start(grid,
# letter) returning the (row, col) of the first occurrence, or None.
# Then write a data-cleaning loop over 10 messy records that skips invalid
# rows (continue), stops if an "END" sentinel row appears (break), and prints
# a summary of kept/skipped rows using loop-else to detect "no sentinel".

# YOUR CODE:

