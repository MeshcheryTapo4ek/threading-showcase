"""
task_done_join_demo.py — Demonstrates queue.Queue task tracking with task_done() and join().

This ensures:
- Producers push items into the queue.
- Consumers process items and call task_done().
- Main thread blocks until all items are processed using join().

This is the canonical way to wait for pipeline completion without using sleeps or counters.
"""

import threading
import random
from queue import Queue
from time import sleep, perf_counter
from src.utils.logger import log

NUM_ITEMS = 8
NUM_CONSUMERS = 2

q = Queue()


def producer():
    for i in range(NUM_ITEMS):
        item = f"item-{i}"
        sleep(random.uniform(0.1, 0.3))  # simulate production
        q.put(item)
        log(f"Producer put {item} (queue size: {q.qsize()})")


def consumer(consumer_id: int):
    while True:
        item = q.get()  # blocks if empty
        log(f"Consumer {consumer_id} processing {item}")
        sleep(random.uniform(0.2, 0.5))  # simulate work
        q.task_done()
        log(f"Consumer {consumer_id} finished {item}")


def run_task_done_join_demo():
    start = perf_counter()

    log("🚀 Starting demo of task_done() and join() — wait for full completion")

    # Start consumers — they run in background (daemon)
    for cid in range(NUM_CONSUMERS):
        threading.Thread(target=consumer, args=(cid,), name=f"Consumer-{cid}", daemon=True).start()

    # Start producer
    t_prod = threading.Thread(target=producer, name="Producer")
    t_prod.start()
    t_prod.join()

    # Wait until all items processed (each put must have task_done())
    log("Main thread waiting for all tasks to finish (q.join())...")
    q.join()

    elapsed = perf_counter() - start
    log(f"✅ All tasks processed. Demo completed in {elapsed:.2f} seconds")


if __name__ == "__main__":
    run_task_done_join_demo()
