#!/usr/bin/python3
# _*_ coding: utf-8 _*_
# Software: yt-dlp-gui
# @FileName: default_yt_dlp_conf.py
# @Author: Gaius Pluto
# @Date: 2023/6/20
import os

import yaml

pwd = os.path.normpath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

NETWORK_OPTIONS = {
    # more information: https://github.com/yt-dlp/yt-dlp#network-options
    "proxy": ""
}
VIDEO_SELECTION = {
    # more information: https://github.com/yt-dlp/yt-dlp#video-selection
    "playlist_items": "",
    "min_filesize": "",
    "max_filesize": "",
    "noplaylist": False,
}
DOWNLOAD_OPTIONS = {
    # more information: https://github.com/yt-dlp/yt-dlp#download-options
    "ratelimit": ""
}
FILESYSTEM_OPTIONS = {
    # more information: https://github.com/yt-dlp/yt-dlp#filesystem-options
    "paths": {"home": os.path.join(pwd, "video")},
    "outtmpl": "%(title)s.%(ext)s",
    "writedescription": False,
    "writeinfojson": False,
    "getcomments": False
}
THUMBNAIL_OPTIONS = {
    # more information: https://github.com/yt-dlp/yt-dlp#thumbnail-options
    "writethumbnail": False
}
VIDEO_FORMAT_OPTIONS = {
    # bv+ba mast download ffmpeg and ffprobe
    "format": "b"
    # "format": "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4] / bv*+ba/b"
}
SUBTITLE_OPTIONS = {
    "writesubtitles": False,
    "subtitleslangs": ['all', '-live_chat']
}
POST_PROCESSING_OPTIONS = {
    # mast ffmpeg and ffprobe, pls set by yourself
}


def rmnullandfalse(x: dict):
    for (key, value) in list(x.items()):
        if isinstance(value, bool):
            if not value:
                del x[key]
        elif isinstance(value, str):
            if value.strip(' \t\n\r') == '':
                del x[key]
        elif isinstance(value, dict) or isinstance(value, list):
            if len(value) == 0:
                del x[key]
        elif isinstance(value, int) or isinstance(value, float):
            if value < 0:
                raise Exception(f"error config in {key}")
        else:
            raise Exception(f"error config in {key}!!!")
    return x


def getfinalconf():
    with open(os.path.join(pwd, 'configs/yt-dlp.yml'), 'r', encoding='utf-8') as f:
        default_conf = yaml.safe_load(f.read())['default']
    raw_list = [default_conf, NETWORK_OPTIONS, VIDEO_SELECTION, DOWNLOAD_OPTIONS, FILESYSTEM_OPTIONS, THUMBNAIL_OPTIONS,
                VIDEO_FORMAT_OPTIONS, SUBTITLE_OPTIONS, POST_PROCESSING_OPTIONS]
    return list(map(rmnullandfalse, raw_list))


CONFIG_LIST = getfinalconf()
