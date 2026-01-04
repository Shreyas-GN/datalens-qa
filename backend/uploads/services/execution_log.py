import time
from datetime import datetime


class ExecutionLogger:
    def __init__(self):
        self.started_at = datetime.utcnow().isoformat()
        self.steps = []

    def log_step(self, name, status, details=None, duration_ms=None):
        self.steps.append({
            "step": name,
            "status": status,  # success | warning | failed
            "details": details or {},
            "duration_ms": duration_ms,
        })

    def build_report(self):
        return {
            "started_at": self.started_at,
            "finished_at": datetime.utcnow().isoformat(),
            "steps": self.steps,
        }