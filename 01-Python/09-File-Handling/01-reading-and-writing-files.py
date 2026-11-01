# ======================================
# TOPIC: READING AND WRITING FILES
# LEVEL: INTERMEDIATE
# ID: python.files.read-write
# ======================================

# INTRODUCTION
# Datasets, logs, prompts and model outputs all live in files. Reading and
# writing files safely is a daily task in AI work.
#
# THEORY
# - open(path, mode, encoding="utf-8") returns a file object.
#   Modes: "r" read (default), "w" write (overwrites!), "a" append,
#          "x" create (fails if exists), add "b" for binary ("rb", "wb").
# - Always use "with open(...) as f:" - the file is closed automatically,
#   even if an error happens (it is a context manager).
# - Reading: f.read() whole file, f.readline() one line, for line in f
#   (memory-efficient, line by line), f.readlines() list of lines.
# - Writing: f.write(text) (no newline added), print(..., file=f).
# - Always pass encoding="utf-8" for text so behaviour is the same everywhere.
#
# REAL-WORLD ANALOGY
# Borrowing a library book: you check it out (open), read or annotate it,
# and the "with" statement is the librarian who makes sure it is returned.
#
# SYNTAX:
#   with open("file.txt", "w", encoding="utf-8") as f:
#       f.write("text\n")
#   with open("file.txt", encoding="utf-8") as f:
#       for line in f: ...
#
# SMALL WORKING EXAMPLE:
import os
import tempfile

folder = tempfile.mkdtemp()
path = os.path.join(folder, "training_log.txt")
with open(path, "w", encoding="utf-8") as f:
    f.write("epoch,loss\n")
    for epoch, loss in enumerate([0.9, 0.6, 0.4], start=1):
        f.write(f"{epoch},{loss}\n")
with open(path, "a", encoding="utf-8") as f:
    print("4,0.35", file=f)
with open(path, encoding="utf-8") as f:
    header = f.readline().strip()
    losses = [float(line.split(",")[1]) for line in f]
print(header, losses)
print(f.closed)
try:
    open(os.path.join(folder, "missing.txt"), encoding="utf-8")
except FileNotFoundError as error:
    print("not found:", os.path.basename(error.filename))

# EXPLANATION (LINE BY LINE):
# tempfile.mkdtemp()           -> a throwaway folder so the example leaves no mess.
# open(path, "w", ...)         -> create/overwrite the file for writing.
# f.write(f"{epoch},{loss}\n") -> write() needs explicit newlines.
# open(path, "a")              -> append mode adds to the end.
# print("4,0.35", file=f)      -> print can write to files (adds the newline).
# f.readline()                 -> read the header line only.
# for line in f                -> continue reading the remaining lines lazily.
# f.closed                     -> True: "with" closed the file for us.
# FileNotFoundError            -> raised when reading a file that does not exist.
#
# COMMON MISTAKES:
# 1. Opening with "w" when you meant "a" - the file is wiped.
# 2. Forgetting newline characters when using write().
# 3. Not specifying encoding -> errors with non-English text on some systems.
# 4. Reading a 10 GB file with f.read() instead of iterating line by line.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Write 5 lines of notes to notes.txt (inside a temporary folder), then read
# them back and print each line with its line number.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Write count_file_stats(path) returning the number of lines, words and
# characters (like the Unix wc command), reading the file line by line.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Write split_file(path, lines_per_chunk, out_dir) that splits a large text
# file into numbered chunk files without loading the whole file into memory,
# and merge_files(paths, out_path) that joins them back. Verify that the
# merged file is identical to the original.

# YOUR CODE:

