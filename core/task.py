import enum
import threading
import uuid
from typing import Any, Callable, Optional

import yt_dlp


class TaskStatus(enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELED = "canceled"


class DownloadTask:
    """Wraps a single yt-dlp download with status tracking and progress callbacks.

    Callbacks (all optional):
        on_progress(task_id, data)  – called by yt-dlp progress_hooks
        on_status_change(task_id, old_status, new_status)
        on_error(task_id, exception)
    """

    def __init__(
        self,
        url: str,
        ydl_opts: dict[str, Any],
        *,
        on_progress: Optional[Callable] = None,
        on_status_change: Optional[Callable] = None,
        on_error: Optional[Callable] = None,
    ):
        self.id: str = uuid.uuid4().hex[:8]
        self.url = url
        self.ydl_opts = dict(ydl_opts)  # shallow copy
        self._status = TaskStatus.PENDING
        self._cancel_event = threading.Event()
        self._error: Optional[Exception] = None

        self._on_progress = on_progress
        self._on_status_change = on_status_change
        self._on_error = on_error

        # Inject our progress hook
        hooks = list(self.ydl_opts.get("progress_hooks", []))
        hooks.append(self._progress_hook)
        self.ydl_opts["progress_hooks"] = hooks

    # -- Properties ----------------------------------------------------------

    @property
    def status(self) -> TaskStatus:
        return self._status

    @property
    def error(self) -> Optional[Exception]:
        return self._error

    # -- Control -------------------------------------------------------------

    def cancel(self):
        """Request cancellation. Safe to call from any thread."""
        self._cancel_event.set()

    # -- Execution (called in worker thread) ---------------------------------

    def run(self):
        """Execute the download. Blocks until done / failed / canceled."""
        self._set_status(TaskStatus.RUNNING)
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                # yt-dlp checks this attribute each iteration
                ydl._download_retcode = 0

                # Patch ydl to respect cancel event
                original_dl = ydl.download

                def cancellable_download(urls):
                    if self._cancel_event.is_set():
                        return
                    return original_dl(urls)

                cancellable_download([self.url])

            if self._cancel_event.is_set():
                self._set_status(TaskStatus.CANCELED)
            else:
                self._set_status(TaskStatus.COMPLETED)

        except Exception as exc:
            if self._cancel_event.is_set():
                self._set_status(TaskStatus.CANCELED)
            else:
                self._error = exc
                self._set_status(TaskStatus.FAILED)
                if self._on_error:
                    self._on_error(self.id, exc)

    # -- Internal ------------------------------------------------------------

    def _set_status(self, new: TaskStatus):
        old = self._status
        if old == new:
            return
        self._status = new
        if self._on_status_change:
            self._on_status_change(self.id, old, new)

    def _progress_hook(self, data: dict):
        if self._cancel_event.is_set():
            raise yt_dlp.utils.DownloadError("Download canceled by user")
        if self._on_progress:
            self._on_progress(self.id, data)
