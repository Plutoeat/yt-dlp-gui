"""Settings dialog – standalone window for all download configuration."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QScrollArea,
    QVBoxLayout,
)

from gui.widgets.settings_panel import SettingsPanel


class SettingsDialog(QDialog):
    """A standalone settings window so the main window stays clean."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Download Settings")
        self.resize(660, 600)
        self.setMinimumWidth(560)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 12)
        layout.setSpacing(12)

        # Scrollable settings panel
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.settings_panel = SettingsPanel()
        scroll.setWidget(self.settings_panel)
        layout.addWidget(scroll, stretch=1)

        # OK / Cancel buttons
        btn_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        btn_box.accepted.connect(self.accept)
        btn_box.rejected.connect(self.reject)
        layout.addWidget(btn_box)
