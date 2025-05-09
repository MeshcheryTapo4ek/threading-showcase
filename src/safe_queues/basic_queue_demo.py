"""
basic_queue_demo.py — Demonstrates the basic functionality of queue.Queue.

This includes:
- put() / get()
- qsize(), full(), empty()
- blocking behavior when full or empty

Useful as a baseline for understanding how Queue handles internal locking and coordination.
"""

import threading
import random
from queue import Queue
from time import sleep, perf_counter
from src.utils.logger import log

# Create a Queue with a maximum size of 3
q = Queue(maxsize=3)


def producer():
    for i in range(5):
        item = f"item-{i}"
        sleep(random.uniform(0.1, 0.4))  # Simulate production time

        log(f"Producer: trying to put {item} (queue size: {q.qsize()})")
        q.put(item)  # Blocks if queue is full
        log(f"Producer: put {item} ✅ (queue size: {q.qsize()})")


def consumer():
    for _ in range(5):
        log(f"Consumer: waiting to get item...")
        item = q.get()  # Blocks if queue is empty
        log(f"Consumer: got {item} ✅ (queue size: {q.qsize()})")
        sleep(random.uniform(0.2, 0.5))  # Simulate processing time
        q.task_done()


def run_basic_queue_demo():
    start = perf_counter()

    log("🚀 Starting basic queue demo — blocking behavior, put/get, qsize")

    t_prod = threading.Thread(target=producer, name="Producer")
    t_cons = threading.Thread(target=consumer, name="Consumer")

    t_cons.start()
    t_prod.start()

    t_prod.join()
    t_cons.join()

    elapsed = perf_counter() - start
    log(f"✅ Basic queue demo completed in {elapsed:.2f} seconds")


if __name__ == "__main__":
    run_basic_queue_demo()
