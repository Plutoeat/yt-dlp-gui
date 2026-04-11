"""Reusable collapsible section widget for progressive disclosure UI."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QSizePolicy,
    QToolButton,
    QVBoxLayout,
    QWidget,
)


class CollapsibleSection(QWidget):
    """A section with a clickable header that expands/collapses its content."""

    def __init__(self, title: str, parent=None, expanded: bool = False):
        super().__init__(parent)

        self._toggle_btn = QToolButton()
        self._toggle_btn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self._toggle_btn.setText(f"  {title}")
        self._toggle_btn.setCheckable(True)
        self._toggle_btn.setChecked(expanded)
        self._toggle_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self._toggle_btn.setArrowType(Qt.DownArrow if expanded else Qt.RightArrow)
        self._toggle_btn.toggled.connect(self._on_toggle)

        self._content = QWidget()
        self._content_layout = QVBoxLayout(self._content)
        self._content_layout.setContentsMargins(12, 8, 12, 12)
        self._content_layout.setSpacing(6)
        self._content.setVisible(expanded)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 2, 0, 2)
        layout.setSpacing(4)
        layout.addWidget(self._toggle_btn)
        layout.addWidget(self._content)

    @property
    def content_layout(self) -> QVBoxLayout:
        return self._content_layout

    def add_widget(self, widget: QWidget):
        self._content_layout.addWidget(widget)

    def add_layout(self, layout):
        self._content_layout.addLayout(layout)

    def is_expanded(self) -> bool:
        return self._toggle_btn.isChecked()

    def set_expanded(self, expanded: bool):
        self._toggle_btn.setChecked(expanded)

    def _on_toggle(self, checked: bool):
        self._toggle_btn.setArrowType(Qt.DownArrow if checked else Qt.RightArrow)
        self._content.setVisible(checked)
