"""Main application window."""

from PySide6.QtCore import Slot
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from configs.app_settings import AppSettings
from configs.ydl_opts import build_opts
from core.ffmpeg_utils import is_ffmpeg_available, get_default_format
from core.history import DownloadHistory
from core.manager import DownloadManager
from gui.bridge import DownloadBridge
from gui.theme_manager import apply_theme
from gui.widgets.format_preview import FormatPreviewDialog
from gui.widgets.log_viewer import LogViewerWidget
from gui.widgets.preset_bar import PresetBar
from gui.widgets.settings_dialog import SettingsDialog
from gui.widgets.task_table import TaskTableWidget
from gui.widgets.url_input import UrlInputWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("yt-dlp GUI")

        self._settings = AppSettings()
        self.resize(
            self._settings.get("window_width", 900),
            self._settings.get("window_height", 640),
        )

        self._bridge = DownloadBridge()
        self._manager = DownloadManager(
            max_workers=self._settings.get("max_workers", 3),
            on_progress=self._bridge.on_progress,
            on_status_change=self._bridge.on_status_change,
            on_error=self._bridge.on_error,
        )

        self._active_count = 0
        self._completed_count = 0
        self._history = DownloadHistory()

        # Settings panel lives in its own dialog
        self._settings_dialog = SettingsDialog(self)

        self._init_menubar()
        self._init_ui()
        self._connect_signals()
        self._load_settings()
        self._load_history()
        self._update_ffmpeg_status()

    def _init_menubar(self):
        menubar = self.menuBar()

        view_menu = menubar.addMenu("View")
        self._theme_action = view_menu.addAction("Switch to Dark Mode")
        self._theme_action.triggered.connect(self._toggle_theme)
        view_menu.addSeparator()
        clear_history_action = view_menu.addAction("Clear Download History")
        clear_history_action.triggered.connect(self._clear_history)

        help_menu = menubar.addMenu("Help")
        about_action = help_menu.addAction("About")
        about_action.triggered.connect(self._show_about)

    def _init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(16, 12, 16, 10)
        layout.setSpacing(10)

        # URL input
        self._url_input = UrlInputWidget()
        layout.addWidget(self._url_input)

        # Preset bar + Settings button
        preset_row = QHBoxLayout()
        preset_row.setSpacing(8)
        self._preset_bar = PresetBar()
        preset_row.addWidget(self._preset_bar, stretch=1)

        self._btn_settings = QPushButton("Settings…")
        self._btn_settings.setToolTip("打开详细下载设置 (格式、字幕、后处理、认证等)")
        self._btn_settings.setMinimumHeight(32)
        preset_row.addWidget(self._btn_settings)
        layout.addLayout(preset_row)

        # Action buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)
        self._btn_download = QPushButton("Start Download")
        self._btn_download.setObjectName("btn_download")
        self._btn_download.setMinimumHeight(44)

        self._btn_cancel_all = QPushButton("Cancel All")
        self._btn_cancel_all.setObjectName("btn_cancel_all")
        self._btn_cancel_all.setMinimumHeight(44)

        btn_layout.addWidget(self._btn_download, stretch=3)
        btn_layout.addWidget(self._btn_cancel_all, stretch=1)
        layout.addLayout(btn_layout)

        # Task table (takes remaining space)
        self._task_table = TaskTableWidget()
        self._task_table.set_retry_callback(self._retry_url)
        self._task_table.set_delete_callback(self._delete_task)
        layout.addWidget(self._task_table, stretch=1)

        # Log viewer
        self._log_viewer = LogViewerWidget()
        layout.addWidget(self._log_viewer)

    def _connect_signals(self):
        self._btn_download.clicked.connect(self._on_download)
        self._btn_cancel_all.clicked.connect(self._on_cancel_all)
        self._btn_settings.clicked.connect(self._on_open_settings)
        self._bridge.progress.connect(self._on_progress)
        self._bridge.status_changed.connect(self._on_status_changed)
        self._bridge.error.connect(self._on_error)
        self._bridge.info_extracted.connect(self._on_info_extracted)
        self._bridge.info_error.connect(self._on_info_error)
        self._url_input.format_requested.connect(self._on_list_formats)
        self._preset_bar.preset_selected.connect(self._on_preset_selected)
        self._preset_bar._btn_save.clicked.connect(self._on_save_preset)

    def _load_settings(self):
        self._settings_dialog.settings_panel.apply_settings(self._settings.to_dict())
        theme = self._settings.get("theme", "light")
        self._theme_action.setText(
            "Switch to Light Mode" if theme == "dark" else "Switch to Dark Mode"
        )

    def _save_settings(self):
        s = self._settings_dialog.settings_panel.collect_settings_dict()
        s["window_width"] = self.width()
        s["window_height"] = self.height()
        s["theme"] = self._settings.get("theme", "light")
        self._settings.update_from(s)
        self._settings.save()

    def _load_history(self):
        """Restore previous download records into the task table."""
        for record in self._history.get_all():
            task_id = record["task_id"]
            url = record["url"]
            title = record.get("title", "")
            status = record.get("status", "completed")
            # Add row — store URL so retry works; no active cancel callback
            self._task_table.add_task(task_id, title or url, cancel_cb=lambda _: None)
            self._task_table._urls[task_id] = url  # ensure URL is stored for retry
            self._task_table.update_status(task_id, status)
            if status == "completed":
                self._completed_count += 1
                pbar = self._task_table._table.cellWidget(
                    self._task_table._row_map.get(task_id, -1), 3
                )
                if pbar:
                    pbar.setValue(100)

    def _update_ffmpeg_status(self):
        ffmpeg_str = "ffmpeg: OK" if is_ffmpeg_available() else "ffmpeg: NOT FOUND"
        self.statusBar().showMessage(f"Ready  |  {ffmpeg_str}")

    def _update_status_bar(self):
        ffmpeg_str = "ffmpeg: OK" if is_ffmpeg_available() else "ffmpeg: NOT FOUND"
        self.statusBar().showMessage(
            f"{self._active_count} active  |  {self._completed_count} completed  |  {ffmpeg_str}"
        )

    # -- Slots ---------------------------------------------------------------

    @Slot()
    def _on_open_settings(self):
        """Open settings dialog. Apply changes only on OK."""
        if self._settings_dialog.exec():
            # User clicked OK — persist
            self._save_settings()

    @Slot()
    def _on_download(self):
        urls = self._url_input.get_urls()
        if not urls:
            QMessageBox.warning(self, "No URLs", "Please enter at least one URL.")
            return

        user_opts = self._settings_dialog.settings_panel.collect_opts()
        if "format" not in user_opts or not user_opts.get("format"):
            user_opts["format"] = get_default_format()
        ydl_opts = build_opts(user_opts)

        for url in urls:
            task_id = self._manager.add_task(url, ydl_opts)
            self._task_table.add_task(
                task_id, url, cancel_cb=self._manager.cancel_task
            )
            self._history.add(task_id, url)
            self._active_count += 1

        self._update_status_bar()

    @Slot()
    def _on_cancel_all(self):
        self._manager.cancel_all()

    @Slot(str, dict)
    def _on_progress(self, task_id: str, data: dict):
        self._task_table.update_progress(task_id, data)
        # Persist title from progress info_dict
        info = data.get("info_dict", {})
        title = info.get("title")
        if title:
            self._history.update_title(task_id, title)

    @Slot(str, str, str)
    def _on_status_changed(self, task_id: str, old_status: str, new_status: str):
        self._task_table.update_status(task_id, new_status)
        self._history.update_status(task_id, new_status)
        if new_status in ("completed", "failed", "canceled"):
            self._active_count = max(0, self._active_count - 1)
            if new_status == "completed":
                self._completed_count += 1
            self._update_status_bar()

    @Slot(str, str)
    def _on_error(self, task_id: str, error_msg: str):
        self._log_viewer.append(f"[ERROR] Task {task_id}: {error_msg}")

    @Slot()
    def _on_list_formats(self):
        url = self._url_input.get_first_url()
        if not url:
            QMessageBox.warning(self, "No URL", "Enter a URL first to list formats.")
            return
        self.statusBar().showMessage("Extracting format info…")
        self._manager.extract_info(
            url,
            on_result=self._bridge.on_info_result,
            on_error=self._bridge.on_info_error,
        )

    @Slot(str, dict)
    def _on_info_extracted(self, url: str, info: dict):
        self.statusBar().showMessage("Ready")
        dialog = FormatPreviewDialog(info, parent=self)
        if dialog.exec() and dialog.selected_format:
            self._settings_dialog.settings_panel.format_combo.setEditText(dialog.selected_format)

    @Slot(str, str)
    def _on_info_error(self, url: str, error_msg: str):
        self.statusBar().showMessage("Ready")
        QMessageBox.warning(self, "Format Extraction Failed", error_msg)

    @Slot(dict)
    def _on_preset_selected(self, preset: dict):
        self._settings_dialog.settings_panel.apply_preset(preset)

    @Slot()
    def _on_save_preset(self):
        opts = self._settings_dialog.settings_panel.collect_opts()
        self._preset_bar.save_preset_with_opts(opts)

    def _retry_url(self, old_task_id: str, url: str):
        # Remove old history record
        self._history.delete(old_task_id)
        # Start fresh download
        user_opts = self._settings_dialog.settings_panel.collect_opts()
        if "format" not in user_opts or not user_opts.get("format"):
            user_opts["format"] = get_default_format()
        ydl_opts = build_opts(user_opts)
        task_id = self._manager.add_task(url, ydl_opts)
        self._task_table.add_task(task_id, url, cancel_cb=self._manager.cancel_task)
        self._history.add(task_id, url)
        self._active_count += 1
        self._update_status_bar()

    def _toggle_theme(self):
        current = self._settings.get("theme", "light")
        new_theme = "dark" if current == "light" else "light"
        self._settings.set("theme", new_theme)
        apply_theme(QApplication.instance(), new_theme)
        self._theme_action.setText(
            "Switch to Light Mode" if new_theme == "dark" else "Switch to Dark Mode"
        )

    def _delete_task(self, task_id: str):
        """Delete a single task from history."""
        self._history.delete(task_id)

    def _clear_history(self):
        self._history.clear_all()
        # Clear table rows that aren't currently active
        # Simplest: just inform the user to restart
        QMessageBox.information(
            self, "History Cleared",
            "Download history has been cleared.\nRestart the app to refresh the task list."
        )

    def _show_about(self):
        from core.ffmpeg_utils import find_ffmpeg
        ffmpeg_path = find_ffmpeg() or "Not found"
        QMessageBox.about(
            self, "About yt-dlp GUI",
            f"yt-dlp GUI v3.1\n\nA GUI wrapper for yt-dlp.\nFFmpeg: {ffmpeg_path}",
        )

    def closeEvent(self, event):
        self._save_settings()
        # Mark any still-running tasks as interrupted so they show correctly on restart
        for record in self._history.get_all():
            if record["status"] == "running":
                self._history.update_status(record["task_id"], "interrupted")
        self._manager.shutdown(wait=False)
        super().closeEvent(event)
