# ======================================
# TOPIC: ASYNC / AWAIT BASICS
# LEVEL: ADVANCED
# ID: python.async.basics
# ======================================

# INTRODUCTION
# AI applications spend most of their time WAITING: for an LLM API, a vector
# database, a web page. Async programming lets one program wait on many things
# at once instead of one after another.
#
# THEORY
# - async def defines a COROUTINE FUNCTION. Calling it returns a coroutine
#   object and does NOT run the body yet.
# - await pauses the current coroutine until another awaitable finishes,
#   letting the EVENT LOOP run other tasks meanwhile.
# - asyncio.run(main()) starts the event loop and runs the top-level coroutine.
# - await can only be used inside async def.
# - Use asyncio.sleep (non-blocking), never time.sleep (blocks everything),
#   inside async code.
# - Async helps with I/O-bound work (network, disk), not CPU-heavy maths.
#
# REAL-WORLD ANALOGY
# A chef cooking several dishes: while the rice simmers (waiting on I/O), the
# chef chops vegetables for another dish instead of staring at the pot.
#
# SYNTAX:
#   async def fetch():
#       await asyncio.sleep(1)
#       return "data"
#   asyncio.run(fetch())
#
# SMALL WORKING EXAMPLE:
import asyncio
import time

async def call_model(prompt, delay):
    print(f"  sending: {prompt}")
    await asyncio.sleep(delay)
    return f"answer to {prompt!r}"

async def sequential():
    first = await call_model("q1", 0.3)
    second = await call_model("q2", 0.3)
    return [first, second]

async def concurrent():
    return await asyncio.gather(call_model("q1", 0.3), call_model("q2", 0.3))

coroutine = call_model("not awaited", 0)
print(type(coroutine).__name__)
coroutine.close()
for runner in (sequential, concurrent):
    start = time.perf_counter()
    answers = asyncio.run(runner())
    print(runner.__name__, answers, f"{time.perf_counter() - start:.2f}s")

# EXPLANATION (LINE BY LINE):
# async def call_model(...)    -> a coroutine function simulating an API call.
# await asyncio.sleep(delay)   -> non-blocking wait; other coroutines may run.
# sequential(): await one, then the other -> about 0.6s in total.
# concurrent(): asyncio.gather(...) runs both at once -> about 0.3s in total.
# coroutine = call_model(...)  -> just a coroutine object; nothing printed yet.
# coroutine.close()            -> clean up the never-awaited coroutine.
# asyncio.run(runner())        -> start an event loop for each demo.
#
# COMMON MISTAKES:
# 1. Forgetting await -> you get a coroutine object, not the result
#    ("RuntimeWarning: coroutine was never awaited").
# 2. Using time.sleep or blocking libraries (requests) inside async code.
# 3. Calling asyncio.run inside an already running loop (e.g. Jupyter: use await).
# 4. Expecting async to speed up CPU-bound work.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Write an async function greet(name, delay) that waits and returns a greeting.
# Run it once with asyncio.run and print the result.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Simulate downloading 5 files with different delays. Time a sequential version
# and a concurrent (gather) version and print the speed-up.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Show the blocking problem: run two coroutines concurrently where one uses
# time.sleep(1) and the other uses asyncio.sleep(1); measure the total time.
# Fix it with asyncio.to_thread for the blocking call and explain the result.

# YOUR CODE:

