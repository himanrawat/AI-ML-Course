# ======================================
# TOPIC: HANDLING EXCEPTIONS (TRY / EXCEPT)
# LEVEL: INTERMEDIATE
# ID: python.exceptions.try-except
# ======================================

# INTRODUCTION
# Real programs meet bad data, missing files and failing networks. Exceptions
# are Python's way of signalling errors; handling them keeps programs running.
#
# THEORY
# - When an error happens, Python RAISES an exception object (ValueError,
#   KeyError, FileNotFoundError...). If nothing catches it, the program stops
#   and prints a traceback.
# - try: risky code
#   except SomeError as e: handle that specific error
#   else: runs only if NO exception happened
#   finally: ALWAYS runs (cleanup), even after return or an unhandled error
# - Catch SPECIFIC exceptions. A bare "except:" or "except Exception:" hides bugs.
# - Multiple types: except (KeyError, IndexError) as e:
# - Exceptions form a hierarchy: FileNotFoundError is a subclass of OSError.
# - EAFP style ("easier to ask forgiveness than permission"): try the operation
#   and handle failure, instead of checking every condition first (LBYL).
#
# REAL-WORLD ANALOGY
# A trapeze artist with a safety net: the act (try) usually succeeds; if they
# fall (exception), the net (except) catches them; the crew always packs up
# afterwards (finally).
#
# SYNTAX:
#   try:
#       ...
#   except ValueError as error:
#       ...
#   else:
#       ...
#   finally:
#       ...
#
# SMALL WORKING EXAMPLE:
def parse_score(text):
    try:
        value = float(text)
    except ValueError:
        print(f"  not a number: {text!r}")
        return None
    else:
        return min(max(value, 0.0), 1.0)
    finally:
        print(f"  parsed {text!r}")

for raw in ["0.82", "high", "1.7"]:
    print(parse_score(raw))

config = {"lr": 0.01}
try:
    batch = config["batch_size"]
except KeyError as error:
    print("missing key:", error)
    batch = 32
print("batch size:", batch)

try:
    1 / 0
except (ZeroDivisionError, OverflowError) as error:
    print(type(error).__name__, "-", error)

# EXPLANATION (LINE BY LINE):
# try: value = float(text)        -> may raise ValueError for bad text.
# except ValueError: ... return None -> handle only that error type.
# else: return clamped value      -> runs only when float() succeeded.
# finally: print(...)             -> runs in EVERY case, even after return.
# config["batch_size"]            -> raises KeyError; we fall back to 32.
# except (ZeroDivisionError, OverflowError) -> one handler for several types.
# type(error).__name__            -> the exception class name for logging.
#
# COMMON MISTAKES:
# 1. Bare except: catches everything, even KeyboardInterrupt, hiding bugs.
# 2. Wrapping huge blocks in one try - you can't tell what failed.
# 3. Silently passing (except: pass) without logging.
# 4. Catching an exception just to re-raise it unchanged.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Write safe_divide(a, b) that returns a / b, or None with a printed warning
# when b is zero or the inputs are not numbers (handle both errors).

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Write average_of_column(rows, column) where rows is a list of dicts.
# Skip rows where the column is missing or not numeric, count how many rows
# were skipped and why (KeyError vs ValueError), and return (average, report).

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Demonstrate the order of execution of try/except/else/finally by writing a
# function with print statements in every block, and call it in three
# scenarios: success, handled error, unhandled error (catch that one outside).
# Then show that a return inside finally overrides an earlier return - and
# explain in a comment why you should never do that.

# YOUR CODE:

