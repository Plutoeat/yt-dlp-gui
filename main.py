#!/usr/bin/env python3
"""yt-dlp-gui – GUI for downloading video based on yt-dlp and PySide6."""

import sys

from PySide6.QtWidgets import QApplication

from configs.app_settings import AppSettings
from gui.main_window import MainWindow
from gui.theme_manager import apply_theme


def main():
    app = QApplication(sys.argv)

    # Load saved theme preference
    settings = AppSettings()
    theme = settings.get("theme", "light")
    apply_theme(app, theme)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
