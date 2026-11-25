"""On-disk state: last run's watchlist and the per-film availability cache."""

import json
import os
from datetime import datetime, timedelta, timezone


def _load_json(path, default):
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return default


def _save_json(path, data):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    os.replace(tmp, path)  # atomic, so a crash never leaves a half-written file


def load_watchlist(path):
    """Last run's watchlist, or None if this is the first run."""
    return _load_json(path, None)


def save_watchlist(path, watchlist):
    _save_json(path, watchlist)


class Cache:
    """Maps (backend, region, title) -> services found plus when it was checked.

    Stores every recognised service, not just yours, so editing MY_SERVICES
    never forces a re-check.
    """

    def __init__(self, path, max_age_days):
        self.path = path
        self.max_age = timedelta(days=max_age_days)
        self.entries = _load_json(path, {})

    @staticmethod
    def key(backend, region, title):
        return f"{backend}|{region.upper()}|{title}"

    def get(self, backend, region, title, now=None):
        """Cached services if the entry is fresh, else None."""
        entry = self.entries.get(self.key(backend, region, title))
        if not entry:
            return None
        now = now or datetime.now(timezone.utc)
        try:
            checked = datetime.fromisoformat(entry["checked_at"])
        except (KeyError, ValueError):
            return None
        if now - checked > self.max_age:
            return None
        return entry["services"]

    def put(self, backend, region, title, services, now=None):
        now = now or datetime.now(timezone.utc)
        self.entries[self.key(backend, region, title)] = {
            "services": services,
            "checked_at": now.isoformat(timespec="seconds"),
        }

    def save(self):
        _save_json(self.path, self.entries)
