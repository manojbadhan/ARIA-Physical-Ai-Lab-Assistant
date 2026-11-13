import time

class UsageTracker:
    """Fires once when a tool has been visible for `hold` seconds (used to snap a 'student using tool' photo)."""
    def __init__(self, hold=3.0, cooldown=60.0):
        self.hold, self.cooldown = hold, cooldown
        self.first, self.fired = {}, {}

    def update(self, labels, now=None):
        now = time.time() if now is None else now; ready = []
        for l in set(labels):
            self.first.setdefault(l, now)
            if now - self.first[l] >= self.hold and now - self.fired.get(l, float("-inf")) >= self.cooldown:
                self.fired[l] = now; ready.append(l)
        for l in list(self.first):
            if l not in labels: del self.first[l]
        return ready
