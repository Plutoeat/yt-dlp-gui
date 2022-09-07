import os
import sys

from PySide6 import QtGui
from PySide6.QtCore import Signal
from PySide6.QtGui import QTextCursor
from PySide6.QtWidgets import QMainWindow, QApplication, QDialog

from model.index import Ui_MainWindow
from util import rw_config
from util.download import DownloadThread, NYoutubeDL, SubThread
from model.settings import Ui_Dialog
from model.more_options import Ui_More_Dialog
from util.rw_config import read_config_yaml, write_config_yml


class NSettings(QDialog, Ui_Dialog):
    def __init__(self):
        super(NSettings, self).__init__()
        self.setupUi(self)
        self.read_config()

    def read_config(self):
        ydp_opt = read_config_yaml()
        if ydp_opt['settings']['proxy'] is None:
            self.lineEdit.setText("")
        else:
            self.lineEdit.setText(ydp_opt['settings']['proxy'])
        if ydp_opt['settings']['match_filter'] is None:
            self.lineEdit_2.setText("")
        else:
            self.lineEdit_2.setText(ydp_opt['settings']['match_filter'])
        if ydp_opt['settings']['ratelimit'] is None:
            self.lineEdit_3.setText("")
        else:
            self.lineEdit_3.setText(ydp_opt['settings']['ratelimit'])
        if ydp_opt['settings']['paths']['home'] is None:
            self.lineEdit_4.setText("")
        else:
            self.lineEdit_4.setText(ydp_opt['settings']['paths']['home'])
        if ydp_opt['settings']['format'] is None or ydp_opt['settings']['format'] == 'b':
            self.radioButton.setChecked(True)
        elif ydp_opt['settings']['format'] == 'bv':
            self.radioButton_2.setChecked(True)
        elif ydp_opt['settings']['format'] == 'ba':
            self.radioButton_3.setChecked(True)
        elif ydp_opt['settings']['format'] == 'bv+ba':
            self.radioButton_4.setChecked(True)

    def accept(self) -> None:
        super(NSettings, self).accept()
        dict_var_eg = {}
        dict_var = {}
        dict_path = {}
        if self.lineEdit.text() == '':
            dict_var['proxy'] = None
        else:
            dict_var['proxy'] = self.lineEdit.text()
        if self.lineEdit_2.text() == '':
            dict_var['match_filter'] = None
        else:
            dict_var['match_filter'] = self.lineEdit_2.text()
        if self.lineEdit_3.text() == '':
            dict_var['ratelimit'] = None
        else:
            dict_var['ratelimit'] = self.lineEdit_3.text()
        if self.lineEdit_4.text() == '':
            dict_path['home'] = None
        else:
            dict_path['home'] = self.lineEdit_4.text()
        if self.radioButton.isChecked():
            dict_var['format'] = 'b'
        elif self.radioButton_2.isChecked():
            dict_var['format'] = 'bv'
        elif self.radioButton_3.isChecked():
            dict_var['format'] = 'ba'
        elif self.radioButton_4.isChecked():
            dict_var['format'] = 'bv+ba'
        else:
            dict_var['format'] = 'b'
        dict_var['paths'] = dict_path
        dict_var_eg['settings'] = dict_var
        write_config_yml(dict_var_eg)
        self.close()


class MoreOT(QDialog, Ui_More_Dialog):
    def __init__(self, communication):
        super(MoreOT, self).__init__()
        self.setupUi(self)
        self.communication = communication
        self.communication.pushButton.setEnabled(True)
        self.checkBox_7.toggled.connect(self.setLineTextEnabled)
        opt = {
            'skip_download': True,
            'listsubtitles': True
        }
        self.nydl = SubThread(opt)
        self.nydl.outputWritten.connect(self.log_sub_langs)

    def log_sub_langs(self, p_str):
        text_cursor = QTextCursor(self.textBrowser.textCursor())
        text_cursor.movePosition(QtGui.QTextCursor.End)
        text_cursor.insertText('{}'.format(p_str))
        self.textBrowser.setTextCursor(text_cursor)
        self.textBrowser.ensureCursorVisible()

    def accept(self) -> None:
        super(MoreOT, self).accept()
        if self.checkBox.isChecked():
            self.communication.ytd_opt['writedescription'] = True
        if self.checkBox_2.isChecked():
            self.communication.ytd_opt['writeinfojson'] = True
        if self.checkBox_3.isChecked():
            self.communication.ytd_opt['getcomments'] = True
        if self.checkBox_4.isChecked():
            self.communication.ytd_opt['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'm4a',
            }]
        if self.checkBox_5.isChecked():
            self.communication.ytd_opt['writethumbnail'] = True
        if self.checkBox_6.isChecked():
            self.communication.ytd_opt['skip_download'] = True
        if self.checkBox_7.isChecked():
            self.communication.ytd_opt['writesubtitles'] = True
            if self.lineEdit.text() != '':
                self.communication.ytd_opt['subtitleslangs'] = self.lineEdit.text().split(',')
        self.communication.pushButton.setEnabled(False)
        self.communication.statusbar.showMessage("开始下载")
        self.communication.thread.start()

    def reject(self) -> None:
        super(MoreOT, self).reject()
        self.communication.pushButton.setEnabled(True)

    def setLineTextEnabled(self):
        if self.checkBox_7.isChecked():
            self.lineEdit.setEnabled(True)
        else:
            self.lineEdit.setEnabled(False)


class Main(QMainWindow, Ui_MainWindow):
    # define signal
    log_signal = Signal(str)
    err_log_signal = Signal(str)

    def __init__(self):
        super(Main, self).__init__()
        self.nsettings = None
        self.setupUi(self)
        self.links = []
        self.ytd_opt = {}
        self.flag = False
        self.thread = DownloadThread(
            communication=self,
            max_thread_number=1
        )
        self.log_signal.connect(self.log_signal_event)
        self.err_log_signal.connect(self.err_log_signal_event)
        self.actionyoutube_dl.triggered.connect(self.settingsDG)
        self.pushButton.clicked.connect(self.strat_download)
        self.show()

    def strat_download(self):
        self.pushButton.setEnabled(False)
        self.links = self.textEdit.toPlainText().split('\n')
        if self.links[0] == '':
            self.pushButton.setEnabled(True)
            self.err_log_signal.emit("textEdit can't null")
            raise Exception("Input Null")
        if self.radioButton.isChecked():
            self.statusbar.showMessage("开始下载")
            self.thread.start()
        elif self.radioButton_2.isChecked():
            self.statusbar.showMessage("选择更多选项")
            self.moreOptionsDG()
        else:
            self.err_log_signal.emit("出错了")
            raise Exception("Unknown err")
        # self.thread.wait()

    def log_signal_event(self, p_str):
        text_cursor = QTextCursor(self.textBrowser.textCursor())
        text_cursor.setPosition(0, QTextCursor.MoveAnchor)
        text_cursor.insertHtml('<p style="font-size:14px;color:green;">{}</p>'.format(p_str))
        text_cursor.insertHtml('<br>')
        self.textBrowser.setTextCursor(text_cursor)

    def err_log_signal_event(self, p_str):
        text_cursor = QTextCursor(self.textBrowser.textCursor())
        text_cursor.setPosition(0, QTextCursor.MoveAnchor)
        text_cursor.insertHtml('<p style="font-size:14px;color:red;">{}</p>'.format(p_str))
        text_cursor.insertHtml('<br>')
        self.textBrowser.setTextCursor(text_cursor)

    def settingsDG(self):
        self.nsettings = NSettings()
        self.nsettings.show()

    def moreOptionsDG(self):
        moreOT = MoreOT(self)
        moreOT.nydl.run(self.textEdit.toPlainText().split('\n'))
        moreOT.nydl.quit()
        moreOT.exec_()


if __name__ == "__main__":
    if not os.path.exists("./config"):
        os.mkdir("./config")
    if not os.path.isfile("./config/yt-dlp.yml"):
        rw_config.generate_config_yml()

    app = QApplication([])
    ui = Main()
    sys.exit(app.exec_())
