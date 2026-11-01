# ======================================
# TOPIC: IMPORTS AND THE STANDARD LIBRARY
# LEVEL: INTERMEDIATE
# ID: python.modules.imports-stdlib
# ======================================

# INTRODUCTION
# Nobody writes everything from scratch. Python ships a large standard library,
# and the AI ecosystem (NumPy, pandas, PyTorch) is reached through imports.
#
# THEORY
# - A MODULE is a .py file; a PACKAGE is a folder of modules.
# - import math                 -> use as math.sqrt(2)
#   from math import sqrt, pi   -> use directly as sqrt(2)
#   import numpy as np          -> alias (community conventions: np, pd, plt)
# - Avoid "from module import *" - it hides where names come from.
# - Python searches for modules in sys.path: the script's folder first,
#   then installed packages. A file named json.py in your folder will SHADOW
#   the real json module - never name files after modules you use.
# - A module's code runs once, the first time it is imported (then cached in
#   sys.modules).
# - Import order convention: standard library, third-party, your own modules.
# Handy standard library modules: math, random, statistics, datetime,
# collections, itertools, functools, pathlib, json, csv, re, os, sys,
# time, logging, typing, dataclasses, subprocess, urllib.
#
# REAL-WORLD ANALOGY
# A toolbox shelf: instead of forging a hammer, you take it from the shelf
# (import). An alias is a nickname written on the tool.
#
# SYNTAX:
#   import module
#   import module as alias
#   from module import name1, name2
#
# SMALL WORKING EXAMPLE:
import random
import re
import statistics
import sys
from collections import Counter
from datetime import date, timedelta

random.seed(7)
sample = [random.randint(1, 100) for _ in range(8)]
print(sample, statistics.mean(sample), statistics.median(sample))
deadline = date(2026, 12, 31) - timedelta(days=30)
print(deadline.isoformat())
text = "Contact asha@example.com or ben@test.org today"
emails = re.findall(r"[\w.]+@[\w.]+\.\w+", text)
print(emails)
print(Counter("mississippi").most_common(2))
print("math" in sys.modules, sys.version_info >= (3, 10))

# EXPLANATION (LINE BY LINE):
# random.seed(7)                    -> makes the "random" numbers reproducible.
# statistics.mean / median          -> simple statistics without extra libraries.
# date(...) - timedelta(days=30)    -> date arithmetic.
# re.findall(pattern, text)         -> regular expressions find all email-like strings.
# Counter("mississippi")            -> counts characters.
# sys.modules                       -> cache of already-imported modules.
# sys.version_info >= (3, 10)       -> check the Python version at runtime.
#
# COMMON MISTAKES:
# 1. Naming your file random.py / json.py / numpy.py (shadows the real module).
# 2. Circular imports (a imports b, b imports a).
# 3. "from x import *" polluting your namespace.
# 4. Forgetting to install third-party packages in the ACTIVE virtual env.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Use the random module to simulate 1000 dice rolls (seeded) and print how
# often each face appeared using collections.Counter.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Use datetime to compute how many days remain until your next birthday and
# which weekday it falls on. Use itertools to print all pairs (combinations)
# of 4 team members.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Create (with pathlib, in a temporary folder) a file named json.py containing
# a print statement, add that folder to sys.path[0], and import json in a
# subprocess (subprocess.run with sys.executable, cwd set to that folder) to
# SHOW the shadowing problem. Explain in comments how to avoid it.

# YOUR CODE:

