"""Horizontal bar of download preset buttons."""

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QHBoxLayout,
    QInputDialog,
    QPushButton,
    QWidget,
)

from configs.presets import PresetManager


class PresetBar(QWidget):
    """A horizontal row of preset buttons. Emits preset_selected with the preset dict."""

    preset_selected = Signal(dict)  # preset options dict

    def __init__(self, parent=None):
        super().__init__(parent)
        self._manager = PresetManager()
        self._buttons: dict[str, QPushButton] = {}
        self._active_name: str = ""

        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(0, 4, 0, 4)
        self._layout.setSpacing(6)

        self._rebuild_buttons()

        # Save preset button
        self._btn_save = QPushButton("+ Save Preset")
        self._btn_save.setProperty("class", "preset-btn")
        self._btn_save.clicked.connect(self._on_save_preset)
        self._layout.addWidget(self._btn_save)

        self._layout.addStretch()

    def _rebuild_buttons(self):
        # Clear existing
        for btn in self._buttons.values():
            self._layout.removeWidget(btn)
            btn.deleteLater()
        self._buttons.clear()

        for name in self._manager.get_all():
            btn = QPushButton(name)
            btn.setProperty("preset", "true")
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, n=name: self._on_preset_clicked(n))
            self._layout.insertWidget(self._layout.count() - 1, btn)  # before stretch
            self._buttons[name] = btn

    def _on_preset_clicked(self, name: str):
        preset = self._manager.get(name)
        if preset is None:
            return

        # Update active state
        self._active_name = name
        for n, btn in self._buttons.items():
            btn.setProperty("active", "true" if n == name else "false")
            btn.style().unpolish(btn)
            btn.style().polish(btn)

        self.preset_selected.emit(preset)

    def deactivate(self):
        """Clear the active preset highlight."""
        self._active_name = ""
        for btn in self._buttons.values():
            btn.setProperty("active", "false")
            btn.setChecked(False)
            btn.style().unpolish(btn)
            btn.style().polish(btn)

    def _on_save_preset(self):
        """Prompt user for a name and save current config as a user preset."""
        # This will be connected by MainWindow to get current settings
        self._save_requested = True

    def save_preset_with_opts(self, opts: dict):
        """Called by MainWindow after collecting current settings."""
        name, ok = QInputDialog.getText(self, "Save Preset", "Preset name:")
        if ok and name.strip():
            self._manager.save_user_preset(name.strip(), opts)
            self._rebuild_buttons()

    @property
    def active_preset_name(self) -> str:
        return self._active_name
