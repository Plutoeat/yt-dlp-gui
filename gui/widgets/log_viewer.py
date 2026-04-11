"""Collapsible log viewer widget."""

import logging

from PySide6.QtWidgets import QGroupBox, QPlainTextEdit, QVBoxLayout


class QTextEditHandler(logging.Handler):
    """Logging handler that appends to a QPlainTextEdit."""

    def __init__(self, text_edit: QPlainTextEdit):
        super().__init__()
        self._text_edit = text_edit

    def emit(self, record):
        msg = self.format(record)
        self._text_edit.appendPlainText(msg)


class LogViewerWidget(QGroupBox):
    def __init__(self, parent=None):
        super().__init__("Log", parent)
        self.setCheckable(True)
        self.setChecked(True)
        layout = QVBoxLayout(self)

        self._text_edit = QPlainTextEdit()
        self._text_edit.setObjectName("log_viewer")
        self._text_edit.setReadOnly(True)
        self._text_edit.setMaximumHeight(150)
        layout.addWidget(self._text_edit)

        self.toggled.connect(self._on_toggle)

        # Install logging handler
        self._handler = QTextEditHandler(self._text_edit)
        self._handler.setFormatter(
            logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        )
        logging.getLogger().addHandler(self._handler)

    def _on_toggle(self, checked: bool):
        self._text_edit.setVisible(checked)

    def append(self, text: str):
        self._text_edit.appendPlainText(text)
