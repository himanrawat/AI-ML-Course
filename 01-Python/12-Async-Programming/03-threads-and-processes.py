# ======================================
# TOPIC: THREADS AND PROCESSES
# LEVEL: ADVANCED
# ID: python.async.threads-processes
# ======================================

# INTRODUCTION
# Not all code is async-friendly. Blocking libraries need threads, and heavy
# CPU work (feature extraction, preprocessing) needs multiple processes to use
# all CPU cores.
#
# THEORY
# - CONCURRENCY = dealing with many things at once (switching between them).
#   PARALLELISM = doing many things at literally the same time (multiple cores).
# - THREADS share memory inside one process. In standard CPython, the GIL
#   (Global Interpreter Lock) lets only one thread run Python bytecode at a
#   time, so threads help with I/O-bound work but not CPU-bound Python code.
#   (Free-threaded Python builds remove the GIL, but are not the default yet.)
# - PROCESSES each have their own interpreter and memory, so they run
#   CPU-bound work in parallel. Data passed between them must be picklable.
# - concurrent.futures gives one simple API for both:
#   ThreadPoolExecutor and ProcessPoolExecutor with .map() and .submit().
# - NumPy/PyTorch release the GIL inside their C code, so they parallelise well.
# - Rule of thumb: I/O-bound -> asyncio or threads; CPU-bound -> processes
#   or vectorised libraries.
#
# REAL-WORLD ANALOGY
# Threads are several cooks sharing one stove (one burner at a time - the GIL).
# Processes are several kitchens, each with its own stove.
#
# SYNTAX:
#   with ThreadPoolExecutor(max_workers=4) as pool:
#       results = list(pool.map(func, items))
#   if __name__ == "__main__":   # required for process pools on macOS/Windows
#       with ProcessPoolExecutor() as pool: ...
#
# SMALL WORKING EXAMPLE:
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

def io_task(n):
    time.sleep(0.2)
    return n

def cpu_task(n):
    return sum(i * i for i in range(n))

def timed(label, func):
    start = time.perf_counter()
    func()
    print(f"{label:<22}{time.perf_counter() - start:.2f}s")

if __name__ == "__main__":
    work = [3_000_000] * 4
    timed("io sequential", lambda: [io_task(i) for i in range(4)])
    with ThreadPoolExecutor(max_workers=4) as pool:
        timed("io threads", lambda: list(pool.map(io_task, range(4))))
    timed("cpu sequential", lambda: [cpu_task(n) for n in work])
    with ThreadPoolExecutor(max_workers=4) as pool:
        timed("cpu threads", lambda: list(pool.map(cpu_task, work)))
    with ProcessPoolExecutor(max_workers=4) as pool:
        timed("cpu processes", lambda: list(pool.map(cpu_task, work)))

# EXPLANATION (LINE BY LINE):
# io_task sleeps (waits like a network call); cpu_task does pure Python maths.
# timed(label, func)          -> small helper that prints elapsed time.
# if __name__ == "__main__":  -> child processes re-import this file; the guard
#                                stops them re-running the demo.
# io threads                  -> ~0.2s instead of ~0.8s: waiting overlaps.
# cpu threads                 -> about the same as sequential: the GIL.
# cpu processes               -> faster on a multi-core machine: true parallelism.
#
# COMMON MISTAKES:
# 1. Using threads for CPU-bound pure-Python work and expecting a speed-up.
# 2. Forgetting the __main__ guard with ProcessPoolExecutor.
# 3. Sharing mutable data between threads without a Lock (race conditions).
# 4. Passing unpicklable objects (lambdas, open files) to processes.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Use ThreadPoolExecutor to "download" 6 URLs (simulate with time.sleep) and
# print the total time compared to a sequential loop.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Demonstrate a race condition: 4 threads each increment a shared counter
# 100,000 times using counter += 1 in a function with a tiny time.sleep(0)
# between read and write. Then fix it with threading.Lock.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Count word frequencies across 8 large generated text documents three ways:
# sequentially, with a ThreadPoolExecutor and with a ProcessPoolExecutor
# (merge Counters at the end). Time each, and explain the results in terms of
# the GIL and process start-up/pickling overhead.

# YOUR CODE:

