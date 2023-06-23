#!/usr/bin/python3
# _*_ coding: utf-8 _*_
# Software: yt-dlp-gui
# @FileName: config.py
# @Author: Gaius Pluto
# @Date: 2023/6/22
from configs.default_yt_dlp_conf import CONFIG_LIST


class ConfigBase:
    def __init__(self, conf_list):
        self.config_list = conf_list

    def assemble_config(self) -> dict:
        ydl_opts = {}
        for i in self.config_list:
            ydl_opts.update(i)
        return ydl_opts


Config = ConfigBase(CONFIG_LIST)
