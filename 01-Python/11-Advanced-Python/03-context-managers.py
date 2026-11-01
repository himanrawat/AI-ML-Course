# ======================================
# TOPIC: CONTEXT MANAGERS
# LEVEL: ADVANCED
# ID: python.advanced.context-managers
# ======================================

# INTRODUCTION
# "with open(...)" closes files; "with torch.no_grad():" turns off gradient
# tracking temporarily. Context managers guarantee setup and cleanup happen.
#
# THEORY
# - with obj as value: calls obj.__enter__() (its return value becomes value),
#   runs the block, then ALWAYS calls obj.__exit__(exc_type, exc, tb) -
#   even if the block raised an exception.
# - If __exit__ returns True, the exception is suppressed (use rarely).
# - contextlib.contextmanager turns a generator into a context manager:
#   code before yield = setup, after yield = cleanup (wrap yield in try/finally).
# - contextlib also offers suppress(ExceptionType), redirect_stdout, ExitStack.
# - Several managers: with open(a) as f1, open(b) as f2:
#
# REAL-WORLD ANALOGY
# A hotel room: check-in gives you a key (enter), you use the room, and
# checkout (exit) happens no matter how your stay went.
#
# SYNTAX:
#   class Manager:
#       def __enter__(self): return self
#       def __exit__(self, exc_type, exc, tb): ...
#
#   @contextmanager
#   def manager():
#       setup; try: yield value; finally: cleanup
#
# SMALL WORKING EXAMPLE:
import time
from contextlib import contextmanager, suppress

class Timer:
    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.elapsed = time.perf_counter() - self.start
        print(f"block took {self.elapsed:.4f}s (error: {exc_type.__name__ if exc_type else None})")
        return False

@contextmanager
def temporary_setting(settings, key, value):
    old = settings[key]
    settings[key] = value
    try:
        yield settings
    finally:
        settings[key] = old

with Timer() as t:
    total = sum(range(100_000))
settings = {"debug": False}
with temporary_setting(settings, "debug", True):
    print("inside:", settings)
print("after:", settings)
try:
    with Timer():
        raise RuntimeError("boom")
except RuntimeError:
    print("error still propagated")
with suppress(FileNotFoundError):
    open("does-not-exist.txt")
print("suppress swallowed the FileNotFoundError")

# EXPLANATION (LINE BY LINE):
# Timer.__enter__              -> records the start time and returns self (bound to t).
# Timer.__exit__(...)          -> computes elapsed time; receives error info if any.
# return False                 -> do not suppress exceptions.
# @contextmanager temporary_setting -> setup before yield, restore in finally.
# with temporary_setting(...)  -> debug is True only inside the block.
# with Timer(): raise RuntimeError -> __exit__ still runs, then the error propagates.
# suppress(FileNotFoundError)  -> intentionally ignore one specific error.
#
# COMMON MISTAKES:
# 1. Not using try/finally around yield, so cleanup is skipped on errors.
# 2. Returning True from __exit__ by accident, hiding exceptions.
# 3. Using the resource after the with block has closed it.
# 4. Forgetting __enter__ must return the object you want after "as".

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Use a with statement to write and read a file, then print f.closed inside
# and outside the block.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Write a class-based context manager ChangeDirectory(path) that switches
# os.getcwd() to path and restores the original directory on exit, even if
# an error occurs. Prove it restores correctly after an exception.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Write a @contextmanager called transaction(data: dict) that yields a COPY
# for modification and commits the changes back only if the block succeeds
# (rolls back on error). Then use contextlib.ExitStack to open a variable
# number of temporary files safely.

# YOUR CODE:

