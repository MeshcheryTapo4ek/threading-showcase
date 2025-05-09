# 🧵 Threading Showcase in Python

Welcome to my personal Python threading playground.

This repo is where I experiment, learn, and document all things multithreading — from the basics to the weird edge cases that make you say “...wait, what?”

Whether you're trying to **use threads properly**, avoid common **gotchas**, or just want to see what happens when things go hilariously wrong — it should be here.

---

## 🧠 What’s Inside?

| Folder                    | What's Going On Here                                                  |
|---------------------------|------------------------------------------------------------------------|
| `src/synchronization/`    | All the classic stuff: `Lock`, `Event`, `Semaphore`, `Barrier`, `Condition` |
| `src/safe_queues/`        | Safe and scalable producer–consumer patterns using `queue.Queue`      |
| `src/parallel_execution/` | Raw threads vs `ThreadPoolExecutor`, results, exceptions, benchmarks  |
| `src/diagnostics/`        | How to introspect running threads, measure memory, detect issues      |
| `src/pitfalls_and_errors/`| The dangerous: race conditions, deadlocks, livelocks, leaks, etc. |
| `src/utils/logger.py`     | Simple but sexy logger with timestamps and thread names               |

---

## 🧪 How to Run

```bash
# Run any script directly, they’re all standalone
python3 src/synchronization/lock_demo.py
python3 src/safe_queues/queue_with_timeout.py
python3 src/parallel_execution/threading_vs_executor.py
```

All scripts:
- Run out of the box
- Have readable output
- Teach one thing, clearly

Wanna check for memory leaks or CPU load per thread?  
Run the diagnostics demos and you’ll even get charts. 📈

---

## 🎯 Why I Built This

Because threading in Python is deceptively simple — until it isn’t.

This repo helps me:
- Cement concepts by building them out
- Create copy-pastable reference demos
- Avoid saying "damn, I forgot how `Condition` works again"

---

## 🙌 Contribute?

Honestly, this is mostly for me — but if you’ve got a weird edge case or a cool trick, I’m all ears. PRs welcome.

---
