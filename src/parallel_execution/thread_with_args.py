"""
thread_with_args.py — Shows how to pass arguments to threads and collect results.

Key concepts:
- Threads receive arguments via `args=(...)`.
- Results are collected using a shared list or Queue.
- This highlights how manual threading quickly becomes boilerplate-heavy.
"""

import threading
import random
from queue import Queue
from time import sleep, perf_counter
from src.utils.logger import log

NUM_THREADS = 5
results = Queue()


def worker(task_id: int, multiplier: float):
    """
    Thread simulates computation and returns result via a shared queue.
    """
    log(f"Task-{task_id} starting with multiplier={multiplier}")
    sleep_time = round(random.uniform(0.3, 0.6), 2)
    sleep(sleep_time)
    result = task_id * multiplier
    results.put((task_id, result))
    log(f"Task-{task_id} finished after {sleep_time}s with result={result}")


def run_thread_with_args_demo():
    start = perf_counter()

    log("🚀 Starting demo: passing args and collecting results manually")

    threads = []
    for i in range(NUM_THREADS):
        multiplier = round(random.uniform(1.0, 3.0), 2)
        t = threading.Thread(target=worker, args=(i, multiplier), name=f"Task-{i}")
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    log("✅ All threads finished. Results collected:")

    while not results.empty():
        tid, val = results.get()
        log(f" → Result from Task-{tid}: {val}")

    elapsed = perf_counter() - start
    log(f"✅ Thread-with-args demo completed in {elapsed:.2f} seconds")


if __name__ == "__main__":
    run_thread_with_args_demo()
