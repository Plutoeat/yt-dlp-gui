# yt-dlp-gui
GUI for downloading video based on yt-dlp and pyside6

------

**开发此程序仅为简化yt-dlp的使用，更多细致的操作请查看[yt-dlp官网](https://github.com/yt-dlp/yt-dlp)**

## 使用 | USAGE

### 直接使用 | Use directly

**Real or virtual python environment**

```shell
pip install -r reqirements.txt
```

**In `yt-dlp-gui`**

```shell
python main.py
```

### 使用可执行文件 | Use executable(Windows)

如果你不想太麻烦，你可以通过[bilibil](https://space.bilibili.com/686725252)i或者与bilibili同名的微信公众号联系我（最好）获取(.exe)文件，但是我可能长时间不看消息，导致你等待较长时间

>If you don’t want to be too troublesome, you can contact me to get the (.exe) file through [bilibili](https://space.bilibili.com/686725252) or the WeChat public account (best) with the same name as bilibili, but I may not read the message for a long time, causing you to wait for a long time

## 问题 | Issue

单选框无论是选择直接还是更多选项后点击下载按钮都会延迟几秒，请不要重复点击按钮

>Clicking the download button will delay for a few seconds after selecting the `directly` or `more options` in the radio box, please do not click the button repeatedly

尤其是选择`more optioins`，GUI需要一些时间获取字幕列表

>Especially when `more optioins` is selected, the GUI takes some time to get the list of subtitles

当你看到`Available automatic captions for XXX:`时，他下面的字幕是自动生成的，这种字幕无法下载（GUI无法下载，但是直接使用yt-dlp搭配正确的指令即可下载，更多操作请查看[yt-dlp项目地址](https://github.com/yt-dlp/yt-dlp)）

>When you see `Available automatic captions for XXX:`, the subtitles below him is automatically generated, and this kind of subtitles cannot be downloaded (GUI cannot be downloaded, but can be downloaded directly by using yt-dlp with the correct command, more For operation, please check [yt-dlp project address](https://github.com/yt-dlp/yt-dlp))

当你看到`Available subtitles for XXX`时，他下面的字幕是可以下载的，下载多种字幕用逗号隔开，更多请查看[yt-dlp项目地址](https://github.com/yt-dlp/yt-dlp)

>When you see `Available subtitles for XXX`, the subtitles below him can be downloaded. Download multiple subtitles separated by commas. For more, please check [yt-dlp project address](https://github.com/ yt-dlp/yt-dlp)

## 全局设定 | Global settings

| 配置(settings)                    | 命令行代码(shell)            | 地址(position)                                               | 内容                                                         | Content                                                      |
| --------------------------------- | ---------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| 代理设置(proxy setting)           | --proxy URL                  | [Network Options](https://github.com/yt-dlp/yt-dlp#network-options) | 使用指定的 HTTP/HTTPS/SOCKS 代理。启用 SOCKS 代理，指定适当的方案， 例如socks5://user:pass@127.0.0.1:1080/。 传入一个空字符串（--proxy ""） 直接连接 | Use the specified HTTP/HTTPS/SOCKS proxy. To enable SOCKS proxy, specify a proper scheme, e.g. socks5://user:pass@127.0.0.1:1080/. Pass in an empty string (--proxy "") for direct connection |
|                                   | --geo-verification-proxy URL | [Geo-restriction](https://github.com/yt-dlp/yt-dlp#geo-restriction) | 一些受地理限制的网站使用此代理验证 IP 地址 。默认代理由 --proxy 指定用于实际下载（若 --proxy 未指定则为`none`） | Use this proxy to verify the IP address for some geo-restricted sites. The default proxy specified by --proxy (or none, if the option is not present) is used for the actual downloading |
| 过滤器设置(filter setting)        | --match-filters FILTER       | [Video Selection](https://github.com/yt-dlp/yt-dlp#video-selection) | 定义视频过滤器模板，在下载视频列表中的文件时符合匹配条件的下载，例如：--match-filter !is_live --match-filter "like_count>?100 & description~='(?i)\bcats \& dogs\b'"匹配不是直播且喜欢超过100（或者喜欢字段不存在）且描述包含猫和狗的词，[了解更多](https://github.com/yt-dlp/yt-dlp#output-template) | Generic video filter. Any "OUTPUT TEMPLATE" field can be compared with a number or a string using the operators defined in "Filtering Formats". You can also simply specify a field to match if the field is present, use "!field" to check if the field is not present, and "&" to check multiple conditions. Use a "\" to escape "&" or quotes if needed. If used multiple times, the filter matches if atleast one of the conditions are met. E.g. --match-filter !is_live --match-filter "like_count>?100 & description~='(?i)\bcats \& dogs\b'" matches only videos that are not live OR those that have a like count more than 100 (or the like field is not available) and also has a description that contains the phrase "cats & dogs" (caseless). Use "--match-filter -" to interactively ask whether to download each video. [more](https://github.com/yt-dlp/yt-dlp#output-template) |
| 限制下载速度(limit download rate) | -r, --limit-rate RATE        | [Download Options](https://github.com/yt-dlp/yt-dlp#download-options) | 以每秒字节数为单位的最大下载速率， 例如50K 或 4.2M           | Maximum download rate in bytes per second, e.g. 50K or 4.2M  |
| 下载地址(download path)           | -P, --paths [TYPES:]PATH     | [Filesystem Options](https://github.com/yt-dlp/yt-dlp#filesystem-options) | 简单来说就是文件的下载地址（例如：C://users//xxx//Videos//youtube） | The paths where the files should be downloaded. Specify the type of file and the path separated by a colon ":".  All the same TYPES as --output are supported. Additionally, you can also provide "home" (default) and "temp" paths. All intermediary files are first downloaded to the temp path and then the final files are moved over to the home path after download is finished.  This option is ignored if --output is an absolute path |
| 下载格式(format)                  | -f, --format FORMAT          | [Video Format Options](https://github.com/yt-dlp/yt-dlp#video-format-options) | 视频格式代码，见“[格式选择](https://github.com/yt-dlp/yt-dlp#format-selection)” 更多细节(GUI默认使用best，提供有bv、ba、bv+ba/b，不支持自定义) | Video format code, see "[FORMAT SELECTION](https://github.com/yt-dlp/yt-dlp#format-selection)" for more details (GUI uses best by default, provides bv, ba, bv+ba/b, does not support customization) |

## 局部设置 | local settings

| 配置(settings)                | 命令行代码(shell)   | 地址(position)                                               | 内容                                                         | Content                                                      |
| ----------------------------- | ------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| 下载描述(write description)   | --write-description | [Filesystem Options](https://github.com/yt-dlp/yt-dlp#filesystem-options) | 将视频描述写入 .description 文件                             | Write video description to a .description file               |
| 下载元数据(write meta data)   | --write-info-json   | [Filesystem Options](https://github.com/yt-dlp/yt-dlp#filesystem-options) | 将视频元数据写入 .info.json 文件 （这可能包含个人信息）      | Write video metadata to a .info.json file (this may contain personal information) |
| 下载评论(write comments)      | --write-comments    | [Filesystem Options](https://github.com/yt-dlp/yt-dlp#filesystem-options) | 检索视频的评论放置在 infojson。如果提取速度很快即使没有这个选项也会获取评论（别名：--get-comments） | Retrieve video comments to be placed in the infojson. The comments are fetched even without this option if the extraction is known to be quick (Alias: --get-comments) |
| 仅下载音频(only audio)        | -x, --extract-audio | [Post-Processing Options](https://github.com/yt-dlp/yt-dlp#post-processing-options) | 将视频文件转换为纯音频文件 （需要 ffmpeg 和 ffprobe）        | Convert video files to audio-only files (requires ffmpeg and ffprobe) |
| 下载缩略图(write thumbnail)   | --write-thumbnail   | [Thumbnail Options](https://github.com/yt-dlp/yt-dlp#thumbnail-options) | 将缩略图图像写入磁盘                                         | Write thumbnail image to disk                                |
| 跳过下载(skip download video) | --skip-download     | [Verbosity and Simulation Options](https://github.com/yt-dlp/yt-dlp#verbosity-and-simulation-options) | 不要下载视频，但要全部写出相关文件（别名：--no-download）    | Do not download the video but write all related files (Alias: --no-download) |
| 下载字幕(write subs)          | --write-subs        | [Subtitle Options](https://github.com/yt-dlp/yt-dlp#subtitle-options) | 写字幕文件                                                   | Write subtitle file                                          |
| 下载字幕的语言                | --sub-langs LANGS   | [Subtitle Options](https://github.com/yt-dlp/yt-dlp#subtitle-options) | 要下载的字幕语言（可以 是正则表达式）或用逗号分隔的“全部”，例如 --sub-langs "en.*,ja"。您可以在前缀 带有“-”的语言代码将其排除在外 请求的语言，例如--子语言 所有，-live_chat。使用 --list-subs 作为列表 可用的语言标签 | Languages of the subtitles to download (can be regex) or "all" separated by commas, e.g. --sub-langs "en.*,ja". You can prefix the language code with a "-" to exclude it from the requested languages, e.g. --sub-langs all,-live_chat. Use --list-subs for a list of available language tags |
| 嵌入字幕(embed subtitles)     | --embed-subs        | [Post-Processing Options](https://github.com/yt-dlp/yt-dlp#post-processing-options) | 在视频中嵌入字幕（仅适用于 mp4、 webm 和 mkv 视频）          | Embed subtitles in the video (only for mp4, webm and mkv videos) |

## 感谢 | Thanks

[ty-dlp](https://github.com/yt-dlp/yt-dlp)

[Pyside6](https://doc.qt.io/qtforpython/PySide6/QtWidgets/index.html)
