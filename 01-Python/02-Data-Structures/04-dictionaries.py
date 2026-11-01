# ======================================
# TOPIC: DICTIONARIES
# LEVEL: BEGINNER
# ID: python.data-structures.dictionaries
# ======================================

# INTRODUCTION
# A dictionary maps keys to values: a word to its meaning, a user id to a
# profile. JSON from APIs becomes nested dictionaries in Python.
#
# THEORY
# - Key -> value pairs. Keys are unique and must be hashable (str, int, tuple).
# - Keeps insertion order (guaranteed since Python 3.7).
# - d[key] raises KeyError if missing; d.get(key, default) does not.
# - Loop with .keys(), .values(), .items().
# - Merge: d1 | d2 (right side wins on conflicts), or d1.update(d2).
# - setdefault and collections.defaultdict help when building groups/counts.
# - collections.Counter counts things.
#
# REAL-WORLD ANALOGY
# A phone contact list: you look up a NAME (key) to get a NUMBER (value).
# Each name appears once; updating a name replaces the number.
#
# SYNTAX:
#   d = {"name": "Asha", "age": 30}
#   d["city"] = "Pune"; del d["age"]
#   for key, value in d.items(): ...
#
# SMALL WORKING EXAMPLE:
from collections import Counter, defaultdict

model = {"name": "classifier", "accuracy": 0.91, "tags": ["nlp"]}
model["epochs"] = 10
model["accuracy"] = 0.93
print(model.get("loss", "not recorded"))
for key, value in model.items():
    print(f"{key:>9}: {value}")
defaults = {"epochs": 5, "batch_size": 32}
config = defaults | {"epochs": 20}
print(config)
words = "the cat and the hat and the bat".split()
print(Counter(words).most_common(2))
by_letter = defaultdict(list)
for w in words:
    by_letter[w[0]].append(w)
print(dict(by_letter))

# EXPLANATION (LINE BY LINE):
# model = {...}               -> keys are strings; values have mixed types.
# model["epochs"] = 10        -> adds a new key.
# model["accuracy"] = 0.93    -> overwrites an existing key.
# .get("loss", "...")         -> returns the default instead of raising KeyError.
# for key, value in .items()  -> loop over pairs; {key:>9} right-aligns the key.
# defaults | {...}            -> new merged dict; the right side's epochs wins.
# Counter(words).most_common(2) -> the two most frequent words with counts.
# defaultdict(list)           -> missing keys automatically start as [].
# by_letter[w[0]].append(w)   -> group words by their first letter.
#
# COMMON MISTAKES:
# 1. d[key] on a missing key -> KeyError (use .get or "in").
# 2. Using a list as a key -> TypeError.
# 3. Changing a dict's size while looping over it -> RuntimeError.
# 4. Assuming dict.update returns a dict (it returns None).

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Create a dict describing a book (title, author, year, rating).
# Update the rating, add a "genre", remove "year", and print every pair.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Write word_frequencies(text) WITHOUT Counter, returning a dict of word -> count
# (lowercase, punctuation removed). Then print the top 3 words using sorted()
# with a key function.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Given a list of records like {"name": "Asha", "dept": "ML", "salary": 120}
# (at least 6 records), build a summary dict:
# {dept: {"count": n, "avg_salary": x, "people": [names sorted]}}.
# Also write deep_get(data, "a.b.c", default=None) that safely reads nested keys.

# YOUR CODE:

