"""
thread_inspection.py — Inspect all running threads and dump their stack traces.

Useful for:
- debugging concurrency issues,
- understanding which threads are alive and what they are doing.

Demonstrates:
- named and unnamed threads,
- live stack extraction via sys._current_frames().
"""

import threading
import time
import sys
import traceback
from src.utils.logger import log

def dump_threads():
    """
    Logs a dump of all currently running threads, including their call stacks.
    Uses sys._current_frames() to retrieve the execution stack of each thread.
    """
    log("\n🧵 Dumping all active threads and their call stacks...")

    frames = sys._current_frames()

    for thread in threading.enumerate():
        log(f"\n--- Thread: name={thread.name}, ident={thread.ident}, daemon={thread.daemon}")
        frame = frames.get(thread.ident)
        if frame:
            for filename, lineno, func, line in traceback.extract_stack(frame):
                log(f"  {filename}:{lineno} in {func}")
                if line:
                    log(f"    → {line.strip()}")
        else:
            log("  No stack frame available.")


def long_running_task(name: str = None):
    """
    Simulates a thread that stays alive for a while.
    Optionally sets the thread name.
    """
    if name:
        threading.current_thread().name = name

    log(f"{threading.current_thread().name} starting.")
    for i in range(5):
        time.sleep(1)
    log(f"{threading.current_thread().name} finishing.")


def run_demo():
    log("🚀 Starting thread inspection demo...")

    # Launch named threads
    threads = [
        threading.Thread(target=long_running_task, args=(f"Worker-{i}",)) for i in range(2)
    ]

    # Launch anonymous threads (no name set explicitly)
    threads += [
        threading.Thread(target=long_running_task) for _ in range(2)
    ]

    for t in threads:
        t.start()

    # Give threads time to start and enter sleep
    time.sleep(2)

    # Dump current threads and their stacks
    dump_threads()

    # Wait for all threads to finish
    for t in threads:
        t.join()

    log("✅ Thread inspection demo complete.")


if __name__ == "__main__":
    run_demo()
