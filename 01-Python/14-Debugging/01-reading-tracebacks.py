# ======================================
# TOPIC: READING TRACEBACKS
# LEVEL: BEGINNER
# ID: python.debugging.tracebacks
# ======================================

# INTRODUCTION
# Errors are not failures - they are messages. A traceback tells you exactly
# what went wrong and where. Reading them quickly is a core debugging skill.
#
# THEORY
# A traceback lists the chain of function calls that led to the error:
# - Read it from the BOTTOM up. The last line is the exception type and message.
# - The lines above show each call: file, line number, function, and code.
#   The bottom-most frame is where the error was raised; frames above it are
#   the callers.
# - "During handling of the above exception, another exception occurred" and
#   "The above exception was the direct cause..." show chained errors.
# - Common types: NameError (typo / undefined), TypeError (wrong type or wrong
#   number of arguments), AttributeError (no such attribute - often None),
#   KeyError, IndexError, ValueError, ImportError/ModuleNotFoundError.
# - Strategy: read the message, find the first frame in YOUR code, inspect the
#   values on that line, form a hypothesis, test it.
#
# REAL-WORLD ANALOGY
# A trail of footprints leading to a broken vase: the last footprint is where
# it broke; following the trail backwards shows how you got there.
#
# SYNTAX:
#   import traceback
#   traceback.print_exc()        # inside except: print the full traceback
#   traceback.format_exc()       # same, as a string (for logs)
#
# SMALL WORKING EXAMPLE:
import traceback

def load_user(users, user_id):
    return users.get(user_id)

def get_email_domain(users, user_id):
    user = load_user(users, user_id)
    return user["email"].split("@")[1]

users = {1: {"email": "asha@example.com"}, 2: {"name": "no email"}}
print(get_email_domain(users, 1))
for bad_id in (2, 3):
    try:
        get_email_domain(users, bad_id)
    except (KeyError, TypeError):
        lines = traceback.format_exc().strip().splitlines()
        print(f"--- user {bad_id}: last line -> {lines[-1]}")
        print("    raised at ->", lines[-3].strip())

# EXPLANATION (LINE BY LINE):
# load_user returns None for unknown ids (dict.get).
# get_email_domain assumes the user exists AND has an email.
# user 1 -> works: "example.com".
# user 2 -> KeyError: 'email' (the dict exists but has no "email" key).
# user 3 -> TypeError: 'NoneType' object is not subscriptable
#           (load_user returned None; None["email"] fails).
# traceback.format_exc()  -> the full traceback text inside an except block.
# lines[-1]               -> the exception line; lines[-3] -> the file/line
#                            where it happened (the line above shows the code).
#
# COMMON MISTAKES:
# 1. Reading only the top of the traceback.
# 2. Guessing instead of printing the actual values on the failing line.
# 3. "Fixing" the symptom (try/except around it) instead of the cause.
# 4. Ignoring the NoneType clue - it usually means a function returned None.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Write three tiny snippets that raise NameError, TypeError and IndexError.
# Catch each, print the exception type and message, and write a comment on
# how you would fix each.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Write a chain of 3 functions (parse -> transform -> report) where the
# deepest one fails on bad input. Print the full traceback with
# traceback.print_exc() and annotate in comments which frame is the cause.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Write a function debug_summary(exc) that walks exc.__traceback__ (use
# traceback.extract_tb) and returns a compact list of "file:line in function"
# entries plus the chained cause (exc.__cause__ / __context__). Test it on an
# error raised with "raise ... from ...".

# YOUR CODE:

