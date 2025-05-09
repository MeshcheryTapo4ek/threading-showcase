"""
thread_pool_executor.py — Demonstrates concurrent.futures.ThreadPoolExecutor.

This shows:
- submitting tasks to a thread pool,
- parallel execution without writing custom Thread classes,
- automatic result handling.

It's the most convenient and scalable way to run parallel tasks in threads.
"""

from concurrent.futures import ThreadPoolExecutor
import random
from time import sleep, perf_counter
from src.utils.logger import log

NUM_TASKS = 5


def compute(task_id: int) -> float:
    """
    Simulates a simple computation.
    Returns square of a random number.
    """
    delay = round(random.uniform(0.3, 0.8), 2)
    x = round(random.uniform(2.0, 5.0), 2)
    log(f"[Task-{task_id}] Starting: input={x}, delay={delay}s")
    sleep(delay)
    result = x ** 2
    log(f"[Task-{task_id}] Done: result={result}")
    return result


def run_thread_pool_demo():
    start = perf_counter()

    log("🚀 Starting ThreadPoolExecutor demo...")

    with ThreadPoolExecutor(max_workers=3) as executor:
        # Submit tasks and collect future objects
        futures = [executor.submit(compute, i) for i in range(NUM_TASKS)]

        # Retrieve results (order preserved)
        for i, future in enumerate(futures):
            result = future.result()
            log(f" → Task-{i} result = {result}")

    elapsed = perf_counter() - start
    log(f"✅ ThreadPoolExecutor demo completed in {elapsed:.2f} seconds")


if __name__ == "__main__":
    run_thread_pool_demo()
