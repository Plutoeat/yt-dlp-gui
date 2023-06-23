#!/usr/bin/python3
# _*_ coding: utf-8 _*_
# Software: yt-dlp-gui
# @FileName: main.py
# @Author: Gaius Pluto
# @Date: 2023/6/22
from core.download import run

URLS = ['https://www.youtube.com/watch?v=BaW_jenozKc']


def main():
    run(URLS)


if __name__ == '__main__':
    main()
