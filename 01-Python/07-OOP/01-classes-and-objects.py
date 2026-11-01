# ======================================
# TOPIC: CLASSES AND OBJECTS
# LEVEL: INTERMEDIATE
# ID: python.oop.classes-objects
# ======================================

# INTRODUCTION
# Libraries like scikit-learn and PyTorch are built from classes: a model is
# an object that holds its parameters (data) and knows how to fit and predict
# (behaviour). Object-oriented programming bundles data and behaviour.
#
# THEORY
# - A CLASS is a blueprint; an OBJECT (instance) is one thing built from it.
# - __init__ runs when an object is created; it sets up instance attributes.
# - self is the instance the method is working on. Python passes it
#   automatically: obj.method(x) is really Class.method(obj, x).
# - Instance attributes (self.x) belong to one object.
#   Class attributes (defined in the class body) are shared by all instances.
# - There are no truly private attributes. Convention: _name means "internal".
#   __name triggers name mangling (rarely needed).
#
# REAL-WORLD ANALOGY
# A cookie cutter (class) and cookies (objects). Every cookie has the same
# shape, but each can have different toppings (attribute values).
#
# SYNTAX:
#   class ClassName:
#       class_attribute = value
#       def __init__(self, arg):
#           self.attribute = arg
#       def method(self):
#           return self.attribute
#
# SMALL WORKING EXAMPLE:
class BankAccount:
    bank_name = "PyBank"

    def __init__(self, owner, balance=0.0):
        self.owner = owner
        self._balance = balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("deposit must be positive")
        self._balance += amount
        return self._balance

    def withdraw(self, amount):
        if amount > self._balance:
            raise ValueError("insufficient funds")
        self._balance -= amount
        return self._balance

    def summary(self):
        return f"{self.owner} @ {self.bank_name}: {self._balance:.2f}"

alice = BankAccount("Alice", 100)
bob = BankAccount("Bob")
alice.deposit(50)
bob.deposit(20)
alice.withdraw(30)
print(alice.summary())
print(bob.summary())
print(isinstance(alice, BankAccount), BankAccount.bank_name)

# EXPLANATION (LINE BY LINE):
# class BankAccount:            -> define the blueprint.
# bank_name = "PyBank"          -> class attribute shared by all accounts.
# def __init__(self, owner, balance=0.0) -> runs on BankAccount("Alice", 100).
# self.owner / self._balance    -> instance attributes, one set per object.
# deposit/withdraw              -> methods that validate input and change state.
# raise ValueError(...)         -> refuse invalid operations.
# alice and bob                 -> two independent objects from one class.
# summary()                     -> reads both instance and class attributes.
#
# COMMON MISTAKES:
# 1. Forgetting self as the first method parameter.
# 2. Writing owner = owner in __init__ instead of self.owner = owner.
# 3. Using a mutable class attribute (items = []) shared by every instance.
# 4. Calling a method without parentheses (alice.summary prints a method object).

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Create a Student class with name and marks (a list). Add methods average()
# and add_mark(mark). Create two students and print their averages.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Create a ShoppingCart class with add_item(name, price, qty=1),
# remove_item(name), total() and a class attribute TAX_RATE. Prove that a
# mutable class attribute would be shared between carts, then fix it.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Create a MinMaxScaler class with fit(values), transform(values) and
# fit_transform(values), mimicking scikit-learn's design: fit learns min and
# max and stores them as self.min_ and self.max_; transform raises an error
# if called before fit. Test it on training data, then on new data.

# YOUR CODE:

