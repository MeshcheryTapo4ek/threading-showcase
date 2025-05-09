"""
barrier_demo.py — Full showcase of threading.Barrier features.

This demo illustrates:
- threads arriving at the barrier at different times (via random delays),
- use of .n_waiting and .broken to monitor the barrier state,
- one thread exceeding the timeout and breaking the barrier,
- proper handling of BrokenBarrierError in other threads,
- coordinator thread detecting and resetting the broken barrier.
"""

import threading
import random
from time import sleep, perf_counter
from src.utils.logger import log

NUM_THREADS = 5
ROUND_COUNT = 3
barrier = threading.Barrier(NUM_THREADS)


def worker(worker_id: int):
    """
    Each worker simulates some work, then waits at the barrier.
    In round 1, worker 0 is intentionally delayed to break the barrier.
    Others will catch a BrokenBarrierError and exit cleanly.
    """
    try:
        for round_idx in range(ROUND_COUNT):
            # Simulate variable pre-barrier workload
            sleep_time = random.uniform(0.1, 1.2)
            log(f"[Round {round_idx}] Worker {worker_id} working for {sleep_time:.2f}s")
            sleep(sleep_time)

            log(f"[R{round_idx}] W{worker_id} waiting ({barrier.n_waiting}/{barrier.parties})")

            # Simulate a stuck thread in round 1 to break the barrier
            if round_idx == 1 and worker_id == 0:
                log(f"[Round {round_idx}] Worker {worker_id} simulating hang (5s)")
                sleep(5)

            try:
                barrier.wait(timeout=2)
                log(f"[Round {round_idx}] Worker {worker_id} passed the barrier")
            except threading.BrokenBarrierError:
                log(f"[Round {round_idx}] Worker {worker_id} detected broken barrier — exiting", prefix="ERROR")
                return

    except Exception as e:
        log(f"Worker {worker_id} — unexpected error: {e}", prefix="CRASH")


def coordinator():
    """
    Periodically checks the barrier state.
    If broken, calls reset() so that remaining threads or next phases can proceed.
    """
    while True:
        sleep(0.5)
        if barrier.broken:
            log("Barrier is broken. Coordinator resetting it.", prefix="COORDINATOR")
            barrier.reset()
            return


def run_barrier_demo():
    start = perf_counter()

    log("🚀 Starting barrier demo with multiple rounds and error simulation...")
    threads = [threading.Thread(target=worker, args=(i,), name=f"Worker-{i}") for i in range(NUM_THREADS)]

    for t in threads:
        t.start()

    coordinator_thread = threading.Thread(target=coordinator, name="Coordinator")
    coordinator_thread.start()

    for t in threads:
        t.join()
    coordinator_thread.join()

    elapsed = perf_counter() - start
    log(f"✅ Demo completed in {elapsed:.2f} seconds")


if __name__ == "__main__":
    run_barrier_demo()
