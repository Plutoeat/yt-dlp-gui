"""Download task table – shows progress, status, speed for each task."""

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QColor
from PySide6.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QGroupBox,
    QHeaderView,
    QMenu,
    QProgressBar,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
)


_COL_ID = 0
_COL_TITLE = 1
_COL_STATUS = 2
_COL_PROGRESS = 3
_COL_SPEED = 4
_COL_ETA = 5
_COL_ACTION = 6
_COLUMNS = ["ID", "Title / URL", "Status", "Progress", "Speed", "ETA", "Action"]

_STATUS_COLORS = {
    "completed": QColor("#2ecc71"),
    "failed": QColor("#e74c3c"),
    "canceled": QColor("#e67e22"),
    "interrupted": QColor("#e67e22"),
    "running": QColor("#3498db"),
    "pending": QColor("#95a5a6"),
}


class TaskTableWidget(QGroupBox):
    def __init__(self, parent=None):
        super().__init__("Tasks", parent)
        layout = QVBoxLayout(self)

        self._table = QTableWidget(0, len(_COLUMNS))
        self._table.setHorizontalHeaderLabels(_COLUMNS)
        self._table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self._table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self._table.setAlternatingRowColors(True)
        self._table.verticalHeader().setVisible(False)
        self._table.verticalHeader().setDefaultSectionSize(36)
        self._table.horizontalHeader().setSectionResizeMode(
            _COL_TITLE, QHeaderView.Stretch
        )
        self._table.horizontalHeader().setSectionResizeMode(
            _COL_PROGRESS, QHeaderView.Fixed
        )
        self._table.horizontalHeader().setSectionResizeMode(
            _COL_ACTION, QHeaderView.Fixed
        )
        self._table.setColumnWidth(_COL_PROGRESS, 140)
        self._table.setColumnWidth(_COL_ID, 60)
        self._table.setColumnWidth(_COL_ACTION, 72)
        self._table.setColumnWidth(_COL_SPEED, 90)
        self._table.setColumnWidth(_COL_ETA, 60)
        self._table.setContextMenuPolicy(Qt.CustomContextMenu)
        self._table.customContextMenuRequested.connect(self._show_context_menu)
        layout.addWidget(self._table)

        # task_id → (row index, url, cancel callback)
        self._row_map: dict[str, int] = {}
        self._urls: dict[str, str] = {}
        self._cancel_callbacks: dict[str, callable] = {}
        self._retry_callback: callable = None
        self._delete_callback: callable = None  # called with task_id to remove from history

    def set_retry_callback(self, cb: callable):
        self._retry_callback = cb

    def set_delete_callback(self, cb: callable):
        self._delete_callback = cb

    def delete_task_row(self, task_id: str):
        """Remove a row from the table."""
        row = self._row_map.get(task_id)
        if row is None:
            return
        self._table.removeRow(row)
        del self._row_map[task_id]
        self._urls.pop(task_id, None)
        self._cancel_callbacks.pop(task_id, None)
        # Rebuild row_map since indices shifted
        self._row_map = {}
        for r in range(self._table.rowCount()):
            tid = self._table.item(r, _COL_ID).text()
            self._row_map[tid] = r

    def add_task(self, task_id: str, url: str, cancel_cb: callable):
        row = self._table.rowCount()
        self._table.insertRow(row)
        self._row_map[task_id] = row
        self._urls[task_id] = url
        self._cancel_callbacks[task_id] = cancel_cb

        self._table.setItem(row, _COL_ID, QTableWidgetItem(task_id))
        display = url if len(url) <= 70 else url[:67] + "…"
        self._table.setItem(row, _COL_TITLE, QTableWidgetItem(display))

        status_item = QTableWidgetItem("pending")
        status_item.setForeground(_STATUS_COLORS["pending"])
        self._table.setItem(row, _COL_STATUS, status_item)

        self._table.setItem(row, _COL_SPEED, QTableWidgetItem(""))
        self._table.setItem(row, _COL_ETA, QTableWidgetItem(""))

        progress = QProgressBar()
        progress.setRange(0, 100)
        progress.setValue(0)
        self._table.setCellWidget(row, _COL_PROGRESS, progress)

        btn = QPushButton("Cancel")
        btn.setFixedHeight(28)
        btn.setStyleSheet("padding: 2px 8px; font-size: 11px;")
        btn.clicked.connect(lambda: self._on_cancel(task_id))
        self._table.setCellWidget(row, _COL_ACTION, btn)

    def update_progress(self, task_id: str, data: dict):
        row = self._row_map.get(task_id)
        if row is None:
            return
        pbar = self._table.cellWidget(row, _COL_PROGRESS)

        # Update title from info_dict if available
        info = data.get("info_dict", {})
        title = info.get("title")
        if title:
            current = self._table.item(row, _COL_TITLE).text()
            if current.startswith("http"):
                self._table.item(row, _COL_TITLE).setText(
                    title if len(title) <= 70 else title[:67] + "…"
                )

        status = data.get("status", "")
        if status == "downloading":
            total = data.get("total_bytes") or data.get("total_bytes_estimate") or 0
            downloaded = data.get("downloaded_bytes", 0)
            if total > 0:
                pbar.setValue(int(downloaded / total * 100))
            self._table.item(row, _COL_SPEED).setText(data.get("_speed_str", ""))
            self._table.item(row, _COL_ETA).setText(data.get("_eta_str", ""))
        elif status == "finished":
            pbar.setValue(100)
            self._table.item(row, _COL_SPEED).setText("")
            self._table.item(row, _COL_ETA).setText("")

    def update_status(self, task_id: str, new_status: str):
        row = self._row_map.get(task_id)
        if row is None:
            return
        item = self._table.item(row, _COL_STATUS)
        item.setText(new_status)
        color = _STATUS_COLORS.get(new_status, QColor("#95a5a6"))
        item.setForeground(color)

        if new_status in ("completed", "failed", "canceled", "interrupted"):
            btn = self._table.cellWidget(row, _COL_ACTION)
            if btn:
                if new_status in ("failed", "canceled", "interrupted"):
                    btn.setText("Retry")
                    btn.setEnabled(True)
                    try:
                        btn.clicked.disconnect()
                    except RuntimeError:
                        pass
                    btn.clicked.connect(lambda: self._on_retry(task_id))
                else:
                    btn.setEnabled(False)
                    btn.setText("Done")

    def _on_cancel(self, task_id: str):
        cb = self._cancel_callbacks.get(task_id)
        if cb:
            cb(task_id)

    def _on_retry(self, task_id: str):
        url = self._urls.get(task_id)
        if url and self._retry_callback:
            # Remove old row first, then retry creates a fresh one
            self.delete_task_row(task_id)
            self._retry_callback(task_id, url)

    def _show_context_menu(self, pos):
        row = self._table.rowAt(pos.y())
        if row < 0:
            return

        task_id = self._table.item(row, _COL_ID).text()
        url = self._urls.get(task_id, "")

        menu = QMenu(self)

        copy_action = QAction("Copy URL", self)
        copy_action.triggered.connect(lambda: QApplication.clipboard().setText(url))
        menu.addAction(copy_action)

        cancel_action = QAction("Cancel", self)
        cancel_action.triggered.connect(lambda: self._on_cancel(task_id))
        menu.addAction(cancel_action)

        if self._retry_callback:
            retry_action = QAction("Retry", self)
            retry_action.triggered.connect(lambda: self._on_retry(task_id))
            menu.addAction(retry_action)

        menu.addSeparator()
        delete_action = QAction("Delete from List", self)
        delete_action.triggered.connect(lambda: self._on_delete(task_id))
        menu.addAction(delete_action)

        menu.exec(self._table.viewport().mapToGlobal(pos))

    def _on_delete(self, task_id: str):
        """Delete a task row and notify history."""
        self.delete_task_row(task_id)
        if self._delete_callback:
            self._delete_callback(task_id)
