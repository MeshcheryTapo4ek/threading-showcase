"""
threading_vs_executor.py — Compares raw threading vs ThreadPoolExecutor on different workloads.

Workloads:
- IO-bound (sleep),
- CPU-bound (sum of squares),
- Hybrid (math + sleep).

Generates a timing comparison bar chart.
"""

import threading
from concurrent.futures import ThreadPoolExecutor
import random
from time import sleep, perf_counter
import matplotlib.pyplot as plt

from src.utils.logger import log

NUM_TASKS = 1500
WORKER_DELAY = (0.3, 0.5)


def io_heavy_work(task_id: int):
    sleep_time = round(random.uniform(*WORKER_DELAY), 2)
    sleep(sleep_time)
    return sleep_time


def cpu_heavy_work(task_id: int):
    total = sum(x ** 2 for x in range(100_000))
    return total


def hybrid_work(task_id: int):
    total = sum(x ** 2 for x in range(100_000))
    sleep(round(random.uniform(*WORKER_DELAY), 2))
    return total


def run_with_threads(work_fn):
    start = perf_counter()
    threads = []

    for i in range(NUM_TASKS):
        t = threading.Thread(target=work_fn, args=(i,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    return perf_counter() - start


def run_with_executor(work_fn):
    start = perf_counter()
    with ThreadPoolExecutor(max_workers=NUM_TASKS) as executor:
        list(executor.map(work_fn, range(NUM_TASKS)))
    return perf_counter() - start


def benchmark(label, work_fn):
    log(f"\n🧪 Benchmarking: {label}")
    t_thread = run_with_threads(work_fn)
    log(f"🧵 threading.Thread time: {t_thread:.2f}s")

    t_pool = run_with_executor(work_fn)
    log(f"⚙️ ThreadPoolExecutor time: {t_pool:.2f}s")

    return t_thread, t_pool


def plot_all(results):
    labels = list(results.keys())
    thread_times = [v[0] for v in results.values()]
    pool_times = [v[1] for v in results.values()]

    x = range(len(labels))
    width = 0.35

    plt.figure(figsize=(8, 5))
    plt.bar([i - width / 2 for i in x], thread_times, width=width, label='threading.Thread')
    plt.bar([i + width / 2 for i in x], pool_times, width=width, label='ThreadPoolExecutor')

    plt.ylabel("Total Time (s)")
    plt.title("Performance: threading vs ThreadPoolExecutor")
    plt.xticks(ticks=x, labels=labels)
    plt.legend()
    plt.tight_layout()

    # Show and save
    plt.savefig("threading_vs_executor.png", dpi=150)
    log("🖼️ Saved plot as 'threading_vs_executor.png'")
    plt.show()


def run_all_benchmarks():
    results = {
        "IO-bound": benchmark("IO-bound (sleep)", io_heavy_work),
        "CPU-bound": benchmark("CPU-bound (sum)", cpu_heavy_work),
        "Hybrid": benchmark("Hybrid (math + sleep)", hybrid_work),
    }
    plot_all(results)


if __name__ == "__main__":
    run_all_benchmarks()
