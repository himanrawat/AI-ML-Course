# ======================================
# TOPIC: FUNCTION ARGUMENTS
# LEVEL: INTERMEDIATE
# ID: python.functions.arguments
# ======================================

# INTRODUCTION
# ML libraries have functions with dozens of options: train_test_split(X, y,
# test_size=0.2, random_state=42). Understanding argument kinds lets you read
# and design such APIs.
#
# THEORY
# - Positional arguments: matched by position.
# - Keyword arguments: matched by name: f(x=1). Order no longer matters.
# - Default values: def f(x, verbose=False). Parameters with defaults go last.
# - *args collects extra positional arguments into a TUPLE.
# - **kwargs collects extra keyword arguments into a DICT.
# - Keyword-only parameters come after * : def f(a, *, strict=True).
# - Positional-only parameters come before / : def f(a, b, /).
# - Unpacking when calling: f(*my_list), f(**my_dict).
# - MUTABLE DEFAULT TRAP: defaults are evaluated ONCE, when the function is
#   defined. def f(items=[]) shares one list across calls. Use None instead.
#
# REAL-WORLD ANALOGY
# Ordering a pizza: the size is required, toppings are extra items (*args),
# and special instructions are named notes (**kwargs) like "extra_cheese=True".
#
# SYNTAX:
#   def f(pos_only, /, normal, *args, kw_only, **kwargs): ...
#
# SMALL WORKING EXAMPLE:
def train(model_name, epochs=10, *, learning_rate=0.01, verbose=False):
    if verbose:
        print(f"training {model_name}")
    return f"{model_name}: {epochs} epochs @ lr={learning_rate}"

def total(*numbers):
    return sum(numbers)

def describe(**settings):
    return ", ".join(f"{k}={v}" for k, v in sorted(settings.items()))

def add_item(item, basket=None):
    if basket is None:
        basket = []
    basket.append(item)
    return basket

print(train("cnn"))
print(train("rnn", 5, learning_rate=0.1, verbose=True))
print(total(1, 2, 3), total(*[4, 5]))
config = {"batch_size": 32, "dropout": 0.2}
print(describe(**config))
print(add_item("a"), add_item("b"))

# EXPLANATION (LINE BY LINE):
# def train(model_name, epochs=10, *, learning_rate=..., verbose=...)
#   -> model_name required; epochs optional; the * makes the rest keyword-only.
# train("cnn")                  -> uses all defaults.
# train("rnn", 5, learning_rate=0.1, verbose=True) -> keyword-only must be named.
# def total(*numbers)           -> numbers is a tuple of all positional arguments.
# total(*[4, 5])                -> unpack a list into separate arguments.
# def describe(**settings)      -> settings is a dict of keyword arguments.
# describe(**config)            -> unpack a dict into keyword arguments.
# add_item uses basket=None     -> a fresh list each call; no shared state.
#
# COMMON MISTAKES:
# 1. Mutable defaults (def f(x=[])).
# 2. Putting a parameter without a default after one with a default.
# 3. Passing a keyword-only argument positionally -> TypeError.
# 4. Overusing **kwargs so callers cannot tell what options exist.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Write greet(name, greeting="Hello", punctuation="!") and call it four ways:
# positional only, with one keyword, with both keywords, and keywords reordered.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Write make_request(url, *, method="GET", timeout=10, **headers) that returns
# a dict describing the request. Show that calling make_request(url, "POST")
# fails and explain why the * is a good API design choice.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Demonstrate the mutable default bug with def append_log(entry, log=[]).
# Print append_log.__defaults__ after each call to prove the list is shared.
# Then write a fixed version, and a function merge_configs(*configs, **overrides)
# that merges any number of dicts left to right, then applies overrides.

# YOUR CODE:

