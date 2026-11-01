# ======================================
# TOPIC: WHILE LOOPS
# LEVEL: BEGINNER
# ID: python.loops.while-loops
# ======================================

# INTRODUCTION
# Sometimes you do not know how many repetitions you need: keep training
# until the loss stops improving, keep retrying until a request succeeds.
# while loops repeat as long as a condition stays true.
#
# THEORY
# - while condition: runs the block again and again while the condition is truthy.
# - Something inside the loop must eventually make the condition false,
#   or you get an infinite loop.
# - while True: ... break is a common pattern when the exit check is in the middle.
# - Use for when you iterate over a known collection; while for "until" logic.
#
# REAL-WORLD ANALOGY
# Filling a bucket: keep pouring water WHILE the bucket is not full.
#
# SYNTAX:
#   while condition:
#       ...
#
# SMALL WORKING EXAMPLE:
loss = 1.0
step = 0
while loss > 0.1:
    loss *= 0.6
    step += 1
print(f"stopped after {step} steps, loss={loss:.3f}")
attempts = 0
max_attempts = 5
responses = ["timeout", "timeout", "ok"]
while attempts < max_attempts:
    result = responses[attempts]
    attempts += 1
    if result == "ok":
        print("success on attempt", attempts)
        break
    print("attempt", attempts, "failed:", result)

# EXPLANATION (LINE BY LINE):
# while loss > 0.1:          -> repeat until the loss is small enough.
# loss *= 0.6                -> each step reduces the loss (a stand-in for training).
# step += 1                  -> count iterations.
# while attempts < max_attempts: -> a safety limit prevents infinite retries.
# result = responses[attempts]   -> simulated server response.
# if result == "ok": ... break   -> leave the loop early on success.
#
# COMMON MISTAKES:
# 1. Forgetting to update the variable in the condition -> infinite loop.
# 2. No maximum iterations for retry loops.
# 3. Using while with a manual index to walk a list (use for).
# 4. Off-by-one: < vs <= in the condition.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Count down from 10 to 1 with a while loop, then print "Liftoff!".

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Implement the number-guessing logic: given a secret number and a list of
# guesses, loop until the guess is correct, printing "higher"/"lower".
# Stop with a message if the guesses run out.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Implement retry_with_backoff(operation, max_attempts=5, base_delay=0.1)
# where operation is a function that may raise an exception. Wait
# base_delay * 2 ** attempt seconds between attempts (time.sleep), and
# re-raise the last error after the final attempt. Test it with a function
# that fails twice then succeeds.

# YOUR CODE:

