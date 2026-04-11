"""Settings panel – 6 collapsible sections with full tooltips."""

from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSlider,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)
from PySide6.QtCore import Qt

from gui.widgets.collapsible_section import CollapsibleSection


class SettingsPanel(QWidget):
    """All download settings organized into collapsible sections."""

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        self._section_format = self._build_format_section()
        self._section_subs = self._build_subtitle_section()
        self._section_postproc = self._build_postprocess_section()
        self._section_auth = self._build_auth_section()
        self._section_download = self._build_download_section()
        self._section_selection = self._build_selection_section()

        for section in [
            self._section_format, self._section_subs, self._section_postproc,
            self._section_auth, self._section_download, self._section_selection,
        ]:
            layout.addWidget(section)

        layout.addStretch()

    # ── Section 1: Format & Quality ─────────────────────────────────────────

    def _hint(self, text: str) -> QLabel:
        """Create a styled hint label."""
        label = QLabel(text)
        label.setWordWrap(True)
        label.setStyleSheet("color: #909399; font-size: 12px; padding: 2px 0 6px 0;")
        return label

    def _build_format_section(self) -> CollapsibleSection:
        section = CollapsibleSection("Format & Quality")
        section.add_widget(self._hint(
            "选择视频/音频的下载格式和质量。留空 Format 将自动选择最佳格式。"
            "有 ffmpeg 时会自动合并最佳视频+音频流。"
        ))
        form = QFormLayout()
        form.setHorizontalSpacing(14)
        form.setVerticalSpacing(10)

        self.format_combo = QComboBox()
        self.format_combo.setEditable(True)
        self.format_combo.addItems([
            "", "b", "bv*+ba/b", "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]",
            "bv*[height<=720]+ba/b[height<=720]",
            "bv*[height<=1080]+ba/b[height<=1080]",
            "bv", "ba",
        ])
        self.format_combo.setToolTip(
            "视频格式选择 (留空=自动选最佳)\n\n"
            "常用格式:\n"
            "  b — 最佳单文件 (不需要ffmpeg)\n"
            "  bv*+ba/b — 最佳视频+最佳音频合并 (需要ffmpeg)\n"
            "  bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4] — 最佳MP4\n"
            "  bv*[height<=720]+ba — 最高720p\n"
            "  ba — 仅下载音频\n\n"
            "支持自定义格式字符串，详见 yt-dlp 文档"
        )
        form.addRow("Format:", self.format_combo)

        self.format_sort_edit = QLineEdit()
        self.format_sort_edit.setPlaceholderText("e.g. res:720,+size")
        self.format_sort_edit.setToolTip(
            "格式排序优先级 (-S 参数)\n\n"
            "示例:\n"
            "  res:720 — 优先不超过720p\n"
            "  +size — 优先最小文件\n"
            "  codec:h264 — 优先H.264编码\n"
            "  fps — 优先最高帧率\n"
            "多个条件用逗号分隔"
        )
        form.addRow("Format Sort:", self.format_sort_edit)

        self.merge_format_combo = QComboBox()
        self.merge_format_combo.addItems(["", "mp4", "mkv", "webm", "avi"])
        self.merge_format_combo.setToolTip(
            "合并视频+音频时的输出容器格式\n\n"
            "当下载的视频流和音频流是分开的时,\n"
            "ffmpeg会将它们合并到此容器中\n\n"
            "mp4 — 兼容性最好\n"
            "mkv — 支持更多编码和字幕格式\n"
            "webm — 适合网页播放"
        )
        form.addRow("Merge Output:", self.merge_format_combo)

        self.audio_format_combo = QComboBox()
        self.audio_format_combo.addItems(["mp3", "m4a", "opus", "flac", "wav", "best"])
        self.audio_format_combo.setToolTip(
            "提取音频时的输出格式\n\n"
            "mp3 — 通用,兼容性最好\n"
            "m4a — Apple生态,音质好\n"
            "opus — 体积小,音质好\n"
            "flac — 无损音频\n"
            "wav — 无压缩原始音频\n"
            "best — 保持原始格式不转码"
        )
        form.addRow("Audio Format:", self.audio_format_combo)

        quality_layout = QHBoxLayout()
        self.audio_quality_slider = QSlider(Qt.Horizontal)
        self.audio_quality_slider.setRange(0, 10)
        self.audio_quality_slider.setValue(5)
        self.audio_quality_slider.setTickPosition(QSlider.TicksBelow)
        self.audio_quality_slider.setToolTip(
            "音频质量 (0=最好, 10=最差)\n"
            "仅在提取音频时生效\n"
            "对应 VBR 编码质量等级"
        )
        self.audio_quality_label = QLabel("5")
        self.audio_quality_slider.valueChanged.connect(
            lambda v: self.audio_quality_label.setText(str(v))
        )
        quality_layout.addWidget(QLabel("Best"))
        quality_layout.addWidget(self.audio_quality_slider, 1)
        quality_layout.addWidget(QLabel("Worst"))
        quality_layout.addWidget(self.audio_quality_label)
        form.addRow("Audio Quality:", quality_layout)

        self.remux_combo = QComboBox()
        self.remux_combo.addItems(["", "mp4", "mkv", "webm", "avi", "mov", "flv"])
        self.remux_combo.setToolTip(
            "重封装: 更换容器格式但不重新编码\n"
            "速度很快,不损失画质\n"
            "例: 将 webm 重封装为 mp4"
        )
        form.addRow("Remux To:", self.remux_combo)

        self.recode_combo = QComboBox()
        self.recode_combo.addItems(["", "mp4", "mkv", "webm", "avi", "flv"])
        self.recode_combo.setToolTip(
            "重编码: 转换为不同格式\n"
            "⚠ 速度较慢,可能损失画质\n"
            "仅在需要特定编码时使用"
        )
        form.addRow("Recode To:", self.recode_combo)

        section.add_layout(form)
        return section

    # ── Section 2: Subtitles ────────────────────────────────────────────────

    def _build_subtitle_section(self) -> CollapsibleSection:
        section = CollapsibleSection("Subtitles")
        section.add_widget(self._hint(
            "下载字幕并可选嵌入视频。支持人工字幕和自动生成字幕，"
            "语言用逗号分隔 (如 en,zh-Hans)。嵌入字幕需要 ffmpeg 且容器为 mp4/mkv/webm。"
        ))
        form = QFormLayout()
        form.setHorizontalSpacing(14)
        form.setVerticalSpacing(10)

        self.cb_subtitles = QCheckBox("Download Subtitles")
        self.cb_subtitles.setToolTip("下载视频的人工字幕文件")
        self.cb_auto_subs = QCheckBox("Download Auto-generated Subtitles")
        self.cb_auto_subs.setToolTip("下载自动生成的字幕 (机器翻译/语音识别)")
        form.addRow(self.cb_subtitles)
        form.addRow(self.cb_auto_subs)

        self.sub_langs_edit = QLineEdit()
        self.sub_langs_edit.setPlaceholderText("all,-live_chat  or  en,zh-Hans")
        self.sub_langs_edit.setToolTip(
            "字幕语言选择 (逗号分隔)\n\n"
            "示例:\n"
            "  all — 所有语言\n"
            "  all,-live_chat — 所有语言但排除聊天记录\n"
            "  en,zh-Hans — 英文和简体中文\n"
            "  en.*,ja — 所有英文变体和日文\n"
            "支持正则表达式"
        )
        form.addRow("Languages:", self.sub_langs_edit)

        self.sub_format_combo = QComboBox()
        self.sub_format_combo.addItems(["best", "vtt", "srt", "ass", "lrc"])
        self.sub_format_combo.setToolTip(
            "字幕下载格式\n\n"
            "srt — 最通用,大多数播放器支持\n"
            "vtt — Web视频常用\n"
            "ass — 支持样式和定位\n"
            "lrc — 歌词格式"
        )
        form.addRow("Format:", self.sub_format_combo)

        self.convert_subs_combo = QComboBox()
        self.convert_subs_combo.addItems(["", "srt", "vtt", "ass", "lrc"])
        self.convert_subs_combo.setToolTip(
            "下载后自动转换字幕格式\n"
            "留空则保持原始格式不转换"
        )
        form.addRow("Convert To:", self.convert_subs_combo)

        self.cb_embed_subs = QCheckBox("Embed Subtitles into Video (mp4/mkv/webm)")
        self.cb_embed_subs.setToolTip(
            "将字幕嵌入视频文件内部\n"
            "播放时可选择显示/隐藏\n"
            "仅支持 mp4, mkv, webm 容器\n"
            "需要 ffmpeg"
        )
        form.addRow(self.cb_embed_subs)

        section.add_layout(form)
        return section

    # ── Section 3: Post-Processing ──────────────────────────────────────────

    def _build_postprocess_section(self) -> CollapsibleSection:
        section = CollapsibleSection("Post-Processing")
        section.add_widget(self._hint(
            "下载完成后的自动处理：嵌入元数据/章节/封面、提取音频、"
            "格式转换、SponsorBlock 去广告等。大部分功能需要安装 ffmpeg。"
        ))
        form = QFormLayout()
        form.setHorizontalSpacing(14)
        form.setVerticalSpacing(10)

        self.cb_embed_metadata = QCheckBox("Embed Metadata")
        self.cb_embed_metadata.setChecked(True)
        self.cb_embed_metadata.setToolTip("将标题、作者、日期等元信息写入文件标签")

        self.cb_embed_chapters = QCheckBox("Embed Chapters")
        self.cb_embed_chapters.setChecked(True)
        self.cb_embed_chapters.setToolTip("将视频章节信息嵌入文件,播放器可显示章节导航")

        self.cb_embed_thumbnail = QCheckBox("Embed Thumbnail")
        self.cb_embed_thumbnail.setToolTip("将视频封面图嵌入文件 (作为专辑封面)")

        self.cb_extract_audio = QCheckBox("Extract Audio Only (requires ffmpeg)")
        self.cb_extract_audio.setToolTip("下载后提取音频,丢弃视频\n配合上方 Audio Format 设置输出格式")

        self.cb_keep_video = QCheckBox("Keep Original Video after Extraction")
        self.cb_keep_video.setToolTip("提取音频后保留原始视频文件不删除")

        self.cb_split_chapters = QCheckBox("Split Video by Chapters")
        self.cb_split_chapters.setToolTip("按章节将视频切割为多个独立文件")

        for cb in [
            self.cb_embed_metadata, self.cb_embed_chapters, self.cb_embed_thumbnail,
            self.cb_extract_audio, self.cb_keep_video, self.cb_split_chapters,
        ]:
            form.addRow(cb)

        self.convert_thumb_combo = QComboBox()
        self.convert_thumb_combo.addItems(["", "jpg", "png", "webp"])
        self.convert_thumb_combo.setToolTip("下载缩略图后自动转换格式")
        form.addRow("Convert Thumbnail:", self.convert_thumb_combo)

        # SponsorBlock
        self.sponsorblock_combo = QComboBox()
        self.sponsorblock_combo.addItems(["None", "Mark as Chapters", "Remove Segments"])
        self.sponsorblock_combo.setToolTip(
            "SponsorBlock: 自动处理赞助商片段\n\n"
            "Mark — 将赞助片段标记为章节\n"
            "Remove — 直接删除赞助片段\n"
            "需要 ffmpeg"
        )
        form.addRow("SponsorBlock:", self.sponsorblock_combo)

        self.sponsorblock_cats_edit = QLineEdit()
        self.sponsorblock_cats_edit.setPlaceholderText("sponsor,intro,outro,selfpromo")
        self.sponsorblock_cats_edit.setToolTip(
            "SponsorBlock 分类 (逗号分隔)\n\n"
            "可选: sponsor, intro, outro,\n"
            "interaction, selfpromo,\n"
            "music_offtopic, preview, filler"
        )
        form.addRow("SB Categories:", self.sponsorblock_cats_edit)

        self.ffmpeg_path_edit = QLineEdit()
        self.ffmpeg_path_edit.setPlaceholderText("Auto-detect")
        self.ffmpeg_path_edit.setToolTip(
            "FFmpeg 可执行文件路径\n"
            "留空则自动从 PATH 中检测\n"
            "所有后处理功能都需要 ffmpeg"
        )
        ffmpeg_layout = QHBoxLayout()
        ffmpeg_layout.addWidget(self.ffmpeg_path_edit, 1)
        ffmpeg_browse = QPushButton("Browse…")
        ffmpeg_browse.clicked.connect(self._browse_ffmpeg)
        ffmpeg_layout.addWidget(ffmpeg_browse)
        form.addRow("FFmpeg Path:", ffmpeg_layout)

        section.add_layout(form)
        return section

    # ── Section 4: Authentication ───────────────────────────────────────────

    def _build_auth_section(self) -> CollapsibleSection:
        section = CollapsibleSection("Authentication")
        section.add_widget(self._hint(
            "访问需要登录的视频。推荐使用浏览器 Cookie 导入 (最安全)，"
            "选择你已登录目标网站的浏览器即可。"
        ))
        form = QFormLayout()
        form.setHorizontalSpacing(14)
        form.setVerticalSpacing(10)

        self.cookie_browser_combo = QComboBox()
        self.cookie_browser_combo.addItems(["None", "chrome", "firefox", "edge", "safari", "brave"])
        self.cookie_browser_combo.setToolTip(
            "从浏览器自动导入 Cookie\n"
            "可访问需要登录的视频\n"
            "选择你已登录目标网站的浏览器"
        )
        form.addRow("Cookies from Browser:", self.cookie_browser_combo)

        cookie_layout = QHBoxLayout()
        self.cookie_file_edit = QLineEdit()
        self.cookie_file_edit.setPlaceholderText("Netscape cookie file path")
        self.cookie_file_edit.setToolTip(
            "Netscape 格式的 Cookie 文件路径\n"
            "可用浏览器扩展导出\n"
            "适合不想直接读取浏览器数据的场景"
        )
        cookie_browse = QPushButton("Browse…")
        cookie_browse.clicked.connect(self._browse_cookie_file)
        cookie_layout.addWidget(self.cookie_file_edit, 1)
        cookie_layout.addWidget(cookie_browse)
        form.addRow("Cookie File:", cookie_layout)

        self.username_edit = QLineEdit()
        self.username_edit.setToolTip("网站登录用户名 (仅少数站点支持)")
        form.addRow("Username:", self.username_edit)

        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.password_edit.setToolTip("网站登录密码\n⚠ 密码不会加密存储,建议优先使用 Cookie")
        form.addRow("Password:", self.password_edit)

        self.cb_netrc = QCheckBox("Use .netrc for authentication")
        self.cb_netrc.setToolTip(
            "从 ~/.netrc 文件读取登录凭据\n"
            "格式: machine youtube.com login user password pass"
        )
        form.addRow(self.cb_netrc)

        section.add_layout(form)
        return section

    # ── Section 5: Download Settings ────────────────────────────────────────

    def _build_download_section(self) -> CollapsibleSection:
        section = CollapsibleSection("Download Settings")
        section.add_widget(self._hint(
            "下载路径、文件名模板、代理、限速等基本设置。"
            "文件名模板支持 %(title)s %(id)s %(uploader)s 等变量。"
        ))
        form = QFormLayout()
        form.setHorizontalSpacing(14)
        form.setVerticalSpacing(10)

        path_layout = QHBoxLayout()
        self.path_edit = QLineEdit()
        self.path_edit.setPlaceholderText("Select download directory…")
        self.path_edit.setToolTip("视频下载保存目录")
        path_browse = QPushButton("Browse…")
        path_browse.clicked.connect(self._browse_path)
        path_layout.addWidget(self.path_edit, 1)
        path_layout.addWidget(path_browse)
        form.addRow("Download Path:", path_layout)

        self.outtmpl_edit = QLineEdit()
        self.outtmpl_edit.setPlaceholderText("%(title)s.%(ext)s")
        self.outtmpl_edit.setToolTip(
            "输出文件名模板\n\n"
            "常用变量:\n"
            "  %(title)s — 视频标题\n"
            "  %(id)s — 视频ID\n"
            "  %(ext)s — 文件扩展名\n"
            "  %(uploader)s — 上传者\n"
            "  %(upload_date)s — 上传日期 (YYYYMMDD)\n"
            "  %(playlist_index)s — 播放列表序号\n"
            "  %(resolution)s — 分辨率\n\n"
            "示例: %(uploader)s/%(title)s [%(id)s].%(ext)s"
        )
        form.addRow("Filename Template:", self.outtmpl_edit)

        self.proxy_edit = QLineEdit()
        self.proxy_edit.setPlaceholderText("socks5://127.0.0.1:1080")
        self.proxy_edit.setToolTip(
            "HTTP/HTTPS/SOCKS 代理地址\n\n"
            "示例:\n"
            "  http://127.0.0.1:7890\n"
            "  socks5://user:pass@127.0.0.1:1080\n"
            "留空则直连"
        )
        form.addRow("Proxy:", self.proxy_edit)

        self.geo_proxy_edit = QLineEdit()
        self.geo_proxy_edit.setPlaceholderText("Proxy for geo-verification only")
        self.geo_proxy_edit.setToolTip(
            "仅用于地理位置验证的代理\n"
            "实际下载仍使用上方的 Proxy 设置\n"
            "用于绕过某些网站的地区限制检查"
        )
        form.addRow("Geo-Verify Proxy:", self.geo_proxy_edit)

        self.ratelimit_edit = QLineEdit()
        self.ratelimit_edit.setPlaceholderText("e.g. 50K or 4.2M")
        self.ratelimit_edit.setToolTip(
            "最大下载速率限制\n\n"
            "示例: 50K = 50KB/s, 4.2M = 4.2MB/s\n"
            "留空则不限速"
        )
        form.addRow("Rate Limit:", self.ratelimit_edit)

        self.workers_spin = QSpinBox()
        self.workers_spin.setRange(1, 10)
        self.workers_spin.setValue(3)
        self.workers_spin.setToolTip("同时下载的最大任务数")
        form.addRow("Concurrent Downloads:", self.workers_spin)

        self.fragment_spin = QSpinBox()
        self.fragment_spin.setRange(1, 16)
        self.fragment_spin.setValue(1)
        self.fragment_spin.setToolTip(
            "每个任务的分片并发下载数\n"
            "提高此值可加速分段视频的下载\n"
            "建议值: 1-4, 过高可能被限速"
        )
        form.addRow("Fragment Concurrency:", self.fragment_spin)

        self.ext_downloader_combo = QComboBox()
        self.ext_downloader_combo.addItems(["", "aria2c", "axel", "curl"])
        self.ext_downloader_combo.setToolTip(
            "使用外部下载器替代内置下载\n\n"
            "aria2c — 支持多线程,速度快\n"
            "axel — 轻量级多线程下载器\n"
            "需要自行安装对应工具"
        )
        form.addRow("External Downloader:", self.ext_downloader_combo)

        self.sleep_spin = QSpinBox()
        self.sleep_spin.setRange(0, 60)
        self.sleep_spin.setSuffix(" sec")
        self.sleep_spin.setToolTip(
            "每次请求间的等待时间 (秒)\n"
            "可避免因请求过于频繁被网站封禁\n"
            "下载播放列表时建议设置 1-3 秒"
        )
        form.addRow("Sleep Between Requests:", self.sleep_spin)

        archive_layout = QHBoxLayout()
        self.archive_edit = QLineEdit()
        self.archive_edit.setPlaceholderText("Path to download archive file")
        self.archive_edit.setToolTip(
            "下载存档文件路径\n"
            "已下载的视频ID会记录在此文件中\n"
            "再次运行时自动跳过已下载的视频\n"
            "适合定期同步频道/播放列表"
        )
        archive_browse = QPushButton("Browse…")
        archive_browse.clicked.connect(self._browse_archive)
        archive_layout.addWidget(self.archive_edit, 1)
        archive_layout.addWidget(archive_browse)
        form.addRow("Download Archive:", archive_layout)

        section.add_layout(form)
        return section

    # ── Section 6: Video Selection ──────────────────────────────────────────

    def _build_selection_section(self) -> CollapsibleSection:
        section = CollapsibleSection("Video Selection")
        section.add_widget(self._hint(
            "过滤和筛选要下载的视频：播放列表范围、文件大小限制、日期过滤等。"
            "默认下载所有内容，按需设置条件。"
        ))
        form = QFormLayout()
        form.setHorizontalSpacing(14)
        form.setVerticalSpacing(10)

        self.cb_noplaylist = QCheckBox("Only download single video (ignore playlist)")
        self.cb_noplaylist.setToolTip("当URL同时指向视频和播放列表时,只下载单个视频")
        form.addRow(self.cb_noplaylist)

        self.playlist_items_edit = QLineEdit()
        self.playlist_items_edit.setPlaceholderText("e.g. 1-3,5,7-9")
        self.playlist_items_edit.setToolTip(
            "选择播放列表中的特定项目\n\n"
            "示例:\n"
            "  1-3 — 第1到第3个\n"
            "  1,3,5 — 第1、3、5个\n"
            "  -3:: — 倒数第3个到最后\n"
            "  ::2 — 每隔一个下载"
        )
        form.addRow("Playlist Items:", self.playlist_items_edit)

        size_layout = QHBoxLayout()
        self.min_filesize_edit = QLineEdit()
        self.min_filesize_edit.setPlaceholderText("Min e.g. 10M")
        self.min_filesize_edit.setToolTip("文件小于此大小则跳过\n示例: 10M = 10MB")
        self.max_filesize_edit = QLineEdit()
        self.max_filesize_edit.setPlaceholderText("Max e.g. 500M")
        self.max_filesize_edit.setToolTip("文件大于此大小则跳过\n示例: 500M = 500MB")
        size_layout.addWidget(QLabel("Min:"))
        size_layout.addWidget(self.min_filesize_edit, 1)
        size_layout.addSpacing(8)
        size_layout.addWidget(QLabel("Max:"))
        size_layout.addWidget(self.max_filesize_edit, 1)
        form.addRow("File Size:", size_layout)

        date_layout = QHBoxLayout()
        self.date_start_edit = QLineEdit()
        self.date_start_edit.setPlaceholderText("YYYYMMDD")
        self.date_start_edit.setToolTip("只下载此日期之后上传的视频")
        self.date_end_edit = QLineEdit()
        self.date_end_edit.setPlaceholderText("YYYYMMDD")
        self.date_end_edit.setToolTip("只下载此日期之前上传的视频")
        date_layout.addWidget(QLabel("After:"))
        date_layout.addWidget(self.date_start_edit, 1)
        date_layout.addSpacing(8)
        date_layout.addWidget(QLabel("Before:"))
        date_layout.addWidget(self.date_end_edit, 1)
        form.addRow("Date Range:", date_layout)

        self.match_filter_edit = QLineEdit()
        self.match_filter_edit.setPlaceholderText("e.g. !is_live & duration>60")
        self.match_filter_edit.setToolTip(
            "自定义视频过滤条件\n\n"
            "示例:\n"
            "  !is_live — 排除直播\n"
            "  duration>60 — 时长超过60秒\n"
            "  like_count>?100 — 点赞超过100\n"
            "  description~='(?i)\\bcats\\b' — 描述包含cats\n"
            "多条件用 & 连接"
        )
        form.addRow("Match Filter:", self.match_filter_edit)

        self.max_downloads_spin = QSpinBox()
        self.max_downloads_spin.setRange(0, 9999)
        self.max_downloads_spin.setSpecialValueText("No limit")
        self.max_downloads_spin.setSingleStep(5)
        self.max_downloads_spin.setToolTip("最大下载数量,达到后停止\n0 = 不限制")
        form.addRow("Max Downloads:", self.max_downloads_spin)

        section.add_layout(form)
        return section

    # ── Browse helpers ──────────────────────────────────────────────────────

    def _browse_path(self):
        path = QFileDialog.getExistingDirectory(self, "Select Download Directory")
        if path:
            self.path_edit.setText(path)

    def _browse_ffmpeg(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select FFmpeg Binary")
        if path:
            self.ffmpeg_path_edit.setText(path)

    def _browse_cookie_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Cookie File", "", "Text Files (*.txt);;All Files (*)")
        if path:
            self.cookie_file_edit.setText(path)

    def _browse_archive(self):
        path, _ = QFileDialog.getSaveFileName(self, "Download Archive File", "", "Text Files (*.txt);;All Files (*)")
        if path:
            self.archive_edit.setText(path)

    # ── Collect / Apply ─────────────────────────────────────────────────────

    def collect_opts(self) -> dict:
        """Collect current UI state into a flat dict for ydl_opts.build_opts()."""
        opts: dict = {}

        # Format & Quality
        fmt = self.format_combo.currentText().strip()
        if fmt:
            opts["format"] = fmt
        fmt_sort = self.format_sort_edit.text().strip()
        if fmt_sort:
            opts["format_sort"] = fmt_sort
        merge = self.merge_format_combo.currentText()
        if merge:
            opts["merge_output_format"] = merge
        opts["audio_format"] = self.audio_format_combo.currentText()
        opts["audio_quality"] = self.audio_quality_slider.value()
        remux = self.remux_combo.currentText()
        if remux:
            opts["remux_video"] = remux
        recode = self.recode_combo.currentText()
        if recode:
            opts["recode_video"] = recode

        # Subtitles
        opts["writesubtitles"] = self.cb_subtitles.isChecked()
        opts["write_auto_subs"] = self.cb_auto_subs.isChecked()
        sub_langs = self.sub_langs_edit.text().strip()
        if sub_langs:
            opts["subtitleslangs"] = sub_langs
        elif self.cb_subtitles.isChecked():
            opts["subtitleslangs"] = "all,-live_chat"
        sub_fmt = self.sub_format_combo.currentText()
        if sub_fmt != "best":
            opts["sub_format"] = sub_fmt
        convert_subs = self.convert_subs_combo.currentText()
        if convert_subs:
            opts["convert_subs"] = convert_subs
        opts["embedsubtitles"] = self.cb_embed_subs.isChecked()

        # Post-Processing
        opts["embed_metadata"] = self.cb_embed_metadata.isChecked()
        opts["embed_chapters"] = self.cb_embed_chapters.isChecked()
        opts["embedthumbnail"] = self.cb_embed_thumbnail.isChecked()
        opts["extract_audio"] = self.cb_extract_audio.isChecked()
        opts["keep_video"] = self.cb_keep_video.isChecked()
        opts["split_chapters"] = self.cb_split_chapters.isChecked()
        convert_thumb = self.convert_thumb_combo.currentText()
        if convert_thumb:
            opts["convert_thumbnails"] = convert_thumb
        sb_action = self.sponsorblock_combo.currentIndex()
        sb_cats = self.sponsorblock_cats_edit.text().strip()
        if sb_action == 1 and sb_cats:
            opts["sponsorblock_mark"] = sb_cats
        elif sb_action == 2 and sb_cats:
            opts["sponsorblock_remove"] = sb_cats
        ffmpeg = self.ffmpeg_path_edit.text().strip()
        if ffmpeg:
            opts["ffmpeg_location"] = ffmpeg

        # Authentication
        browser = self.cookie_browser_combo.currentText()
        if browser != "None":
            opts["cookiesfrombrowser"] = browser
        cookie_file = self.cookie_file_edit.text().strip()
        if cookie_file:
            opts["cookiefile"] = cookie_file
        username = self.username_edit.text().strip()
        if username:
            opts["username"] = username
        password = self.password_edit.text()
        if password:
            opts["password"] = password
        opts["netrc"] = self.cb_netrc.isChecked()

        # Download Settings
        dl_path = self.path_edit.text().strip()
        if dl_path:
            opts["paths"] = {"home": dl_path}
        outtmpl = self.outtmpl_edit.text().strip()
        if outtmpl:
            opts["outtmpl"] = outtmpl
        proxy = self.proxy_edit.text().strip()
        if proxy:
            opts["proxy"] = proxy
        geo_proxy = self.geo_proxy_edit.text().strip()
        if geo_proxy:
            opts["geo_verification_proxy"] = geo_proxy
        ratelimit = self.ratelimit_edit.text().strip()
        if ratelimit:
            opts["ratelimit"] = ratelimit
        frag = self.fragment_spin.value()
        if frag > 1:
            opts["concurrent_fragment_downloads"] = frag
        ext_dl = self.ext_downloader_combo.currentText()
        if ext_dl:
            opts["external_downloader"] = ext_dl
        sleep = self.sleep_spin.value()
        if sleep > 0:
            opts["sleep_interval"] = sleep
        archive = self.archive_edit.text().strip()
        if archive:
            opts["download_archive"] = archive

        # Video Selection
        if self.cb_noplaylist.isChecked():
            opts["noplaylist"] = True
        playlist_items = self.playlist_items_edit.text().strip()
        if playlist_items:
            opts["playlist_items"] = playlist_items
        min_fs = self.min_filesize_edit.text().strip()
        if min_fs:
            opts["min_filesize"] = min_fs
        max_fs = self.max_filesize_edit.text().strip()
        if max_fs:
            opts["max_filesize"] = max_fs
        date_start = self.date_start_edit.text().strip()
        if date_start:
            opts["date_range_start"] = date_start
        date_end = self.date_end_edit.text().strip()
        if date_end:
            opts["date_range_end"] = date_end
        match_filter = self.match_filter_edit.text().strip()
        if match_filter:
            opts["match_filter"] = match_filter
        max_dl = self.max_downloads_spin.value()
        if max_dl > 0:
            opts["max_downloads"] = max_dl

        return opts

    def collect_settings_dict(self) -> dict:
        """Collect current UI state as app_settings keys (for persistence)."""
        s: dict = {}
        s["format"] = self.format_combo.currentText().strip()
        s["format_sort"] = self.format_sort_edit.text().strip()
        s["merge_output_format"] = self.merge_format_combo.currentText()
        s["audio_format"] = self.audio_format_combo.currentText()
        s["audio_quality"] = self.audio_quality_slider.value()
        s["remux_video"] = self.remux_combo.currentText()
        s["recode_video"] = self.recode_combo.currentText()
        s["writesubtitles"] = self.cb_subtitles.isChecked()
        s["write_auto_subs"] = self.cb_auto_subs.isChecked()
        s["subtitleslangs"] = self.sub_langs_edit.text().strip()
        s["sub_format"] = self.sub_format_combo.currentText()
        s["convert_subs"] = self.convert_subs_combo.currentText()
        s["embed_subs"] = self.cb_embed_subs.isChecked()
        s["embed_metadata"] = self.cb_embed_metadata.isChecked()
        s["embed_chapters"] = self.cb_embed_chapters.isChecked()
        s["embedthumbnail"] = self.cb_embed_thumbnail.isChecked()
        s["extract_audio"] = self.cb_extract_audio.isChecked()
        s["keep_video"] = self.cb_keep_video.isChecked()
        s["split_chapters"] = self.cb_split_chapters.isChecked()
        s["convert_thumbnails"] = self.convert_thumb_combo.currentText()
        sb = self.sponsorblock_combo.currentIndex()
        cats = self.sponsorblock_cats_edit.text().strip()
        s["sponsorblock_mark"] = cats if sb == 1 else ""
        s["sponsorblock_remove"] = cats if sb == 2 else ""
        s["ffmpeg_location"] = self.ffmpeg_path_edit.text().strip()
        s["cookiesfrombrowser"] = self.cookie_browser_combo.currentText()
        s["cookiefile"] = self.cookie_file_edit.text().strip()
        s["username"] = self.username_edit.text().strip()
        s["password"] = self.password_edit.text()
        s["netrc"] = self.cb_netrc.isChecked()
        s["download_path"] = self.path_edit.text().strip()
        s["outtmpl"] = self.outtmpl_edit.text().strip()
        s["proxy"] = self.proxy_edit.text().strip()
        s["geo_verification_proxy"] = self.geo_proxy_edit.text().strip()
        s["ratelimit"] = self.ratelimit_edit.text().strip()
        s["max_workers"] = self.workers_spin.value()
        s["concurrent_fragment_downloads"] = self.fragment_spin.value()
        s["external_downloader"] = self.ext_downloader_combo.currentText()
        s["sleep_interval"] = self.sleep_spin.value()
        s["download_archive"] = self.archive_edit.text().strip()
        s["noplaylist"] = self.cb_noplaylist.isChecked()
        s["playlist_items"] = self.playlist_items_edit.text().strip()
        s["min_filesize"] = self.min_filesize_edit.text().strip()
        s["max_filesize"] = self.max_filesize_edit.text().strip()
        s["date_range_start"] = self.date_start_edit.text().strip()
        s["date_range_end"] = self.date_end_edit.text().strip()
        s["match_filter"] = self.match_filter_edit.text().strip()
        s["max_downloads"] = self.max_downloads_spin.value()
        return s

    def apply_settings(self, settings: dict):
        """Populate UI from a settings dict."""
        def _set_combo(combo, val):
            idx = combo.findText(val)
            if idx >= 0:
                combo.setCurrentIndex(idx)
            elif combo.isEditable():
                combo.setEditText(val)

        _set_combo(self.format_combo, settings.get("format", ""))
        self.format_sort_edit.setText(settings.get("format_sort", ""))
        _set_combo(self.merge_format_combo, settings.get("merge_output_format", ""))
        _set_combo(self.audio_format_combo, settings.get("audio_format", "mp3"))
        self.audio_quality_slider.setValue(settings.get("audio_quality", 5))
        _set_combo(self.remux_combo, settings.get("remux_video", ""))
        _set_combo(self.recode_combo, settings.get("recode_video", ""))
        self.cb_subtitles.setChecked(settings.get("writesubtitles", False))
        self.cb_auto_subs.setChecked(settings.get("write_auto_subs", False))
        self.sub_langs_edit.setText(settings.get("subtitleslangs", ""))
        _set_combo(self.sub_format_combo, settings.get("sub_format", "best"))
        _set_combo(self.convert_subs_combo, settings.get("convert_subs", ""))
        self.cb_embed_subs.setChecked(settings.get("embed_subs", False))
        self.cb_embed_metadata.setChecked(settings.get("embed_metadata", True))
        self.cb_embed_chapters.setChecked(settings.get("embed_chapters", True))
        self.cb_embed_thumbnail.setChecked(settings.get("embedthumbnail", False))
        self.cb_extract_audio.setChecked(settings.get("extract_audio", False))
        self.cb_keep_video.setChecked(settings.get("keep_video", False))
        self.cb_split_chapters.setChecked(settings.get("split_chapters", False))
        _set_combo(self.convert_thumb_combo, settings.get("convert_thumbnails", ""))
        sb_mark = settings.get("sponsorblock_mark", "")
        sb_remove = settings.get("sponsorblock_remove", "")
        if sb_remove:
            self.sponsorblock_combo.setCurrentIndex(2)
            self.sponsorblock_cats_edit.setText(sb_remove)
        elif sb_mark:
            self.sponsorblock_combo.setCurrentIndex(1)
            self.sponsorblock_cats_edit.setText(sb_mark)
        else:
            self.sponsorblock_combo.setCurrentIndex(0)
        self.ffmpeg_path_edit.setText(settings.get("ffmpeg_location", ""))
        _set_combo(self.cookie_browser_combo, settings.get("cookiesfrombrowser", "None"))
        self.cookie_file_edit.setText(settings.get("cookiefile", ""))
        self.username_edit.setText(settings.get("username", ""))
        self.password_edit.setText(settings.get("password", ""))
        self.cb_netrc.setChecked(settings.get("netrc", False))
        self.path_edit.setText(settings.get("download_path", ""))
        self.outtmpl_edit.setText(settings.get("outtmpl", ""))
        self.proxy_edit.setText(settings.get("proxy", ""))
        self.geo_proxy_edit.setText(settings.get("geo_verification_proxy", ""))
        self.ratelimit_edit.setText(settings.get("ratelimit", ""))
        self.workers_spin.setValue(settings.get("max_workers", 3))
        self.fragment_spin.setValue(settings.get("concurrent_fragment_downloads", 1))
        _set_combo(self.ext_downloader_combo, settings.get("external_downloader", ""))
        self.sleep_spin.setValue(settings.get("sleep_interval", 0))
        self.archive_edit.setText(settings.get("download_archive", ""))
        self.cb_noplaylist.setChecked(settings.get("noplaylist", False))
        self.playlist_items_edit.setText(settings.get("playlist_items", ""))
        self.min_filesize_edit.setText(settings.get("min_filesize", ""))
        self.max_filesize_edit.setText(settings.get("max_filesize", ""))
        self.date_start_edit.setText(settings.get("date_range_start", ""))
        self.date_end_edit.setText(settings.get("date_range_end", ""))
        self.match_filter_edit.setText(settings.get("match_filter", ""))
        self.max_downloads_spin.setValue(settings.get("max_downloads", 0))

    def apply_preset(self, preset: dict):
        """Apply a preset dict on top of current settings."""
        self.apply_settings(preset)
