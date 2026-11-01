# ======================================
# TOPIC: PROPERTIES, CLASS METHODS AND STATIC METHODS
# LEVEL: INTERMEDIATE
# ID: python.oop.properties-classmethods
# ======================================

# INTRODUCTION
# Good classes protect their data and offer convenient ways to create objects.
# Properties validate attributes; class methods give alternative constructors
# like pd.DataFrame.from_dict or Model.from_pretrained.
#
# THEORY
# - @property turns a method into a read-only attribute: obj.area (no parentheses).
# - @name.setter adds validation when assigning: obj.radius = -1 -> error.
# - @classmethod receives the CLASS (cls) instead of an instance. Used for
#   alternative constructors: Config.from_dict(d).
# - @staticmethod receives neither; it is a plain function grouped in the class.
# - Use properties when an attribute needs computing or validating; plain
#   attributes are fine otherwise (no Java-style getters/setters).
#
# REAL-WORLD ANALOGY
# A thermostat: you read the temperature like a value (property), but when you
# set it, the device checks the range first (setter). The factory that builds
# thermostats from a spec sheet is a class method.
#
# SYNTAX:
#   @property
#   def name(self): return self._name
#   @name.setter
#   def name(self, value): ...
#   @classmethod
#   def from_x(cls, x): return cls(...)
#
# SMALL WORKING EXAMPLE:
class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius

    @property
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("below absolute zero")
        self._celsius = value

    @property
    def fahrenheit(self):
        return self._celsius * 9 / 5 + 32

    @classmethod
    def from_fahrenheit(cls, f):
        return cls((f - 32) * 5 / 9)

    @staticmethod
    def is_fever(celsius):
        return celsius >= 38

t = Temperature(25)
print(t.celsius, t.fahrenheit)
t.celsius = 30
print(t.fahrenheit)
body = Temperature.from_fahrenheit(100.4)
print(round(body.celsius, 1), Temperature.is_fever(body.celsius))
try:
    t.celsius = -300
except ValueError as error:
    print("rejected:", error)

# EXPLANATION (LINE BY LINE):
# self.celsius = celsius in __init__ -> goes through the setter, so it is validated too.
# @property celsius / @celsius.setter -> reading and writing use these methods.
# fahrenheit property                -> computed on demand, no setter = read-only.
# @classmethod from_fahrenheit(cls, f) -> alternative constructor; cls is Temperature.
# @staticmethod is_fever             -> utility related to the class, needs no self.
# t.celsius = -300                   -> setter raises ValueError.
#
# COMMON MISTAKES:
# 1. Naming the stored attribute the same as the property (self.celsius inside
#    the setter) -> infinite recursion. Store it as self._celsius.
# 2. Calling a property with parentheses: t.fahrenheit().
# 3. Using staticmethod when the method needs the class (use classmethod).
# 4. Writing getters/setters for every attribute "just in case".

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Create a Rectangle with width and height and read-only properties area and
# perimeter. Show that assigning to area raises an AttributeError.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Create a User class with an email property whose setter validates the format
# (contains "@" and a "." after it) and stores it lowercased. Add a classmethod
# from_csv_row("name,email") and a staticmethod is_valid_email(email).

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Create a TrainingConfig class with learning_rate (0 < lr <= 1), batch_size
# (power of two) and epochs (positive int) validated by properties.
# Add classmethods from_dict(d) and from_json(text), a to_dict() method, and
# a class attribute that counts how many configs have been created.

# YOUR CODE:

