# ======================================
# TOPIC: API ERRORS, RETRIES AND RATE LIMITS
# LEVEL: ADVANCED
# ID: python.apis.retries-rate-limits
# ======================================

# INTRODUCTION
# Production AI apps call external APIs thousands of times. Some calls WILL
# fail: rate limits, timeouts, overloaded servers. Robust clients retry the
# right errors in the right way.
#
# THEORY
# - Retry only TRANSIENT errors: 408 timeout, 429 rate limit, 5xx server
#   errors, connection errors. Never blindly retry 400/401/403/404.
# - Exponential backoff: wait base * 2 ** attempt seconds, capped at a maximum.
# - Jitter: add randomness so many clients do not retry at the same moment.
# - Respect a "Retry-After" header when the server sends one.
# - Limit total attempts and total time.
# - Rate limiting on your side (token bucket) prevents 429s in the first place.
# - Idempotency: retrying a POST that creates something can duplicate it;
#   APIs use idempotency keys to make retries safe.
#
# REAL-WORLD ANALOGY
# Calling a busy helpline: if the line is busy you wait a bit, then longer each
# time; if they say "call back in 10 minutes" you do exactly that; if they say
# "wrong number" you stop calling.
#
# SYNTAX:
#   delay = min(cap, base * 2 ** attempt) * random.uniform(0.5, 1.5)
#
# SMALL WORKING EXAMPLE:
import random
import time

class APIError(Exception):
    def __init__(self, status, retry_after=None):
        super().__init__(f"HTTP {status}")
        self.status = status
        self.retry_after = retry_after

RETRYABLE = {408, 429, 500, 502, 503, 504}

def call_with_retries(func, max_attempts=4, base=0.05, cap=1.0, sleep=time.sleep):
    for attempt in range(max_attempts):
        try:
            return func()
        except APIError as error:
            last_try = attempt == max_attempts - 1
            if error.status not in RETRYABLE or last_try:
                raise
            delay = error.retry_after or min(cap, base * 2 ** attempt) * random.uniform(0.5, 1.5)
            print(f"  attempt {attempt + 1}: HTTP {error.status}, retrying in {delay:.3f}s")
            sleep(delay)

def make_fake_api(statuses):
    responses = iter(statuses)
    def call():
        status = next(responses)
        if status != 200:
            raise APIError(status, retry_after=0.01 if status == 429 else None)
        return {"status": 200, "data": "ok"}
    return call

random.seed(1)
print(call_with_retries(make_fake_api([503, 429, 200])))
try:
    call_with_retries(make_fake_api([401, 200]))
except APIError as error:
    print("not retried:", error)
try:
    call_with_retries(make_fake_api([500, 500, 500, 500]))
except APIError as error:
    print("gave up:", error)

# EXPLANATION (LINE BY LINE):
# class APIError with status and retry_after -> carry the information retries need.
# RETRYABLE = {...}             -> only transient failures are retried.
# for attempt in range(max_attempts) -> bounded number of tries.
# if not retryable or last_try: raise -> fail fast on 4xx or after the final attempt.
# delay = retry_after or backoff with jitter -> server's hint wins when present.
# sleep=time.sleep parameter    -> can be swapped for a fake in tests (dependency injection).
# make_fake_api([...])          -> closure returning a scripted sequence of statuses.
# Three scenarios: recover, fail fast on 401, give up after 4 server errors.
#
# COMMON MISTAKES:
# 1. Retrying non-retryable errors (wasting time and money).
# 2. Retrying immediately in a tight loop (makes overload worse).
# 3. Infinite retries with no cap.
# 4. Retrying non-idempotent operations without idempotency keys.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Print the backoff delays (without jitter) for attempts 0..7 with base 0.5s
# and a cap of 8s. Explain why a cap matters.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Turn call_with_retries into a decorator @retryable(max_attempts=3) and write
# a unit-test-style check (plain asserts) using a fake sleep function that
# records the delays instead of sleeping.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Implement a TokenBucket rate limiter (capacity, refill_rate per second) with
# acquire() that blocks until a token is available. Use it to send 20 fake
# requests at no more than 5 per second and print timestamps proving the rate.
# Then make an async version using asyncio.

# YOUR CODE:

