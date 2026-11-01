# ======================================
# TOPIC: SETS
# LEVEL: BEGINNER
# ID: python.data-structures.sets
# ======================================

# INTRODUCTION
# A set stores unique values with no order. It answers questions like
# "have I seen this before?" and "what do these two groups share?" very fast.
#
# THEORY
# - No duplicates: adding an existing value does nothing.
# - Unordered: no indexing; iteration order is not guaranteed.
# - Items must be hashable (str, int, tuple - not list or dict).
# - Membership test (x in s) is O(1) on average - much faster than a list.
# - Set algebra: | union, & intersection, - difference, ^ symmetric difference.
# - Empty set is set(), NOT {} (that is an empty dict).
# - frozenset is an immutable set (can be a dict key).
#
# REAL-WORLD ANALOGY
# A guest list at a door: each name appears once, order does not matter,
# and the bouncer checks "is this name on the list?" instantly.
#
# SYNTAX:
#   s = {1, 2, 3};  empty = set()
#   s.add(4); s.discard(9); s.remove(1)   # remove raises KeyError if missing
#   a | b, a & b, a - b, a ^ b
#
# SMALL WORKING EXAMPLE:
ml_team = {"asha", "ben", "chen", "dev"}
web_team = {"ben", "eva", "dev"}
ml_team.add("asha")
print(len(ml_team))
print("both:", sorted(ml_team & web_team))
print("all:", sorted(ml_team | web_team))
print("only ML:", sorted(ml_team - web_team))
print("exactly one team:", sorted(ml_team ^ web_team))
labels = ["cat", "dog", "cat", "bird", "dog"]
print("unique labels:", sorted(set(labels)))
print("eva" in web_team, type({}), type(set()))

# EXPLANATION (LINE BY LINE):
# ml_team = {...}              -> a set of four names.
# .add("asha")                 -> already present, so nothing changes; len stays 4.
# ml_team & web_team           -> intersection: names in both sets.
# |                            -> union: everyone in either set.
# -                            -> difference: in ml_team but not web_team.
# ^                            -> in exactly one of the two sets.
# sorted(set(labels))          -> remove duplicates, then sort for stable printing.
# type({}) vs type(set())      -> dict vs set.
#
# COMMON MISTAKES:
# 1. Using {} for an empty set.
# 2. Expecting sets to keep insertion order or support s[0].
# 3. Putting lists inside sets -> TypeError: unhashable type.
# 4. Using remove() on a value that may be missing (use discard()).

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Create two sets of skills (yours and a job's requirements).
# Print the skills you have, the skills you are missing, and extra skills.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Write has_duplicates(items) using a set, and first_duplicate(items) that
# returns the first value seen twice (or None) in a single pass.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Implement jaccard_similarity(text_a, text_b) = |A & B| / |A | B| over the
# sets of lowercase words. Use it to find the most similar pair in a list of
# 5 short sentences. (Jaccard similarity is used in deduplicating datasets.)

# YOUR CODE:

