"""
wait_as_completed_demo.py — Demonstrates concurrent.futures.as_completed().

This pattern:
- submits many tasks,
- processes results as they complete (not in order of submission),
- is perfect for fast-response-first scenarios (e.g. querying mirrors, scraping).

This is how you handle futures when order doesn’t matter.
"""

from concurrent.futures import ThreadPoolExecutor, as_completed
import random
from time import sleep, perf_counter
from src.utils.logger import log

NUM_TASKS = 6


def compute(task_id: int) -> float:
    delay = round(random.uniform(0.3, 1.0), 2)
    x = round(random.uniform(2.0, 5.0), 2)
    log(f"[Task-{task_id}] Started: x={x}, delay={delay}s")
    sleep(delay)
    result = round(x ** 2, 2)
    log(f"[Task-{task_id}] Finished: result={result}")
    return task_id, result


def run_as_completed_demo():
    start = perf_counter()

    log("🚀 Starting as_completed() demo — unordered result handling")

    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {executor.submit(compute, i): i for i in range(NUM_TASKS)}

        for future in as_completed(futures):
            task_id, result = future.result()
            log(f" → Task-{task_id} completed with result: {result}")

    elapsed = perf_counter() - start
    log(f"✅ as_completed demo completed in {elapsed:.2f} seconds")


if __name__ == "__main__":
    run_as_completed_demo()
