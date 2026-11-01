# ======================================
# TOPIC: INHERITANCE AND POLYMORPHISM
# LEVEL: INTERMEDIATE
# ID: python.oop.inheritance
# ======================================

# INTRODUCTION
# Every PyTorch model inherits from nn.Module; every scikit-learn estimator
# shares a common base. Inheritance lets classes share and specialise behaviour.
#
# THEORY
# - class Child(Parent): Child gets all of Parent's methods and attributes.
# - Override a method by defining it again in Child.
# - super().method(...) calls the parent's version (commonly in __init__).
# - POLYMORPHISM: different classes answer the same method call in their own
#   way, so code can treat them uniformly (for shape in shapes: shape.area()).
# - Abstract base classes (abc.ABC + @abstractmethod) define methods that
#   subclasses MUST implement; you cannot instantiate the abstract class.
# - Multiple inheritance is allowed; the Method Resolution Order (Class.__mro__)
#   decides lookup order.
# - Prefer COMPOSITION (has-a) over inheritance (is-a) when unsure.
#
# REAL-WORLD ANALOGY
# All vehicles can move(); a car moves on roads, a boat on water. A driver can
# ask any vehicle to move without knowing which kind it is.
#
# SYNTAX:
#   class Child(Parent):
#       def __init__(self, a, b):
#           super().__init__(a)
#           self.b = b
#
# SMALL WORKING EXAMPLE:
from abc import ABC, abstractmethod

class Model(ABC):
    def __init__(self, name):
        self.name = name
        self.is_trained = False

    def fit(self, data):
        self.is_trained = True
        return self

    @abstractmethod
    def predict(self, x):
        ...

class ThresholdModel(Model):
    def __init__(self, name, threshold):
        super().__init__(name)
        self.threshold = threshold

    def predict(self, x):
        return int(x >= self.threshold)

class MeanModel(Model):
    def fit(self, data):
        self.mean_ = sum(data) / len(data)
        return super().fit(data)

    def predict(self, x):
        return self.mean_

models = [ThresholdModel("thresh", 0.5), MeanModel("mean")]
for m in models:
    m.fit([0.2, 0.4, 0.9])
    print(m.name, m.predict(0.7), m.is_trained)
try:
    Model("abstract")
except TypeError as error:
    print("cannot instantiate:", error)
print([cls.__name__ for cls in MeanModel.__mro__])

# EXPLANATION (LINE BY LINE):
# class Model(ABC)               -> abstract base class for all models.
# fit() in Model                 -> shared behaviour; returns self for chaining.
# @abstractmethod predict        -> subclasses must implement predict.
# ThresholdModel.__init__ calls super().__init__(name) -> reuse parent setup.
# MeanModel.fit overrides fit, then calls super().fit(data) to keep shared logic.
# for m in models: m.predict(0.7) -> polymorphism: same call, different behaviour.
# Model("abstract")              -> TypeError: abstract classes can't be created.
# MeanModel.__mro__              -> lookup order: MeanModel, Model, ABC, object.
#
# COMMON MISTAKES:
# 1. Forgetting super().__init__() so parent attributes are never set.
# 2. Deep inheritance chains that are hard to follow.
# 3. Using inheritance just to reuse one helper method (use composition).
# 4. Overriding a method with a different signature, breaking polymorphism.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Create Animal with speak() returning "...", and Dog/Cat subclasses that
# override speak(). Loop over a list of animals and print each sound.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Create an abstract Shape with area() and perimeter(), and Rectangle, Circle
# and Square (Square should inherit from Rectangle). Sort a list of shapes by
# area and print them.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Design a tiny text-preprocessing framework: abstract Step with
# apply(text) -> str, concrete steps (Lowercase, StripPunctuation,
# ReplaceNumbers), and a Pipeline class that HAS a list of steps (composition)
# and is itself a Step. Explain in a comment why Pipeline uses composition.

# YOUR CODE:

