"""
thread_class_demo.py — Demonstrates subclassing threading.Thread.

Each worker is an instance of a custom Thread subclass that:
- holds its own inputs and output,
- logs its execution flow,
- exposes a `.result` after joining.

This pattern is useful when you need full control over thread logic/state.
"""

import threading
import random
from time import sleep, perf_counter
from src.utils.logger import log

NUM_THREADS = 4


class WorkerThread(threading.Thread):
    def __init__(self, task_id: int, data: float):
        super().__init__(name=f"Worker-{task_id}")
        self.task_id = task_id
        self.data = data
        self.result = None

    def run(self):
        """
        Called when thread starts via .start().
        Simulates computation and stores result.
        """
        log(f"Thread-{self.task_id} starting with input={self.data}")
        delay = round(random.uniform(0.4, 0.8), 2)
        sleep(delay)
        self.result = self.data ** 2
        log(f"Thread-{self.task_id} finished in {delay}s, result={self.result}")


def run_thread_class_demo():
    start = perf_counter()

    log("🚀 Starting thread subclassing demo...")

    threads = []
    for i in range(NUM_THREADS):
        data = round(random.uniform(2.0, 5.0), 2)
        t = WorkerThread(task_id=i, data=data)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    log("✅ All threads finished. Results:")

    for t in threads:
        log(f" → Worker-{t.task_id} result = {t.result}")

    elapsed = perf_counter() - start
    log(f"✅ Thread subclass demo completed in {elapsed:.2f} seconds")


if __name__ == "__main__":
    run_thread_class_demo()
