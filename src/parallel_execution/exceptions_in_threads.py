"""
exceptions_in_threads.py — Demonstrates how to catch exceptions from threads via Future.result().

This is critical for real applications where:
- threads can raise exceptions,
- you don't want silent failures,
- exception details are retrievable from the future object.

NEVER ignore Future.result().
"""

from concurrent.futures import ThreadPoolExecutor, as_completed
import random
from time import sleep, perf_counter
from src.utils.logger import log

NUM_TASKS = 6


def risky_compute(task_id: int) -> float:
    delay = round(random.uniform(0.3, 0.7), 2)
    sleep(delay)

    # 30% chance of failure
    if random.random() < 0.3:
        raise ValueError(f"Task-{task_id} failed due to bad luck 💥")

    x = round(random.uniform(1.0, 4.0), 2)
    result = round(x ** 2, 2)
    return result


def run_exception_handling_demo():
    start = perf_counter()

    log("🚀 Starting demo: catching exceptions from thread pool")

    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {executor.submit(risky_compute, i): i for i in range(NUM_TASKS)}

        for future in as_completed(futures):
            task_id = futures[future]
            try:
                result = future.result()
                log(f" → Task-{task_id} succeeded with result: {result}")
            except Exception as e:
                log(f" ❌ Task-{task_id} raised exception: {e}", prefix="ERROR")

    elapsed = perf_counter() - start
    log(f"✅ Exception-handling demo completed in {elapsed:.2f} seconds")


if __name__ == "__main__":
    run_exception_handling_demo()
