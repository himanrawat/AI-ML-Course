# ======================================
# TOPIC: ITERATORS AND GENERATORS
# LEVEL: ADVANCED
# ID: python.advanced.iterators-generators
# ======================================

# INTRODUCTION
# Datasets are often too big for memory. Generators produce items one at a time,
# on demand - the idea behind data loaders that stream batches to a model.
#
# THEORY
# - An ITERABLE can be looped over (list, str, dict, file). iter(obj) gives
#   an ITERATOR, which returns items one by one via next() and raises
#   StopIteration when exhausted.
# - The iterator protocol: __iter__ returns the iterator, __next__ returns
#   the next item.
# - A GENERATOR FUNCTION uses yield. Calling it returns a generator (an
#   iterator) and runs NOTHING yet. Each next() runs until the next yield,
#   then pauses, keeping local variables.
# - Generators are LAZY and SINGLE-USE: once exhausted, they stay empty.
# - yield from other_iterable delegates to another iterable.
# - itertools provides lazy building blocks: islice, chain, count, cycle,
#   groupby, batched (Python 3.12+).
#
# REAL-WORLD ANALOGY
# A ticket dispenser at a bank: it does not print all tickets in advance;
# it prints the next number only when someone presses the button.
#
# SYNTAX:
#   def gen():
#       yield value
#   it = iter(items); next(it)
#   (x * 2 for x in items)   # generator expression
#
# SMALL WORKING EXAMPLE:
from itertools import batched, islice

def read_records(n):
    for i in range(n):
        print(f"  loading record {i}")
        yield {"id": i, "value": i * i}

def batches(iterable, size):
    yield from batched(iterable, size)

stream = read_records(5)
print(type(stream).__name__)
print(next(stream))
for batch in batches(stream, 2):
    print("batch:", [r["id"] for r in batch])
print("exhausted:", list(stream))

def countdown(n):
    while n > 0:
        yield n
        n -= 1

print(list(islice(countdown(1_000_000), 3)))
numbers = iter([10, 20])
print(next(numbers), next(numbers), next(numbers, "done"))

# EXPLANATION (LINE BY LINE):
# def read_records(n): ... yield {...} -> a generator function.
# stream = read_records(5)  -> nothing is loaded yet (no "loading" printed).
# next(stream)              -> runs until the first yield: loads record 0.
# batches(stream, 2)        -> continues from record 1, grouping in pairs.
# list(stream) after the loop -> [] because generators are single-use.
# islice(countdown(1_000_000), 3) -> takes only 3 items; the rest never runs.
# next(numbers, "done")     -> a default instead of raising StopIteration.
#
# COMMON MISTAKES:
# 1. Iterating a generator twice and getting nothing the second time.
# 2. Calling len() on a generator (TypeError).
# 3. Expecting code in a generator function to run when it is called.
# 4. Converting huge generators to lists, defeating the purpose.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Write a generator even_numbers(limit) and print the first 10 values.
# Show what happens when you call next() after it is exhausted.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Write a class Countdown implementing __iter__ and __next__ (no yield).
# Then write the same with a generator function and compare the amount of code.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Build a lazy data pipeline from generators: read_lines(path) ->
# parse_json(lines) -> filter_valid(records) -> batch(records, size).
# Process a temporary JSONL file with 10,000 records and show, with
# tracemalloc, that peak memory stays small compared to loading a list.

# YOUR CODE:

