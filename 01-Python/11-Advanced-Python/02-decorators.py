# ======================================
# TOPIC: DECORATORS
# LEVEL: ADVANCED
# ID: python.advanced.decorators
# ======================================

# INTRODUCTION
# @app.get("/"), @torch.no_grad(), @lru_cache, @pytest.fixture: decorators are
# everywhere in AI and web code. They add behaviour to functions without
# changing the functions' code.
#
# THEORY
# - A decorator is a function that takes a function and returns a new function.
# - @decorator above def f is shorthand for: f = decorator(f)
# - The returned "wrapper" usually accepts *args, **kwargs, calls the original
#   and adds behaviour before/after (timing, logging, retries, caching).
# - Use functools.wraps(func) on the wrapper to keep the original name and
#   docstring.
# - Decorators WITH arguments need one more level: a function that returns
#   a decorator: @retry(times=3).
# - Decorators stack: the one closest to def is applied first.
#
# REAL-WORLD ANALOGY
# Gift wrapping: the gift (function) is unchanged, but the wrapping adds
# something around it, and you can wrap a gift several times.
#
# SYNTAX:
#   def decorator(func):
#       @functools.wraps(func)
#       def wrapper(*args, **kwargs):
#           ...before...
#           result = func(*args, **kwargs)
#           ...after...
#           return result
#       return wrapper
#
# SMALL WORKING EXAMPLE:
import functools
import time

def timed(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        print(f"{func.__name__} took {time.perf_counter() - start:.4f}s")
        return result
    return wrapper

def retry(times):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except ConnectionError as error:
                    print(f"attempt {attempt} failed: {error}")
            raise ConnectionError(f"{func.__name__} failed {times} times")
        return wrapper
    return decorator

calls = {"n": 0}

@timed
@retry(times=3)
def flaky_api():
    """Pretend to call an API that fails twice."""
    calls["n"] += 1
    if calls["n"] < 3:
        raise ConnectionError("timeout")
    return "ok"

print(flaky_api())
print(flaky_api.__name__, "-", flaky_api.__doc__)

# EXPLANATION (LINE BY LINE):
# timed(func) returns wrapper   -> wrapper measures time around func.
# @functools.wraps(func)        -> wrapper keeps func's __name__ and __doc__.
# retry(times) returns decorator -> decorator factory because it takes arguments.
# for attempt ... try: return func(...) -> retry on ConnectionError.
# @timed @retry(times=3) def flaky_api -> flaky_api = timed(retry(3)(flaky_api)).
# flaky_api() fails twice, succeeds on attempt 3; total time printed once.
# flaky_api.__name__            -> "flaky_api", thanks to functools.wraps.
#
# COMMON MISTAKES:
# 1. Forgetting to return the result inside wrapper (function returns None).
# 2. Forgetting functools.wraps (debugging and docs show "wrapper").
# 3. Writing @retry instead of @retry(times=3) for a decorator factory.
# 4. Getting the stacking order wrong.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Write a decorator log_calls that prints the function name and arguments
# before each call and the return value after. Apply it to add(a, b).

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Write a decorator count_calls that stores the number of calls as an
# attribute on the wrapper (wrapper.calls). Write validate_positive that raises
# ValueError if any numeric argument is negative. Stack both on one function.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Write cache_with_ttl(seconds) - a memoizing decorator whose entries expire
# after the given time (use time.monotonic). Support keyword arguments in the
# cache key, and add a wrapper.cache_clear() function. Test expiry with a
# short TTL and time.sleep.

# YOUR CODE:

