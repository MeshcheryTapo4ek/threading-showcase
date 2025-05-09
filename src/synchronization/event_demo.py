"""
event_demo.py — Advanced demo of threading.Event with multiple rounds and randomized work.

Demonstrates:
- event-based synchronization across multiple phases;
- randomized work duration after signal;
- timeout handling if signal is not received in time.
"""

import threading
import random
from time import sleep, perf_counter
from src.utils.logger import log

NUM_WORKERS = 3
NUM_ROUNDS = 3
SIGNAL_TIMEOUT = 2.0  # seconds

ready_event = threading.Event()


def worker(worker_id: int):
    """
    Worker waits for signal in each round, then performs randomized-duration work.
    If signal is not received in time, the worker logs a timeout and skips the round.
    """
    for round_idx in range(1, NUM_ROUNDS + 1):
        log(f"[Round {round_idx}] Worker {worker_id} is waiting for signal...")

        signal_received = ready_event.wait(timeout=SIGNAL_TIMEOUT)

        if signal_received:
            work_time = round(random.uniform(0.3, 1.0), 2)
            log(f"[Round {round_idx}] Worker {worker_id} received signal — working for {work_time}s")
            sleep(work_time)
            log(f"[Round {round_idx}] Worker {worker_id} finished.")
        else:
            log(f"[Round {round_idx}] Worker {worker_id} timed out waiting for signal.", prefix="WARN")

        # Clear the signal before next round (coordinator won't re-set if it's already True)
        ready_event.clear()


def coordinator():
    """
    Sends a signal in each round, allowing all workers to proceed.
    Each round starts after a small delay, simulating phase transitions.
    """
    for round_idx in range(1, NUM_ROUNDS + 1):
        sleep(1 + 0.3 * round_idx)
        log(f"[Round {round_idx}] Coordinator: broadcasting signal")
        ready_event.set()


def run_event_demo():
    start = perf_counter()

    log("🚀 Starting advanced Event demo with randomized worker execution...")

    threads = [threading.Thread(target=worker, args=(i,), name=f"Worker-{i}") for i in range(1, NUM_WORKERS + 1)]
    for t in threads: t.start()

    coordinator_thread = threading.Thread(target=coordinator, name="Coordinator")
    coordinator_thread.start()

    for t in threads:
        t.join()
    coordinator_thread.join()

    elapsed = perf_counter() - start
    log(f"✅ Demo completed in {elapsed:.2f} seconds")


if __name__ == "__main__":
    run_event_demo()
