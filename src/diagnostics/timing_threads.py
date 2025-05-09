"""
timing_threads.py — Track thread lifetimes across multiple runs by name.

Each time a thread starts and finishes, we record how long it lived.
Results are grouped and summarized by thread name (not instance).
"""

import threading
from time import perf_counter, sleep
import random
from collections import defaultdict
from src.utils.logger import log

# Grouped lifetime durations by thread name
thread_lifetime_stats = defaultdict(list)


def simulated_task():
    """
    Simulated work: random delay.
    """
    sleep_time = round(random.uniform(0.2, 0.8), 2)
    sleep(sleep_time)


class TimedThread(threading.Thread):
    """
    Thread that tracks its own start and end time.
    Lifetime is recorded into a global stats dict by name.
    """
    def __init__(self, name: str, num_tasks: int):
        super().__init__(name=name)
        self.num_tasks = num_tasks
        self._start_time = None
        self._end_time = None

    def run(self):
        self._start_time = perf_counter()
        log(f"{self.name} started.")
        for _ in range(self.num_tasks):
            simulated_task()
        self._end_time = perf_counter()
        log(f"{self.name} finished.")
        duration = self._end_time - self._start_time
        thread_lifetime_stats[self.name].append(duration)


def run_demo():
    log("🚀 Starting repeated thread lifetime tracking demo...")

    NUM_CYCLES = 3
    WORKERS = ["Worker-A", "Worker-B"]

    threads = []
    for cycle in range(NUM_CYCLES):
        for name in WORKERS:
            t = TimedThread(name=name, num_tasks=3)
            t.start()
            threads.append(t)

    for t in threads:
        t.join()

    log("\n📊 Aggregated lifetime stats by thread name:")
    for name, durations in thread_lifetime_stats.items():
        avg = sum(durations) / len(durations)
        log(f"{name}: runs={len(durations)}, min={min(durations):.3f}s, "
            f"max={max(durations):.3f}s, avg={avg:.3f}s, total={sum(durations):.2f}s")

    log("✅ Thread lifetime aggregation demo complete.")


if __name__ == "__main__":
    run_demo()
