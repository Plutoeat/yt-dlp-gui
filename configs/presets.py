"""Built-in and user-defined download presets."""

import json
import os
from typing import Any

_ROOT = os.path.normpath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_USER_PRESETS_FILE = os.path.join(_ROOT, "configs", "user_presets.json")

BUILTIN_PRESETS: dict[str, dict[str, Any]] = {
    "Best MP4": {
        "format": "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4] / bv*+ba/b",
        "merge_output_format": "mp4",
        "embed_metadata": True,
        "embed_chapters": True,
    },
    "720p": {
        "format": "bv*[height<=720]+ba/b[height<=720]",
        "merge_output_format": "mp4",
    },
    "1080p": {
        "format": "bv*[height<=1080]+ba/b[height<=1080]",
        "merge_output_format": "mp4",
    },
    "Audio MP3": {
        "extract_audio": True,
        "audio_format": "mp3",
        "audio_quality": 0,
    },
    "Audio FLAC": {
        "extract_audio": True,
        "audio_format": "flac",
    },
    "With Subtitles": {
        "format": "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4] / bv*+ba/b",
        "writesubtitles": True,
        "write_auto_subs": True,
        "subtitleslangs": "en,zh-Hans",
        "embedsubtitles": True,
        "convert_subs": "srt",
        "merge_output_format": "mkv",
    },
}


class PresetManager:
    """Manages built-in and user-defined presets."""

    def __init__(self, path: str = _USER_PRESETS_FILE):
        self._path = path
        self._user_presets: dict[str, dict[str, Any]] = {}
        self._load()

    def _load(self):
        if os.path.isfile(self._path):
            try:
                with open(self._path, "r", encoding="utf-8") as f:
                    self._user_presets = json.load(f)
            except (json.JSONDecodeError, OSError):
                self._user_presets = {}

    def _save(self):
        os.makedirs(os.path.dirname(self._path), exist_ok=True)
        with open(self._path, "w", encoding="utf-8") as f:
            json.dump(self._user_presets, f, indent=2, ensure_ascii=False)

    def get_all(self) -> dict[str, dict[str, Any]]:
        """Return all presets (built-in + user), user presets override built-in."""
        merged = dict(BUILTIN_PRESETS)
        merged.update(self._user_presets)
        return merged

    def get_builtin_names(self) -> list[str]:
        return list(BUILTIN_PRESETS.keys())

    def get_user_names(self) -> list[str]:
        return list(self._user_presets.keys())

    def get(self, name: str) -> dict[str, Any] | None:
        if name in self._user_presets:
            return self._user_presets[name]
        return BUILTIN_PRESETS.get(name)

    def save_user_preset(self, name: str, opts: dict[str, Any]):
        self._user_presets[name] = opts
        self._save()

    def delete_user_preset(self, name: str) -> bool:
        if name in self._user_presets:
            del self._user_presets[name]
            self._save()
            return True
        return False
