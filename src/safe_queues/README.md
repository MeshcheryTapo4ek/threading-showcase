# 📦 Safe Queues — Thread-Safe Queues in Python

This module explores real-world patterns and safety mechanisms using `queue.Queue`.

All examples demonstrate:
- Blocking behavior;
- Timeouts and backpressure;
- Producer-consumer pipelines;
- Task tracking via `task_done()` and `join()`.

---

## 🔧 Overview

| Demo File                 | Focus                           | Pattern                       |
|---------------------------|----------------------------------|-------------------------------|
| `basic_queue_demo.py`     | Core API (put/get, qsize)       | Single producer/consumer      |
| `bounded_queue_example.py`| Backpressure via `maxsize`      | Slow consumer blocking producer |
| `queue_with_timeout.py`   | Timeouts for robustness         | Avoid stuck threads           |
| `producer_consumer_queue.py`| Multiple producers/consumers | Canonical PC pipeline         |
| `task_done_join_demo.py`  | Task tracking with `join()`     | Graceful completion tracking  |

---

## 🧠 Feature Comparison

| Feature                    | Basic | Bounded | Timeout | Multi-PC | Task Join |
|----------------------------|:-----:|:-------:|:-------:|:--------:|:---------:|
| Blocking behavior          | ✅    | ✅      | ✅      | ✅       | ✅        |
| Uses `maxsize`             | ✅    | ✅      | ✅      | ❌       | ❌        |
| Uses `timeout`             | ❌    | ❌      | ✅      | ❌       | ❌        |
| Uses `task_done()`         | ❌    | ❌      | ✅      | ✅       | ✅        |
| Uses `join()`              | ❌    | ❌      | ❌      | ✅       | ✅        |
| Multiple producers/consumers | ❌  | ❌      | ❌      | ✅       | ✅        |
| Daemon workers             | ❌    | ❌      | ❌      | ✅       | ✅        |

---

## 🛠 When to Use What

| Scenario                                     | Recommended Pattern               |
|---------------------------------------------|-----------------------------------|
| Just want a thread-safe queue               | `basic_queue_demo.py`            |
| Need to throttle fast producers             | `bounded_queue_example.py`       |
| Must avoid lock-ups / deadlocks             | `queue_with_timeout.py`          |
| Running real producer-consumer workloads    | `producer_consumer_queue.py`     |
| Need precise pipeline shutdown detection    | `task_done_join_demo.py`         |

---

## 🔍 Highlights

### `basic_queue_demo.py`
- Shows `put()`, `get()`, `qsize()`, `full()`, `empty()`;
- Producer blocks if queue is full;
- Consumer blocks if queue is empty.

### `bounded_queue_example.py`
- Queue with `maxsize = 2`;
- Consumer is intentionally slower;
- Demonstrates **backpressure** in action.

### `queue_with_timeout.py`
- Uses `.put(..., timeout=1.0)` and `.get(..., timeout=1.5)`;
- Producer may skip items;
- Consumer may exit early.

### `producer_consumer_queue.py`
- 2 producers, 3 consumers;
- Uses `.task_done()` and `.join()` to wait for full completion;
- Threads run as daemons — no manual cleanup needed.

### `task_done_join_demo.py`
- Single producer + multiple consumers;
- Demonstrates canonical usage of `.join()` for **graceful shutdown**.

---

## 🧾 Glossary

| Method             | Description                                |
|--------------------|--------------------------------------------|
| `put(item)`        | Add to queue, blocks if full               |
| `get()`            | Take from queue, blocks if empty           |
| `put(..., timeout)`| Waits up to timeout, raises `Full`         |
| `get(..., timeout)`| Waits up to timeout, raises `Empty`        |
| `task_done()`      | Mark item as processed                     |
| `join()`           | Block until all items marked done          |

---

## 🏁 TL;DR

| You want to...                                      | Use                           |
|-----------------------------------------------------|--------------------------------|
| Block until queue has room                          | `put()` or `put(timeout=...)` |
| Block until item is available                       | `get()` or `get(timeout=...)` |
| Avoid deadlocks or infinite waits                   | Use timeouts everywhere       |
| Track processing of each queue item                 | `task_done()` + `join()`      |
| Scale to many producers/consumers safely            | `Queue` with daemon threads   |
