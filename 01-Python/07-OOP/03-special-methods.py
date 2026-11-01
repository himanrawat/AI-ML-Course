# ======================================
# TOPIC: SPECIAL (DUNDER) METHODS
# LEVEL: INTERMEDIATE
# ID: python.oop.special-methods
# ======================================

# INTRODUCTION
# Why does len(dataset) work on a PyTorch Dataset, and a + b on NumPy arrays?
# Because those classes define special "dunder" (double underscore) methods
# that plug into Python's built-in syntax.
#
# THEORY
# Common special methods:
#   __repr__   unambiguous text for developers (shown in the REPL / lists)
#   __str__    friendly text for print()
#   __len__    len(obj)            __getitem__  obj[i], slicing, iteration
#   __iter__   for x in obj        __contains__ x in obj
#   __eq__     obj == other        __lt__       obj < other (enables sorting)
#   __add__    obj + other         __mul__      obj * other
#   __call__   obj(...)            __bool__     truthiness
# Return NotImplemented from operators when the other type is unsupported.
# If you define __eq__, also define __hash__ (or the object becomes unhashable).
#
# REAL-WORLD ANALOGY
# Universal plugs: if your appliance has the standard plug shape (the dunder
# method), it works in every socket (built-in syntax) without adapters.
#
# SYNTAX:
#   class Vector:
#       def __add__(self, other): ...
#       def __repr__(self): ...
#
# SMALL WORKING EXAMPLE:
import math

class Vector:
    def __init__(self, *components):
        self.components = tuple(components)

    def __repr__(self):
        return f"Vector{self.components}"

    def __len__(self):
        return len(self.components)

    def __getitem__(self, index):
        return self.components[index]

    def __add__(self, other):
        if not isinstance(other, Vector):
            return NotImplemented
        return Vector(*(a + b for a, b in zip(self, other, strict=True)))

    def __mul__(self, scalar):
        return Vector(*(a * scalar for a in self))

    def __eq__(self, other):
        return isinstance(other, Vector) and self.components == other.components

    def __hash__(self):
        return hash(self.components)

    def __abs__(self):
        return math.sqrt(sum(a * a for a in self))

v = Vector(3, 4)
w = Vector(1, 2)
print(v + w, v * 2, abs(v), len(v), v[0])
print(list(v), v == Vector(3, 4), {v, Vector(3, 4)})

# EXPLANATION (LINE BY LINE):
# __repr__        -> print(v) shows Vector(3, 4) instead of <object at 0x...>.
# __len__         -> len(v) works.
# __getitem__     -> v[0] works, and also makes v iterable (list(v), zip(self, other)).
# __add__         -> v + w adds component-wise; NotImplemented for other types.
# __mul__         -> v * 2 scales the vector.
# __eq__/__hash__ -> equal vectors compare equal and deduplicate in a set.
# __abs__         -> abs(v) returns the length: sqrt(3^2 + 4^2) = 5.0.
#
# COMMON MISTAKES:
# 1. Defining __str__ but not __repr__ (lists of objects still look ugly).
# 2. Defining __eq__ without __hash__ -> instances can't go in sets/dict keys.
# 3. Raising TypeError instead of returning NotImplemented in operators.
# 4. Mutating self in __add__ instead of returning a new object.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Create a Book class with __repr__ and __str__ and show where each is used
# (print(book) vs print([book])).

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Create a Money class (amount, currency) supporting +, comparison (<, ==),
# sorting, and raising an error when adding different currencies.
# Hint: functools.total_ordering can fill in the other comparisons.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Create a TextDataset class (like a PyTorch Dataset) wrapping a list of
# (text, label) pairs: support len(), indexing, slicing returning a new
# TextDataset, iteration, "in" for labels, and __call__(text) that returns
# the label of an exact matching text or None.

# YOUR CODE:

