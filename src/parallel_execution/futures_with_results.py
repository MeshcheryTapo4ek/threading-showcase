"""
futures_with_results.py — Demonstrates using submit() and result() to retrieve outputs from threads.

This approach gives:
- fine-grained control over task submission,
- access to Future objects (can be cancelled, checked, etc),
- ability to process results in submission order (not completion order).
"""

from concurrent.futures import ThreadPoolExecutor
import random
from time import sleep, perf_counter
from src.utils.logger import log

NUM_TASKS = 6


def compute(task_id: int) -> float:
    delay = round(random.uniform(0.3, 0.9), 2)
    x = round(random.uniform(1.5, 4.5), 2)
    log(f"[Task-{task_id}] Started: input={x}, delay={delay}s")
    sleep(delay)
    result = round(x ** 2, 2)
    log(f"[Task-{task_id}] Finished: result={result}")
    return result


def run_futures_with_results_demo():
    start = perf_counter()

    log("🚀 Starting demo: submit() + result()")

    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = []
        for i in range(NUM_TASKS):
            fut = executor.submit(compute, i)
            futures.append(fut)

        for i, fut in enumerate(futures):
            result = fut.result()  # blocks until done
            log(f" → Task-{i} returned: {result}")

    elapsed = perf_counter() - start
    log(f"✅ submit/result demo completed in {elapsed:.2f} seconds")


if __name__ == "__main__":
    run_futures_with_results_demo()
