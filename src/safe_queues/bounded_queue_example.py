"""
bounded_queue_example.py — Demonstrates backpressure behavior of queue.Queue with maxsize.

When the queue is full, producers are blocked until consumers make space.
This pattern is essential when working with bounded resources like memory or external services.
"""

import threading
import random
from queue import Queue
from time import sleep, perf_counter
from src.utils.logger import log

QUEUE_MAXSIZE = 2
NUM_ITEMS = 6

q = Queue(maxsize=QUEUE_MAXSIZE)


def producer():
    for i in range(NUM_ITEMS):
        item = f"item-{i}"
        sleep(random.uniform(0.1, 0.3))  # simulate work

        log(f"Producer trying to put {item} (queue size: {q.qsize()}/{QUEUE_MAXSIZE})")
        q.put(item)  # blocks if full
        log(f"Producer put {item} ✅ (queue size: {q.qsize()}/{QUEUE_MAXSIZE})")


def consumer():
    for _ in range(NUM_ITEMS):
        sleep(random.uniform(0.4, 0.6))  # simulate slower consumer

        log("Consumer waiting for item...")
        item = q.get()
        log(f"Consumer got {item}")
        q.task_done()


def run_bounded_queue_demo():
    start = perf_counter()

    log(f"🚀 Starting bounded queue demo with maxsize = {QUEUE_MAXSIZE}")

    t_prod = threading.Thread(target=producer, name="Producer")
    t_cons = threading.Thread(target=consumer, name="Consumer")

    t_cons.start()
    t_prod.start()

    t_prod.join()
    t_cons.join()

    elapsed = perf_counter() - start
    log(f"✅ Bounded queue demo completed in {elapsed:.2f} seconds")


if __name__ == "__main__":
    run_bounded_queue_demo()
