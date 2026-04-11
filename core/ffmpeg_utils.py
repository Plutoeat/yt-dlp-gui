"""FFmpeg detection and utilities."""

import shutil
from functools import lru_cache


@lru_cache(maxsize=1)
def find_ffmpeg() -> str | None:
    """Return the path to ffmpeg if found, else None."""
    return shutil.which("ffmpeg")


@lru_cache(maxsize=1)
def find_ffprobe() -> str | None:
    """Return the path to ffprobe if found, else None."""
    return shutil.which("ffprobe")


def is_ffmpeg_available() -> bool:
    return find_ffmpeg() is not None


def get_default_format() -> str:
    """Return the best default format string based on ffmpeg availability."""
    if is_ffmpeg_available():
        return "bv*+ba/b"
    return "b"
