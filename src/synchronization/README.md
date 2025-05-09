# 🧵 Thread Synchronization — Python `threading` Primitives

This section demonstrates Python's core synchronization tools from the `threading` module.

Each demo is:
- Isolated and focused;
- Logged with timestamps and thread names;
- Realistic via randomized delays and timeouts.

---

## 🔧 Overview

| 🧩 Primitive   | 📁 File                    | 🎯 Scenario                       |
|---------------|----------------------------|-----------------------------------|
| `Lock`        | `lock_demo.py`             | Race condition / counter update   |
| `Condition`   | `condition_demo.py`        | Producer ↔ Consumer signaling     |
| `Event`       | `event_demo.py`            | Broadcast signal to many workers |
| `Barrier`     | `barrier_demo.py`          | Thread checkpoint + failure path |
| `Semaphore`   | `semaphore_demo.py`        | Limit concurrent access           |

---

## 🧠 Primitive Comparison

| Feature               | `Lock` | `Condition` | `Event` | `Barrier` | `Semaphore` |
|-----------------------|--------|-------------|---------|-----------|-------------|
| One-to-one            | ✅     | ✅           | ❌      | ❌        | ❌          |
| One-to-many           | ❌     | ✅           | ✅      | ❌        | ❌          |
| Group-to-group sync   | ❌     | ❌           | ❌      | ✅        | ❌          |
| Resource limiting     | ❌     | ❌           | ❌      | ❌        | ✅          |
| `wait()` support      | ❌     | ✅           | ✅      | ✅        | ❌          |
| `notify()`/`set()`    | ❌     | ✅           | ✅      | ❌        | ❌          |
| Timeout support       | ❌     | ✅           | ✅      | ✅        | ❌          |
| Reusable              | ✅     | ✅           | ✅      | Manual    | ✅          |
| Simplicity            | 🟢 Easy| 🟡 Medium     | 🟢 Easy | meh idk | 🟡 Medium    |

---

## 🧭 Use Case Guide

| Goal                                 | Use...        |
|--------------------------------------|---------------|
| Protect one critical section         | `Lock`        |
| Signal between producers/consumers   | `Condition`   |
| Broadcast "go" to many threads       | `Event`       |
| Wait for all threads to reach point  | `Barrier`     |
| Throttle concurrency (e.g. DB pool)  | `Semaphore`   |

---

## 🧪 What each file demonstrates

### `lock_demo.py`
- ❌ Without `Lock`: counter is corrupted (race condition);
- ✅ With `Lock`: expected result every time;
- 👁 Useful for beginners to understand concurrency issues.

### `condition_demo.py`
- 🎯 Shared buffer with capacity;
- Producers wait if full, consumers if empty;
- ⏱ Includes timeouts and graceful exit;
- 🔁 Demonstrates classic bounded-buffer pattern.

### `event_demo.py`
- 👷 Workers wait for event signal;
- 📡 If received → they work; otherwise timeout;
- 🔄 Phase-based coordination with round resets;
- 🧠 Clean, elegant broadcast sync.

### `barrier_advanced_demo.py`
- 🧍 Threads reach a shared checkpoint;
- 💣 One intentionally breaks it (timeout);
- ❗ Others detect failure, exit gracefully;
- 🛠 Coordinator resets barrier (optional recovery flow).

### `semaphore_demo.py`
- 🎟 Up to N workers can access resource simultaneously;
- 🚥 Others wait until a slot is released;
- 🧰 Classic use-case: DB connections, GPU slots, API limits.

---

## ✅ Common Features

| Feature               | Present |
|------------------------|--------|
| Randomized timing      | ✅      |
| Timeouts and exits     | ✅      |
| Named threads / logs   | ✅      |
| Coordinator patterns   | ✅      |
| Clean shutdown         | ✅      |

---

## 📊 Suggested Diagrams

| Concept     | Diagram Type | Show...                                   |
|-------------|--------------|-------------------------------------------|
| `Condition` | State diagram| Buffer full/empty transitions             |
| `Event`     | Timeline     | Workers waiting → signal broadcast        |
| `Barrier`   | Sequence     | Threads waiting → timeout → break/reset   |
| `Semaphore` | Slot counter | Active vs queued threads over time        |
| `Lock`      | Counter table| Actual vs expected count w/ and w/o lock  |


---

## 🏁 TL;DR — Pick the Right Tool

| Need                              | Use           |
|-----------------------------------|----------------|
| Mutex for shared variables        | `Lock`         |
| Conditional wait + wake           | `Condition`    |
| Phase transition / mass signal    | `Event`        |
| Thread checkpoint sync            | `Barrier`      |
| Throttle concurrent workers       | `Semaphore`    |
