"""
condition_demo.py — Demonstrates signaling between threads using threading.Condition.

This version includes:
- randomized producer and consumer delays,
- detailed commentary on behavior and race conditions,
- classic producer-consumer buffer logic using Condition.

Key idea: Consumers wait when the buffer is empty,
Producers wait when the buffer is full,
and both coordinate using `condition.wait()` / `condition.notify()`.
"""

import threading
import random
from time import sleep, perf_counter
from src.utils.logger import log

# Shared buffer (acts as a bounded queue)
buffer = []
buffer_capacity = 5

# Condition wraps a Lock and provides signaling primitives
condition = threading.Condition()

NUM_PRODUCERS = 2
NUM_CONSUMERS = 2
NUM_ITEMS_PER_PRODUCER = 5


def producer(producer_id: int):
    for item_id in range(NUM_ITEMS_PER_PRODUCER):
        item = f"Producer_id_{producer_id}-item_id_{item_id}"

        # Simulate unpredictable production time
        sleep(random.uniform(0.1, 0.6))

        with condition:
            # If buffer is full — wait until consumer consumes
            while len(buffer) >= buffer_capacity:
                log(f"Producer {producer_id} waiting — buffer full")
                condition.wait()

            # Critical section — safe to add item
            buffer.append(item)
            log(f"Producer {producer_id} produced {item} (buffer size: {len(buffer)})")

            # Wake up one consumer (if any are waiting)
            condition.notify()


def consumer(consumer_id: int):
    while True:
        with condition:
            # Wait until buffer has something
            while not buffer:
                log(f"Consumer {consumer_id} waiting — buffer empty")
                # Wait at most 3 seconds before giving up
                condition.wait(timeout=3)
                if not buffer:
                    log(f"Consumer {consumer_id} timeout — exiting", prefix="WARN")
                    return

            # Critical section — safe to consume
            item = buffer.pop(0)
            log(f"Consumer {consumer_id} consumed {item} (buffer size: {len(buffer)})")

            # Wake up one producer if they were waiting due to full buffer
            condition.notify()

        # Simulate variable consumption speed
        sleep(random.uniform(0.2, 0.8))


def run_condition_demo():
    start = perf_counter()

    log("🚀 Starting Condition demo — producer/consumer with random delays")

    producers = [threading.Thread(target=producer, args=(i,), name=f"Producer-{i}") for i in range(NUM_PRODUCERS)]
    consumers = [threading.Thread(target=consumer, args=(i,), name=f"Consumer-{i}") for i in range(NUM_CONSUMERS)]

    # Start consumers first — they'll likely start waiting immediately
    for t in consumers + producers:
        t.start()

    # Join producers — when they finish, no more items will be added
    for t in producers:
        t.join()

    # Join consumers — they will timeout and exit if no new items come in 3s
    for t in consumers:
        t.join()

    elapsed = perf_counter() - start
    log(f"✅ Condition demo completed in {elapsed:.2f} seconds")


if __name__ == "__main__":
    run_condition_demo()
