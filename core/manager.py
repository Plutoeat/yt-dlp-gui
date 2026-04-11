import threading
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable, Optional

from core.task import DownloadTask, TaskStatus


class DownloadManager:
    """Manages a queue of DownloadTasks with concurrent execution.

    Pure-Python callback interface – no Qt dependency.

    Callbacks (all optional):
        on_progress(task_id, data)
        on_status_change(task_id, old_status, new_status)
        on_error(task_id, exception)
    """

    def __init__(
        self,
        max_workers: int = 3,
        *,
        on_progress: Optional[Callable] = None,
        on_status_change: Optional[Callable] = None,
        on_error: Optional[Callable] = None,
    ):
        self._max_workers = max_workers
        self._on_progress = on_progress
        self._on_status_change = on_status_change
        self._on_error = on_error

        self._tasks: dict[str, DownloadTask] = {}
        self._lock = threading.Lock()
        self._executor = ThreadPoolExecutor(max_workers=max_workers)

    # -- Public API ----------------------------------------------------------

    def add_task(self, url: str, ydl_opts: dict[str, Any]) -> str:
        """Create and enqueue a download task. Returns the task id."""
        task = DownloadTask(
            url,
            ydl_opts,
            on_progress=self._on_progress,
            on_status_change=self._on_status_change,
            on_error=self._on_error,
        )
        with self._lock:
            self._tasks[task.id] = task
        self._executor.submit(task.run)
        return task.id

    def cancel_task(self, task_id: str) -> bool:
        """Cancel a specific task. Returns True if the task was found."""
        with self._lock:
            task = self._tasks.get(task_id)
        if task is None:
            return False
        task.cancel()
        return True

    def cancel_all(self):
        """Cancel every active task."""
        with self._lock:
            tasks = list(self._tasks.values())
        for task in tasks:
            if task.status in (TaskStatus.PENDING, TaskStatus.RUNNING):
                task.cancel()

    def get_task(self, task_id: str) -> Optional[DownloadTask]:
        with self._lock:
            return self._tasks.get(task_id)

    def get_all_tasks(self) -> list[DownloadTask]:
        with self._lock:
            return list(self._tasks.values())

    def remove_finished(self):
        """Remove completed / failed / canceled tasks from the list."""
        terminal = {TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.CANCELED}
        with self._lock:
            self._tasks = {
                tid: t for tid, t in self._tasks.items() if t.status not in terminal
            }

    def extract_info(
        self,
        url: str,
        on_result: Callable,
        on_error: Callable,
        ydl_opts: dict[str, Any] | None = None,
    ):
        """Submit an info extraction job (no download).

        Calls on_result(url, info_dict) or on_error(url, error_msg).
        """
        from core.info_extractor import extract_info as _extract

        def _run():
            try:
                info = _extract(url, ydl_opts)
                on_result(url, info)
            except Exception as e:
                on_error(url, str(e))

        self._executor.submit(_run)

    def shutdown(self, wait: bool = True):
        """Cancel all tasks and shut down the thread pool."""
        self.cancel_all()
        self._executor.shutdown(wait=wait)
