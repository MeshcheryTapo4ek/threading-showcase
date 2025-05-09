"""
basic_thread_demo.py — Shows how to start multiple threads manually using threading.Thread.

This is the rawest way to create threads:
- Define a function
- Start N threads manually
- Wait for them to finish using .join()

This approach is simple but doesn't scale well — you'll see why soon.
"""

import threading
import random
from time import sleep, perf_counter
from src.utils.logger import log

NUM_THREADS = 5


def worker(thread_id: int):
    """
    Simulates some work. Each thread runs this function independently.
    """
    log(f"Thread-{thread_id} starting work...")
    work_time = round(random.uniform(0.5, 1.2), 2)
    sleep(work_time)
    log(f"Thread-{thread_id} finished after {work_time}s")


def run_basic_thread_demo():
    start = perf_counter()

    log("🚀 Starting basic thread demo — manual thread creation")

    threads = []

    for tid in range(NUM_THREADS):
        t = threading.Thread(target=worker, args=(tid,), name=f"Thread-{tid}")
        t.start()
        threads.append(t)

    # Wait for all threads to complete
    for t in threads:
        t.join()

    elapsed = perf_counter() - start
    log(f"✅ Basic thread demo completed in {elapsed:.2f} seconds")


if __name__ == "__main__":
    run_basic_thread_demo()
