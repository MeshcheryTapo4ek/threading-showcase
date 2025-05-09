"""
queue_with_timeout.py — Demonstrates safe use of queue.Queue with timeout.

We show:
- Producers that give up if queue is full for too long.
- Consumers that exit if no items arrive in time.

This pattern helps avoid stuck threads in real-world systems.
"""

import threading
import random
from queue import Queue, Full, Empty
from time import sleep, perf_counter
from src.utils.logger import log

QUEUE_MAXSIZE = 3
NUM_ITEMS = 5

q = Queue(maxsize=QUEUE_MAXSIZE)


def producer():
    for i in range(NUM_ITEMS):
        item = f"item-{i}"
        sleep(random.uniform(0.1, 0.4))

        try:
            log(f"Producer trying to put {item}...")
            q.put(item, timeout=1.0)  # wait max 1s
            log(f"Producer put {item} ✅")
        except Full:
            log(f"Producer could not put {item} — queue full! Skipping.", prefix="WARN")


def consumer():
    for _ in range(NUM_ITEMS + 2):  # try to consume more than produced
        sleep(random.uniform(0.3, 0.6))

        try:
            log("Consumer waiting for item...")
            item = q.get(timeout=1.5)
            log(f"Consumer got {item} ✅")
            q.task_done()
        except Empty:
            log("Consumer timed out waiting — exiting.", prefix="WARN")
            break


def run_queue_timeout_demo():
    start = perf_counter()

    log("🚀 Starting queue demo with put/get timeouts")

    t_prod = threading.Thread(target=producer, name="Producer")
    t_cons = threading.Thread(target=consumer, name="Consumer")

    t_cons.start()
    t_prod.start()

    t_prod.join()
    t_cons.join()

    elapsed = perf_counter() - start
    log(f"✅ Timeout queue demo completed in {elapsed:.2f} seconds")


if __name__ == "__main__":
    run_queue_timeout_demo()
