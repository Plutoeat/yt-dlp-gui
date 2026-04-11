"""Adapter layer: pure-Python callbacks → Qt Signals for thread-safe GUI updates."""

from PySide6.QtCore import QObject, Signal


class DownloadBridge(QObject):
    """Bridges DownloadManager callbacks into Qt signals.

    Connect these signals to GUI slots for thread-safe updates.
    """

    # Download task signals
    progress = Signal(str, dict)            # task_id, progress data
    status_changed = Signal(str, str, str)  # task_id, old_status, new_status
    error = Signal(str, str)                # task_id, error message

    # Info extraction signals
    info_extracted = Signal(str, dict)      # url, info_dict
    info_error = Signal(str, str)           # url, error message

    def on_progress(self, task_id: str, data: dict):
        self.progress.emit(task_id, data)

    def on_status_change(self, task_id: str, old_status, new_status):
        self.status_changed.emit(task_id, old_status.value, new_status.value)

    def on_error(self, task_id: str, exc: Exception):
        self.error.emit(task_id, str(exc))

    def on_info_result(self, url: str, info: dict):
        self.info_extracted.emit(url, info)

    def on_info_error(self, url: str, error_msg: str):
        self.info_error.emit(url, error_msg)
