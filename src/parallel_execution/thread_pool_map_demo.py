"""
thread_pool_map_demo.py — Demonstrates parallel execution using ThreadPoolExecutor.map().

Unlike submit(), map() is simpler for running the same function over many inputs.
It returns results in the same order as inputs, and runs tasks in parallel behind the scenes.
"""

from concurrent.futures import ThreadPoolExecutor
import random
from time import sleep, perf_counter
from src.utils.logger import log

NUM_TASKS = 6


def compute(x: float) -> float:
    delay = round(random.uniform(0.3, 0.8), 2)
    log(f"Computing square of {x} with delay {delay}s")
    sleep(delay)
    return x ** 2


def run_thread_pool_map_demo():
    start = perf_counter()

    log("🚀 Starting ThreadPoolExecutor.map() demo...")

    inputs = [round(random.uniform(2.0, 5.0), 2) for _ in range(NUM_TASKS)]

    with ThreadPoolExecutor(max_workers=3) as executor:
        results = executor.map(compute, inputs)

    for x, res in zip(inputs, results):
        log(f" → {x}^2 = {res}")

    elapsed = perf_counter() - start
    log(f"✅ ThreadPoolExecutor.map() demo completed in {elapsed:.2f} seconds")


if __name__ == "__main__":
    run_thread_pool_map_demo()
