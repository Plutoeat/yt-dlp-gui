"""Extract video info without downloading – powers the format preview feature."""

from typing import Any

import yt_dlp


def extract_info(url: str, ydl_opts: dict[str, Any] | None = None) -> dict[str, Any]:
    """Extract video metadata and available formats.

    Returns the full info_dict from yt-dlp, which includes:
    - title, duration, thumbnail, description
    - formats: list of available streams with resolution, codec, filesize, etc.
    - subtitles / automatic_captions
    """
    opts = dict(ydl_opts or {})
    opts.update({
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
    })
    # Remove hooks that don't apply to info extraction
    opts.pop("progress_hooks", None)
    opts.pop("postprocessor_hooks", None)
    opts.pop("postprocessors", None)

    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=False)
    return info or {}
