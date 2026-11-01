# ======================================
# TOPIC: STRINGS
# LEVEL: BEGINNER
# ID: python.variables.strings
# ======================================

# INTRODUCTION
# Text is everywhere in AI: prompts, documents, labels, model output.
# Strings are Python's type for text, and you will use them constantly.
#
# THEORY
# A string (str) is an immutable sequence of Unicode characters.
# - Quotes: 'single', "double", """triple for multi-line""".
# - Indexing: s[0] is the first character, s[-1] the last.
# - Slicing: s[start:stop:step] - stop is NOT included. s[::-1] reverses.
# - Immutable: methods return NEW strings; the original never changes.
# - f-strings embed expressions: f"{name} is {age}", f"{price:.2f}".
# - Useful methods: lower, upper, strip, split, join, replace, startswith,
#   endswith, find, count, isdigit.
#
# REAL-WORLD ANALOGY
# A string is a row of letter tiles glued to a board. You can read any tile
# or copy a section, but to "change" it you must make a new board.
#
# SYNTAX:
#   s[index], s[start:stop:step]
#   f"text {expression:format_spec}"
#   separator.join(list_of_strings)
#
# SMALL WORKING EXAMPLE:
sentence = "  Machine Learning is fun  "
clean = sentence.strip()
words = clean.split()
print(clean.lower())
print(words)
print("-".join(words))
print(clean[0], clean[-1], clean[:7], clean[::-1])
score = 0.91234
print(f"Model: {clean[:16]!r} | accuracy: {score:.1%} | words: {len(words)}")
print("learn" in clean.lower(), clean.count("n"))

# EXPLANATION (LINE BY LINE):
# sentence = "  ...  "  -> a string with extra spaces at both ends.
# .strip()              -> returns a copy without leading/trailing whitespace.
# .split()              -> splits on any whitespace into a list of words.
# .lower()              -> lowercase copy; "clean" itself is unchanged.
# "-".join(words)       -> join is called ON the separator, with the list as argument.
# clean[0], clean[-1]   -> first and last characters.
# clean[:7]             -> characters 0..6 ("Machine").
# clean[::-1]           -> step -1 walks backwards: the reversed string.
# f"...{score:.1%}"     -> formats 0.91234 as "91.2%". !r shows the repr (with quotes).
# "learn" in ...        -> substring test returns True/False.
#
# COMMON MISTAKES:
# 1. Trying s[0] = "X" -> TypeError (strings are immutable).
# 2. Calling s.upper() and expecting s to change - assign the result.
# 3. Writing list.join("-") instead of "-".join(list).
# 4. Building big strings with += in a loop (slow) instead of "".join(parts).
# 5. Forgetting the f in f-strings: "{name}" prints literally.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Given text = "python for ai", print it in UPPER case, Title Case,
# its length, and the word "for" replaced by "and".

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Write is_palindrome(text) that ignores case, spaces and punctuation.
# "A man, a plan, a canal: Panama" -> True. Use str methods and slicing.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Write a simple tokenizer tokenize(text) that lowercases text, removes
# punctuation (use the string module's string.punctuation), splits into words,
# and returns the list. Then print the 3 most common words in a paragraph
# along with counts, formatted in aligned columns using f-string widths.

# YOUR CODE:

