import threading
from datetime import datetime

# Global state to track last log time (per thread is overkill here)
_last_log_time = None


def log(message: str, *, prefix: str = ""):
    """
    Logs a message with timestamp, delta since last log, and current thread name.

    Example:
    [12:34:56.789 | +123ms] [Thread-1] [my_module] Starting work...
    """
    global _last_log_time
    now = datetime.now()
    now_str = now.strftime('%H:%M:%S.%f')[:-3]
    thread_name = threading.current_thread().name
    module_tag = f"[{prefix}]" if prefix else ""

    # Compute time since last log
    if _last_log_time is None:
        delta_str = "   ---"
    else:
        delta_ms = (now - _last_log_time).total_seconds() * 1000
        delta_str = f"+{delta_ms:6.1f}ms"

    _last_log_time = now
    print(f"[{now_str} | {delta_str}] [{thread_name}] {module_tag} {message}")
