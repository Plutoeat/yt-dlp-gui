#!/usr/bin/python3
# _*_ coding: utf-8 _*_
# Software: yt-dlp-gui
# @FileName: mylogger
# @Author: Gaius Pluto
# @Date: 2023/6/22
import logging.config
import os.path

import yaml

config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'configs/log_config.yml')
config_path = os.path.normpath(config_path)

with open(config_path, 'r') as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)

logger = logging.getLogger("default")
