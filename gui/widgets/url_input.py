"""URL input widget – multi-line text area with paste/import/format buttons."""

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QGroupBox,
    QHBoxLayout,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
)


class UrlInputWidget(QGroupBox):

    format_requested = Signal()  # emitted when user wants to preview formats

    def __init__(self, parent=None):
        super().__init__("URLs", parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 14, 10, 10)

        self._text_edit = QPlainTextEdit()
        self._text_edit.setPlaceholderText(
            "Enter video URLs here, one per line…"
        )
        self._text_edit.setMaximumHeight(90)
        layout.addWidget(self._text_edit)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(8)

        self._btn_paste = QPushButton("Paste")
        self._btn_paste.clicked.connect(self._paste_clipboard)

        self._btn_import = QPushButton("Import Batch File")
        self._btn_import.clicked.connect(self._import_batch)

        self._btn_formats = QPushButton("List Formats")
        self._btn_formats.setToolTip("Preview available formats for the first URL")
        self._btn_formats.clicked.connect(self.format_requested.emit)

        self._btn_clear = QPushButton("Clear")
        self._btn_clear.clicked.connect(self._text_edit.clear)

        btn_layout.addWidget(self._btn_paste)
        btn_layout.addWidget(self._btn_import)
        btn_layout.addStretch()
        btn_layout.addWidget(self._btn_formats)
        btn_layout.addWidget(self._btn_clear)
        layout.addLayout(btn_layout)

    def get_urls(self) -> list[str]:
        text = self._text_edit.toPlainText().strip()
        if not text:
            return []
        urls = []
        seen = set()
        for line in text.splitlines():
            line = line.strip()
            if line and not line.startswith("#") and line not in seen:
                urls.append(line)
                seen.add(line)
        return urls

    def get_first_url(self) -> str:
        urls = self.get_urls()
        return urls[0] if urls else ""

    def clear(self):
        self._text_edit.clear()

    def _paste_clipboard(self):
        text = QApplication.clipboard().text()
        if text:
            current = self._text_edit.toPlainText()
            if current and not current.endswith("\n"):
                current += "\n"
            self._text_edit.setPlainText(current + text)

    def _import_batch(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Import Batch File", "", "Text Files (*.txt);;All Files (*)"
        )
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                lines = f.read()
            current = self._text_edit.toPlainText()
            if current and not current.endswith("\n"):
                current += "\n"
            self._text_edit.setPlainText(current + lines)
        except OSError as e:
            QMessageBox.warning(self, "Error", f"Could not read file:\n{e}")
