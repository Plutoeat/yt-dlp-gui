"""Build yt-dlp option dicts from user input with YAML defaults as fallback."""

import os
from typing import Any

import yaml

_ROOT = os.path.normpath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_YDL_YAML = os.path.join(_ROOT, "configs", "yt-dlp.yml")


def _load_yaml_defaults() -> dict[str, Any]:
    """Load base defaults from yt-dlp.yml."""
    try:
        with open(_YDL_YAML, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f.read())
        return data.get("default", {}) if data else {}
    except FileNotFoundError:
        return {}


def build_opts(user_opts: dict[str, Any] | None = None) -> dict[str, Any]:
    """Merge YAML defaults with user-supplied options.

    Pipeline: merge → postprocessors → special fields → clean.
    """
    defaults = _load_yaml_defaults()
    # Always enable resume / partial download support
    defaults.setdefault("continuedl", True)
    merged = {**defaults, **(user_opts or {})}
    merged = _build_postprocessors(merged)
    merged = _convert_special_fields(merged)
    return _clean(merged)


def _build_postprocessors(opts: dict[str, Any]) -> dict[str, Any]:
    """Assemble the postprocessors list from high-level flags."""
    pps: list[dict] = list(opts.get("postprocessors", []))

    # Extract audio
    if opts.pop("extract_audio", False):
        audio_fmt = opts.pop("audio_format", "mp3")
        audio_quality = opts.pop("audio_quality", 5)
        pps.append({
            "key": "FFmpegExtractAudio",
            "preferredcodec": audio_fmt,
            "preferredquality": str(audio_quality),
        })
    else:
        opts.pop("audio_format", None)
        opts.pop("audio_quality", None)

    # Embed thumbnail
    if opts.pop("embedthumbnail", False):
        if not opts.get("writethumbnail"):
            opts["writethumbnail"] = True
        pps.append({"key": "EmbedThumbnail"})

    # Convert thumbnails
    convert_thumb = opts.pop("convert_thumbnails", "")
    if convert_thumb:
        pps.append({
            "key": "FFmpegThumbnailsConvertor",
            "format": convert_thumb,
        })

    # Embed subtitles
    if opts.get("embedsubtitles"):
        pps.append({"key": "FFmpegEmbedSubtitle"})

    # Convert subtitles
    convert_subs = opts.pop("convert_subs", "")
    if convert_subs:
        pps.append({
            "key": "FFmpegSubtitlesConvertor",
            "format": convert_subs,
        })

    # Embed metadata — use yt-dlp's native option, not a manual postprocessor
    if opts.pop("embed_metadata", False):
        opts["addmetadata"] = True

    # Embed chapters — use yt-dlp's native option
    if opts.pop("embed_chapters", False):
        opts["addchapters"] = True

    # Remux video (change container without re-encoding)
    remux = opts.pop("remux_video", "")
    if remux:
        pps.append({
            "key": "FFmpegVideoRemuxer",
            "preferedformat": remux,
        })

    # Recode video (re-encode)
    recode = opts.pop("recode_video", "")
    if recode:
        pps.append({
            "key": "FFmpegVideoConvertor",
            "preferedformat": recode,
        })

    # SponsorBlock
    sb_mark = opts.pop("sponsorblock_mark", "")
    sb_remove = opts.pop("sponsorblock_remove", "")
    if sb_mark or sb_remove:
        sb_opts: dict[str, Any] = {"key": "SponsorBlock"}
        if sb_mark:
            sb_opts["categories"] = [c.strip() for c in sb_mark.split(",")]
            sb_opts["action"] = "mark"
        if sb_remove:
            sb_opts["categories"] = [c.strip() for c in sb_remove.split(",")]
            sb_opts["action"] = "remove"
        pps.append(sb_opts)

    # Split chapters
    if opts.pop("split_chapters", False):
        pps.append({"key": "FFmpegSplitChapters"})

    if pps:
        opts["postprocessors"] = pps

    return opts


def _convert_special_fields(opts: dict[str, Any]) -> dict[str, Any]:
    """Convert GUI-friendly values to yt-dlp expected types."""
    # cookiesfrombrowser: string → tuple
    browser = opts.pop("cookiesfrombrowser", None)
    if browser and browser != "None":
        opts["cookiesfrombrowser"] = (browser,)

    # cookiefile: rename to cookies
    cookiefile = opts.pop("cookiefile", "")
    if cookiefile:
        opts["cookiefile"] = cookiefile

    # subtitleslangs: ensure list
    langs = opts.get("subtitleslangs")
    if isinstance(langs, str):
        opts["subtitleslangs"] = [s.strip() for s in langs.split(",") if s.strip()]

    # format_sort: string → list
    fmt_sort = opts.get("format_sort")
    if isinstance(fmt_sort, str) and fmt_sort.strip():
        opts["format_sort"] = [s.strip() for s in fmt_sort.split(",") if s.strip()]
    elif not fmt_sort:
        opts.pop("format_sort", None)

    # write_auto_subs → writeautomaticsub
    if opts.pop("write_auto_subs", False):
        opts["writeautomaticsub"] = True

    # sub_format → subtitlesformat
    sub_fmt = opts.pop("sub_format", "")
    if sub_fmt and sub_fmt != "best":
        opts["subtitlesformat"] = sub_fmt

    # merge_output_format
    merge_fmt = opts.get("merge_output_format")
    if not merge_fmt:
        opts.pop("merge_output_format", None)

    # ffmpeg_location
    ffmpeg_loc = opts.pop("ffmpeg_location", "")
    if ffmpeg_loc:
        opts["ffmpeg_location"] = ffmpeg_loc

    # download_archive
    archive = opts.pop("download_archive", "")
    if archive:
        opts["download_archive"] = archive

    # date range
    date_start = opts.pop("date_range_start", "")
    date_end = opts.pop("date_range_end", "")
    if date_start:
        opts["dateafter"] = date_start
    if date_end:
        opts["datebefore"] = date_end

    # match_filter
    match_filter = opts.pop("match_filter", "")
    if match_filter:
        opts["match_filter"] = [match_filter]

    # max_downloads — remove unless explicitly set to a meaningful value (>= 2)
    # value of 0 = no limit, 1 = breaks thumbnail/subtitle downloads
    max_dl = opts.pop("max_downloads", 0)
    if isinstance(max_dl, int) and max_dl >= 2:
        opts["max_downloads"] = max_dl

    # sleep_interval
    sleep = opts.pop("sleep_interval", 0)
    if sleep and sleep > 0:
        opts["sleep_interval"] = sleep

    # external_downloader
    ext_dl = opts.pop("external_downloader", "")
    if ext_dl and ext_dl != "none":
        opts["external_downloader"] = {"default": ext_dl}

    # keep_video
    if opts.get("keep_video"):
        opts["keepvideo"] = opts.pop("keep_video")
    else:
        opts.pop("keep_video", None)

    # netrc
    if opts.pop("netrc", False):
        opts["usenetrc"] = True

    # Clean up GUI-only keys that yt-dlp doesn't understand
    for gui_key in [
        "theme", "active_preset", "window_width", "window_height",
        "language", "download_path", "embed_subs",
    ]:
        opts.pop(gui_key, None)

    return opts


def _clean(opts: dict[str, Any]) -> dict[str, Any]:
    """Remove None and empty-string values. Preserve False booleans."""
    cleaned = {}
    for key, value in opts.items():
        if value is None:
            continue
        if isinstance(value, str) and not value.strip():
            continue
        if isinstance(value, (dict, list)) and len(value) == 0:
            continue
        cleaned[key] = value
    return cleaned
