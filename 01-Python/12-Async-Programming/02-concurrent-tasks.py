# ======================================
# TOPIC: RUNNING TASKS CONCURRENTLY
# LEVEL: ADVANCED
# ID: python.async.concurrent-tasks
# ======================================

# INTRODUCTION
# Evaluating a prompt on 500 test cases, or embedding 10,000 documents, means
# many API calls. You need concurrency - but controlled, with timeouts, error
# handling and rate limits.
#
# THEORY
# - asyncio.create_task(coro) schedules a coroutine to run in the background.
# - asyncio.gather(*aws, return_exceptions=True) waits for all and returns
#   results in ORDER; with return_exceptions=True, errors are returned as values.
# - asyncio.TaskGroup (3.11+) runs tasks together; if one fails, the others are
#   cancelled and errors are raised as an ExceptionGroup.
# - asyncio.Semaphore(n) limits how many tasks run at the same time
#   (respect API rate limits).
# - asyncio.timeout(seconds) / asyncio.wait_for cancel slow operations.
# - asyncio.as_completed yields results as soon as each finishes.
#
# REAL-WORLD ANALOGY
# A restaurant with 3 chefs (semaphore) and 20 orders: orders queue up, at most
# three are cooked at once, and any dish taking too long is cancelled (timeout).
#
# SYNTAX:
#   sem = asyncio.Semaphore(3)
#   async with sem: ...
#   async with asyncio.timeout(2): ...
#   results = await asyncio.gather(*tasks, return_exceptions=True)
#
# SMALL WORKING EXAMPLE:
import asyncio
import random

async def score_example(i, sem, active):
    async with sem:
        active.append(i)
        peak = len(active)
        await asyncio.sleep(random.uniform(0.01, 0.05))
        active.remove(i)
        if i == 3:
            raise ValueError(f"bad example {i}")
        return {"id": i, "score": round(random.random(), 2), "peak": peak}

async def slow_call():
    await asyncio.sleep(1)

async def main():
    random.seed(0)
    sem = asyncio.Semaphore(3)
    active = []
    results = await asyncio.gather(
        *(score_example(i, sem, active) for i in range(8)), return_exceptions=True
    )
    ok = [r for r in results if not isinstance(r, Exception)]
    failed = [r for r in results if isinstance(r, Exception)]
    print(len(ok), "succeeded;", "failed:", failed)
    print("max concurrent:", max(r["peak"] for r in ok))
    try:
        async with asyncio.timeout(0.1):
            await slow_call()
    except TimeoutError:
        print("slow call cancelled after 0.1s")

asyncio.run(main())

# EXPLANATION (LINE BY LINE):
# async with sem:              -> at most 3 coroutines inside this block at once.
# active list / peak           -> records how many were running simultaneously.
# raise ValueError for i == 3  -> simulate one failing request.
# gather(..., return_exceptions=True) -> one failure does not lose other results.
# split results into ok / failed -> typical evaluation-run bookkeeping.
# max(r["peak"] ...)           -> never more than 3: the semaphore works.
# async with asyncio.timeout(0.1) -> cancels slow_call and raises TimeoutError.
#
# COMMON MISTAKES:
# 1. Launching thousands of requests at once and hitting rate limits.
# 2. Forgetting return_exceptions=True, losing all results on one failure.
# 3. Creating tasks and never awaiting them (errors disappear).
# 4. No timeouts on network calls.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Use asyncio.create_task to start three timers (0.3s, 0.1s, 0.2s), await all
# of them, and print the order in which they finish.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Process 20 fake requests with at most 5 running at a time (Semaphore).
# Use asyncio.as_completed to print each result as soon as it is ready,
# with a progress counter like "7/20 done".

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Build an async batch evaluator: evaluate(items, worker, concurrency=4,
# timeout=0.5, retries=2). It should run worker(item) with limited concurrency,
# retry failures with exponential backoff, mark timeouts, and return a summary
# dict (succeeded, failed, timed_out, total_time). Rewrite the core with
# asyncio.TaskGroup and compare its failure behaviour with gather.

# YOUR CODE:

