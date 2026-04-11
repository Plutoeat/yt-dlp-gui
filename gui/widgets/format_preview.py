"""Format preview dialog – shows available video/audio streams."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QDialog,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
)


def _fmt_size(size_bytes) -> str:
    if not size_bytes:
        return ""
    if size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.0f} KB"
    if size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
    return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"


_COLUMNS = ["ID", "Ext", "Resolution", "FPS", "VCodec", "ACodec", "Size", "Bitrate", "Note"]


class FormatPreviewDialog(QDialog):
    """Shows available formats for a video URL."""

    def __init__(self, info_dict: dict, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Available Formats")
        self.resize(800, 500)
        self._selected_format: str = ""

        layout = QVBoxLayout(self)

        # Title
        title = info_dict.get("title", "Unknown")
        duration = info_dict.get("duration_string", "")
        title_label = QLabel(f"<b>{title}</b>  ({duration})" if duration else f"<b>{title}</b>")
        title_label.setWordWrap(True)
        layout.addWidget(title_label)

        # Format table
        self._table = QTableWidget(0, len(_COLUMNS))
        self._table.setHorizontalHeaderLabels(_COLUMNS)
        self._table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self._table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self._table.setSelectionMode(QAbstractItemView.SingleSelection)
        self._table.setAlternatingRowColors(True)
        self._table.verticalHeader().setVisible(False)
        self._table.horizontalHeader().setSectionResizeMode(_COLUMNS.index("Note"), QHeaderView.Stretch)
        layout.addWidget(self._table, stretch=1)

        # Populate
        formats = info_dict.get("formats", [])
        self._populate(formats)

        # Buttons
        btn_layout = QHBoxLayout()
        self._btn_use = QPushButton("Use Selected Format")
        self._btn_use.setEnabled(False)
        self._btn_use.clicked.connect(self._on_use)
        btn_layout.addStretch()
        btn_layout.addWidget(self._btn_use)
        btn_layout.addWidget(QPushButton("Close", clicked=self.reject))
        layout.addLayout(btn_layout)

        self._table.selectionModel().selectionChanged.connect(self._on_selection)

    def _populate(self, formats: list[dict]):
        for fmt in formats:
            row = self._table.rowCount()
            self._table.insertRow(row)

            fid = fmt.get("format_id", "")
            ext = fmt.get("ext", "")
            w = fmt.get("width")
            h = fmt.get("height")
            res = f"{w}x{h}" if w and h else fmt.get("resolution", "audio only")
            fps = str(fmt.get("fps", "")) if fmt.get("fps") else ""
            vcodec = fmt.get("vcodec", "none")
            if vcodec == "none":
                vcodec = ""
            acodec = fmt.get("acodec", "none")
            if acodec == "none":
                acodec = ""
            size = _fmt_size(fmt.get("filesize") or fmt.get("filesize_approx"))
            tbr = fmt.get("tbr")
            bitrate = f"{tbr:.0f}k" if tbr else ""
            note = fmt.get("format_note", "")

            for col, val in enumerate([fid, ext, res, fps, vcodec, acodec, size, bitrate, note]):
                item = QTableWidgetItem(str(val))
                item.setData(Qt.UserRole, fid)
                self._table.setItem(row, col, item)

    def _on_selection(self):
        rows = self._table.selectionModel().selectedRows()
        self._btn_use.setEnabled(bool(rows))

    def _on_use(self):
        rows = self._table.selectionModel().selectedRows()
        if rows:
            fid = self._table.item(rows[0].row(), 0).text()
            self._selected_format = fid
            self.accept()

    @property
    def selected_format(self) -> str:
        return self._selected_format
