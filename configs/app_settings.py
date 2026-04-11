"""GUI application settings persistence (window state, language, last-used config)."""

import json
import os
from typing import Any

_ROOT = os.path.normpath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_SETTINGS_FILE = os.path.join(_ROOT, "configs", "app_settings.json")

_DEFAULTS: dict[str, Any] = {
    # App
    "language": "en",
    "theme": "light",
    "window_width": 960,
    "window_height": 720,
    "active_preset": "",

    # Download settings
    "download_path": os.path.join(_ROOT, "video"),
    "outtmpl": "",
    "proxy": "",
    "geo_verification_proxy": "",
    "ratelimit": "",
    "max_workers": 3,
    "concurrent_fragment_downloads": 1,
    "external_downloader": "",
    "sleep_interval": 0,
    "download_archive": "",

    # Format & quality
    "format": "",  # empty = auto-detect (ffmpeg → bv*+ba/b, else b)
    "format_sort": "",
    "merge_output_format": "",
    "audio_format": "mp3",
    "audio_quality": 5,

    # Video selection
    "noplaylist": False,
    "playlist_items": "",
    "min_filesize": "",
    "max_filesize": "",
    "date_range_start": "",
    "date_range_end": "",
    "match_filter": "",
    "max_downloads": 0,

    # Subtitles
    "writesubtitles": False,
    "write_auto_subs": False,
    "subtitleslangs": "",
    "sub_format": "best",
    "convert_subs": "",
    "embed_subs": False,

    # Metadata & thumbnails
    "writethumbnail": False,
    "embedthumbnail": False,
    "convert_thumbnails": "",
    "writedescription": False,
    "writeinfojson": False,
    "getcomments": False,

    # Post-processing
    "extract_audio": False,
    "embed_metadata": True,
    "embed_chapters": True,
    "remux_video": "",
    "recode_video": "",
    "sponsorblock_mark": "",
    "sponsorblock_remove": "",
    "split_chapters": False,
    "keep_video": False,
    "ffmpeg_location": "",
    "skip_download": False,

    # Authentication
    "cookiesfrombrowser": "None",
    "cookiefile": "",
    "username": "",
    "password": "",
    "netrc": False,
}


class AppSettings:
    """Read / write application-level settings to a JSON file."""

    def __init__(self, path: str = _SETTINGS_FILE):
        self._path = path
        self._data: dict[str, Any] = dict(_DEFAULTS)
        self.load()

    def load(self):
        if os.path.isfile(self._path):
            try:
                with open(self._path, "r", encoding="utf-8") as f:
                    stored = json.load(f)
                self._data.update(stored)
            except (json.JSONDecodeError, OSError):
                pass

    def save(self):
        os.makedirs(os.path.dirname(self._path), exist_ok=True)
        with open(self._path, "w", encoding="utf-8") as f:
            json.dump(self._data, f, indent=2, ensure_ascii=False)

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def set(self, key: str, value: Any):
        self._data[key] = value

    def to_dict(self) -> dict[str, Any]:
        return dict(self._data)

    def update_from(self, opts: dict[str, Any]):
        """Bulk update settings from a dict (e.g., from settings panel)."""
        for key, value in opts.items():
            if key in _DEFAULTS:
                self._data[key] = value
