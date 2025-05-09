"""
lock_demo.py — Demonstrates race conditions and how Lock solves them.

This script shows how multiple threads can corrupt shared state
when no synchronization is used, and how `threading.Lock` prevents this.
"""

import threading
from time import sleep
from src.utils.logger import log

# Shared resource (dangerous to mutate concurrently)
counter = 0
NUM_ITERATIONS = 1_200
NUM_THREADS = 6  # Increased to provoke race conditions more reliably

# Create a lock for synchronization
lock = threading.Lock()


def increment_unsafely():
    """
    Increments the global counter without any synchronization.
    This leads to a race condition — threads overwrite each other's increments.
    """
    global counter
    for _ in range(NUM_ITERATIONS):
        tmp = counter
        tmp += 1
        # Adding tiny sleep increases context-switch chance → exposes race
        sleep(0.00001)
        counter = tmp


def increment_safely():
    """
    Increments the global counter using a Lock to protect the critical section.
    Prevents threads from corrupting shared state.
    """
    global counter
    for _ in range(NUM_ITERATIONS):
        with lock:
            counter += 1


def run_demo(target_func, description: str):
    """
    Runs the demo with multiple threads using the provided target function.

    :param target_func: Function to execute in each thread.
    :param description: Description to log before running.
    """
    global counter
    counter = 0
    threads = []

    log(f"\n--- {description} ---")

    for _ in range(NUM_THREADS):
        thread = threading.Thread(target=target_func)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    expected = NUM_ITERATIONS * NUM_THREADS

    log(f"Expected counter: {expected}")
    log(f"Actual counter:   {counter}")

    if counter != expected:
        log("❌ Race condition occurred! Shared state was corrupted.", prefix="ERROR")
    else:
        log("✅ Counter is correct. Synchronization successful.", prefix="OK")
    print()


if __name__ == "__main__":
    run_demo(increment_unsafely, "Unsafe Increment (No Lock)")
    run_demo(increment_safely, "Safe Increment (With Lock)")
