#!/usr/bin/python3
# _*_ coding: utf-8 _*_
# Software: yt-dlp-gui
# @FileName: download
# @Author: Gaius Pluto
# @Date: 2023/6/22

import yt_dlp

from configs.config import Config


def run(url):
    ydl_opts = Config.assemble_config()

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(url)
