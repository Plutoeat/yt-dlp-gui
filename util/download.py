from PySide6.QtCore import QRunnable, QObject, QThreadPool, QThread, Signal
from yt_dlp import YoutubeDL

from util.rw_config import read_config_yaml


class SubThread(QThread):
    outputWritten = Signal(str)

    def __init__(self, opt):
        super(SubThread, self).__init__()
        self.opt = opt

    def run(self, url_list) -> None:
        nydl = NYoutubeDL(self, self.opt)
        nydl.download(url_list)


class NYoutubeDL(YoutubeDL):
    def __init__(self, communication, params):
        super(NYoutubeDL, self).__init__(params)
        self.communication = communication

    def to_screen(self, message, skip_eol=False, quiet=None):
        self.communication.outputWritten.emit(message)
        super(NYoutubeDL, self).to_screen(message)
        
    def to_stdout(self, message, skip_eol=False, quiet=None):
        self.communication.outputWritten.emit(message)
        super(NYoutubeDL, self).to_stdout(message)


def mergeDict(dict1, dict2):
    res = {**dict1, **dict2}
    return res


class Thread(QRunnable):
    communication = None

    def __init__(self):
        super(Thread, self).__init__()
        self.thread_logo = None

    def run(self):
        ytd_opt = self.loadYTDLPConfig()
        all_opt = mergeDict(self.communication.ytd_opt, ytd_opt)
        print(all_opt)
        with YoutubeDL(all_opt) as ydl:
            ydl.download(self.thread_logo)
        self.communication.ytd_opt = {}
        self.communication.log_signal.emit('{}已经下载完成'.format(self.thread_logo))

    def loadYTDLPConfig(self):
        ytd_opt = read_config_yaml()["settings"]
        for key in list(ytd_opt.keys()):
            if not ytd_opt.get(key) or ytd_opt.get(key) is None:
                ytd_opt.pop(key)
        return ytd_opt

    # 自定义函数，用来初始化一些变量
    def transfer(self, thread_logo, communication):
        """
        :param thread_logo:线程标识，方便识别。
        :param communication:信号
        :return:
        """

        self.thread_logo = thread_logo
        self.communication = communication


# 定义任务，在这里主要创建线程
class Tasks(QObject):
    communication = None
    max_thread_number = 0

    def __init__(self, communication, max_thread_number):
        """
        :param communication:通讯
        :param max_thread_number:最大线程数
        """
        super(Tasks, self).__init__()

        self.max_thread_number = max_thread_number
        self.communication = communication

        self.pool = QThreadPool()
        self.pool.globalInstance()

    def start(self):
        # 设置最大线程数

        self.pool.setMaxThreadCount(self.max_thread_number)
        for i in self.communication.links:
            task_thread = Thread()
            task_thread.transfer(thread_logo=i, communication=self.communication)
            task_thread.setAutoDelete(True)
            self.communication.log_signal.emit('{}开始下载'.format(i))
            self.pool.start(task_thread)

        self.pool.waitForDone()
        self.communication.log_signal.emit('任务执行完毕')
        self.communication.statusbar.showMessage("下载完成")
        self.communication.pushButton.setEnabled(True)
        self.communication.flag = False


class DownloadThread(QThread):
    def __init__(self, communication, max_thread_number):
        super(DownloadThread, self).__init__()
        self.task = Tasks(
            communication=communication,
            max_thread_number=max_thread_number
        )

    def run(self) -> None:
        self.task.start()
