"""Download history persistence – survives app restarts."""

import json
import os
import time
from typing import Any

_ROOT = os.path.normpath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_HISTORY_FILE = os.path.join(_ROOT, "configs", "download_history.json")


class DownloadHistory:
    """Persists download task records to JSON."""

    def __init__(self, path: str = _HISTORY_FILE):
        self._path = path
        self._records: list[dict[str, Any]] = []
        self._load()

    def _load(self):
        if os.path.isfile(self._path):
            try:
                with open(self._path, "r", encoding="utf-8") as f:
                    self._records = json.load(f)
            except (json.JSONDecodeError, OSError):
                self._records = []

    def _save(self):
        os.makedirs(os.path.dirname(self._path), exist_ok=True)
        with open(self._path, "w", encoding="utf-8") as f:
            json.dump(self._records, f, indent=2, ensure_ascii=False)

    def add(self, task_id: str, url: str, title: str = ""):
        self._records.append({
            "task_id": task_id,
            "url": url,
            "title": title,
            "status": "running",
            "progress": 0,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        })
        self._save()

    def update_status(self, task_id: str, status: str):
        for r in self._records:
            if r["task_id"] == task_id:
                r["status"] = status
                break
        self._save()

    def update_title(self, task_id: str, title: str):
        for r in self._records:
            if r["task_id"] == task_id:
                if not r.get("title"):
                    r["title"] = title
                break
        self._save()

    def get_all(self) -> list[dict[str, Any]]:
        return list(self._records)

    def clear_completed(self):
        self._records = [r for r in self._records if r["status"] not in ("completed", "failed", "canceled")]
        self._save()

    def delete(self, task_id: str):
        self._records = [r for r in self._records if r["task_id"] != task_id]
        self._save()

    def clear_all(self):
        self._records = []
        self._save()
