"""Theme management – load and switch between light/dark QSS themes."""

import os

from PySide6.QtWidgets import QApplication

_STYLES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "styles")

_THEMES = {
    "light": os.path.join(_STYLES_DIR, "theme.qss"),
    "dark": os.path.join(_STYLES_DIR, "dark_theme.qss"),
}


def apply_theme(app: QApplication, theme_name: str):
    """Apply a named theme to the application."""
    path = _THEMES.get(theme_name)
    if path and os.path.isfile(path):
        with open(path, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())


def available_themes() -> list[str]:
    return list(_THEMES.keys())
