"""
producer_consumer_queue.py — Classic producer-consumer pattern using queue.Queue.

Multiple producers push items into a shared queue,
and multiple consumers pull and process them.

We use task_done() and join() to know when all items have been processed.
This is the idiomatic and safest way to coordinate producer-consumer threads.
"""

import threading
import random
from queue import Queue
from time import sleep, perf_counter
from src.utils.logger import log

NUM_PRODUCERS = 2
NUM_CONSUMERS = 3
ITEMS_PER_PRODUCER = 5

# Shared thread-safe queue
q = Queue()


def producer(producer_id: int):
    for item_id in range(ITEMS_PER_PRODUCER):
        item = f"p{producer_id}-i{item_id}"
        sleep(random.uniform(0.1, 0.4))  # simulate producing
        q.put(item)
        log(f"Producer {producer_id} added {item} (queue size: {q.qsize()})")


def consumer(consumer_id: int):
    while True:
        item = q.get()  # blocks if empty
        log(f"Consumer {consumer_id} got {item}")
        sleep(random.uniform(0.2, 0.5))  # simulate processing
        q.task_done()
        log(f"Consumer {consumer_id} finished {item}")


def run_producer_consumer_demo():
    start = perf_counter()

    log("🚀 Starting producer-consumer queue demo with task tracking...")

    # Start consumers (they will block on empty queue)
    for cid in range(NUM_CONSUMERS):
        threading.Thread(target=consumer, args=(cid,), name=f"Consumer-{cid}", daemon=True).start()

    # Start producers
    producers = [
        threading.Thread(target=producer, args=(pid,), name=f"Producer-{pid}")
        for pid in range(NUM_PRODUCERS)
    ]
    for t in producers: t.start()

    # Wait for all producers to finish
    for t in producers: t.join()

    # Wait until queue is fully processed
    q.join()  # blocks until every put() has a matching task_done()

    elapsed = perf_counter() - start
    log(f"✅ Producer-consumer demo completed in {elapsed:.2f} seconds")


if __name__ == "__main__":
    run_producer_consumer_demo()
