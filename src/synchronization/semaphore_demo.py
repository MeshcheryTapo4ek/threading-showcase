"""
semaphore_demo.py — Demonstrates limiting concurrent access using threading.Semaphore.

This example simulates multiple clients trying to use a limited resource (e.g., database),
but only a fixed number of them can access it at the same time.

Useful when you want to limit parallelism: connections, GPU access, etc.
"""

import threading
import random
from time import sleep, perf_counter
from src.utils.logger import log

# Only N workers can enter the critical section at once
MAX_CONCURRENT = 3
semaphore = threading.Semaphore(MAX_CONCURRENT)

NUM_WORKERS = 10


def worker(worker_id: int):
    """
    Simulates a worker trying to access a limited resource (e.g., DB connection).
    """
    log(f"Worker {worker_id} waiting to enter...")

    with semaphore:  # blocks if MAX_CONCURRENT already inside
        log(f"Worker {worker_id} acquired access ✅")
        work_time = round(random.uniform(0.5, 1.5), 2)
        sleep(work_time)
        log(f"Worker {worker_id} done (worked {work_time}s)")

    log(f"Worker {worker_id} released access.")


def run_semaphore_demo():
    start = perf_counter()

    log("🚀 Starting Semaphore demo — limit concurrent access")

    threads = [threading.Thread(target=worker, args=(i,), name=f"Worker-{i}") for i in range(NUM_WORKERS)]

    for t in threads: t.start()
    for t in threads: t.join()

    elapsed = perf_counter() - start
    log(f"✅ Semaphore demo completed in {elapsed:.2f} seconds")


if __name__ == "__main__":
    run_semaphore_demo()
