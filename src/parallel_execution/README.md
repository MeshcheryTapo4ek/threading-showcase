# 🧵 Parallel Execution — Modern Threading Patterns in Python

This module explores ways to execute multiple tasks concurrently using Python threads and `ThreadPoolExecutor`.

Each demo shows:
- Thread lifecycle & structure
- Result handling (manual & via futures)
- Exception safety
- Performance comparison (IO vs CPU)

---

## 🔧 Overview of Examples

| Demo File                  | Concept Highlighted                        | API Used                      |
|----------------------------|---------------------------------------------|-------------------------------|
| `basic_thread_demo.py`     | Manual thread creation & joining           | `threading.Thread`            |
| `thread_with_args.py`      | Passing args & collecting results manually | `threading.Thread + Queue`    |
| `thread_class_demo.py`     | Subclassing Thread                         | `Custom Thread subclass`      |
| `thread_pool_executor.py`  | Submitting tasks with futures              | `ThreadPoolExecutor.submit()` |
| `thread_pool_map_demo.py`  | Batch execution with ordered results       | `ThreadPoolExecutor.map()`    |
| `futures_with_results.py`  | Handling results via `.result()`           | `submit + result`             |
| `exceptions_in_threads.py` | Catching exceptions in threads             | `Future.result()`             |
| `wait_as_completed_demo.py`| Handling futures as they finish            | `as_completed()`              |
| `threading_vs_executor.py` | Performance: thread vs executor            | All of the above + benchmark  |

---

## 🧠 Feature Comparison

| Feature                  | `Thread` | `Thread subclass` | `ThreadPoolExecutor` |
|--------------------------|----------|--------------------|-----------------------|
| Manual start/stop        | ✅       | ✅                 | ❌ (auto-managed)     |
| Pass args to worker      | ✅       | ✅                 | ✅                   |
| Return result easily     | ❌       | ✅ via `.result`   | ✅                   |
| Exception handling       | ❌       | ❌                 | ✅ via `.result()`    |
| Easy scaling             | ❌       | ❌                 | ✅                   |
| Preserves input order    | ❌       | ✅ (manual)        | ✅ (`map`, `.result`) |
| Processes results as done| ❌       | ❌                 | ✅ (`as_completed`)   |
| Best for production      | 🔴 No    | 🟡 Sometimes        | 🟢 Yes                |

---

## 🧪 When to Use What

| Use Case                                 | Recommended Pattern               |
|------------------------------------------|-----------------------------------|
| Quick test, low scale                    | `basic_thread_demo.py`           |
| Custom logic/state per thread            | `thread_class_demo.py`           |
| Need returned results                    | `futures_with_results.py`        |
| Tasks can fail — handle it!              | `exceptions_in_threads.py`       |
| Need task order preserved                | `thread_pool_map_demo.py`        |
| React to fastest results                 | `wait_as_completed_demo.py`      |
| Compare real performance                 | `threading_vs_executor.py`       |

---

## 📊 Performance: Thread vs Executor

`threading_vs_executor.py` benchmarks:

| Workload Type | `threading.Thread` | `ThreadPoolExecutor` |
|---------------|--------------------|-----------------------|
| IO-bound      | 🟢 Slightly faster  | 🟡                    |
| CPU-bound     | 🟡 Slower (GIL)     | 🟡                    |
| Hybrid        | 🟡 Comparable       | 🟢 Slightly better     |

→ In CPU-heavy tasks, neither will help much. Use `multiprocessing` or `joblib` instead.

