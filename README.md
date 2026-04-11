# yt-dlp-gui

A clean, modern GUI for [yt-dlp](https://github.com/yt-dlp/yt-dlp), built with PySide6.

Paste a URL, click download — that's it. All advanced yt-dlp options are available when you need them.

> **This program is designed to simplify the use of yt-dlp. For more advanced operations, please refer to the [yt-dlp documentation](https://github.com/yt-dlp/yt-dlp).**

![Screenshot](assets/Screenshot%202026-04-12%20at%2000.11.23.png)

## Features

- **Simple by default** — paste URL, click Start Download
- **Preset system** — one-click presets: Best MP4, 720p, 1080p, Audio MP3, Audio FLAC, With Subtitles
- **Format preview** — list all available formats before downloading
- **Smart defaults** — auto-detects ffmpeg, auto-selects best format with video+audio merging
- **Resume downloads** — interrupted downloads resume from where they left off
- **Download history** — records persist across app restarts, with retry support
- **Dark / Light theme** — switch from the View menu
- **Full yt-dlp power** — 50+ configurable options organized in a clean settings dialog:
  - Format & Quality (format string, sort, merge output, audio format/quality, remux, recode)
  - Subtitles (download, auto-generated, language, format, convert, embed)
  - Post-Processing (metadata, chapters, thumbnail embed, SponsorBlock, split chapters)
  - Authentication (browser cookies, cookie file, username/password, netrc)
  - Download Settings (path, filename template, proxy, rate limit, concurrency, archive)
  - Video Selection (playlist items, file size filter, date range, match filter)

## Requirements

- Python >= 3.13
- [ffmpeg](https://ffmpeg.org/) (recommended, required for merging video+audio, embedding subtitles, and post-processing)

## Installation

```shell
# Clone the repository
git clone https://github.com/Plutoeat/yt-dlp-gui.git
cd yt-dlp-gui

# Install dependencies with uv
uv sync

# Run
uv run python main.py
```

Or with pip:

```shell
pip install pyside6 yt-dlp pyyaml
python main.py
```

## Usage

1. Paste one or more video URLs (one per line) or use **Import Batch File**
2. Optionally select a **preset** or click **Settings...** to configure options
3. Click **Start Download**
4. Monitor progress in the task table; right-click for options (retry, delete, copy URL)

## Project Structure

```
yt-dlp-gui/
├── main.py                  # App entry point
├── core/
│   ├── task.py              # DownloadTask: 5-state machine, progress hooks
│   ├── manager.py           # DownloadManager: thread pool, task queue
│   ├── info_extractor.py    # Format preview (extract_info without download)
│   ├── ffmpeg_utils.py      # FFmpeg auto-detection
│   └── history.py           # Download history persistence
├── configs/
│   ├── ydl_opts.py          # Build yt-dlp options with postprocessor assembly
│   ├── app_settings.py      # App settings persistence (JSON)
│   ├── presets.py            # Built-in + user-defined presets
│   └── yt-dlp.yml           # YAML defaults
├── gui/
│   ├── main_window.py       # Main window
│   ├── bridge.py            # Pure Python callback -> Qt Signal adapter
│   ├── theme_manager.py     # Light/dark theme switching
│   ├── styles/              # QSS stylesheets
│   └── widgets/             # UI components
│       ├── url_input.py
│       ├── preset_bar.py
│       ├── settings_panel.py
│       ├── settings_dialog.py
│       ├── format_preview.py
│       ├── task_table.py
│       ├── log_viewer.py
│       └── collapsible_section.py
└── pyproject.toml
```

## Architecture

```
GUI Layer (PySide6)
  ↓ Qt Signals
Bridge Layer (callback → Signal adapter)
  ↓ Pure Python callbacks
Core Layer (DownloadManager, DownloadTask)
  ↓
yt-dlp API
```

The core layer has **zero Qt dependency** and can be tested independently.

## Thanks

- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [PySide6](https://doc.qt.io/qtforpython-6/)
