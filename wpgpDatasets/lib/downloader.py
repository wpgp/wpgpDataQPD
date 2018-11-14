from pathlib import Path
from typing import Union
from PyQt5.QtCore import pyqtSignal, QObject, QCoreApplication
from PyQt5.QtWidgets import QProgressBar
# from qgis.core import QgsApplication

from .wpftp import wpFtp


class DownloadThread(QObject):
    finished = pyqtSignal(str)  # emits the LOCAL path (str) of the downloaded file

    def __init__(self, progress_bar: QProgressBar = None,
                 parent=None, **kwargs):

        super().__init__(parent=parent)

        self.ftp = wpFtp(server=kwargs['server'])
        self.url = None
        self.download_folder = None
        self.filename = None
        self.filesize = 0
        self.progress_bar = progress_bar
        self.progress = 0

    def __pbar(self, x):
        # sizeof = sys.getsizeof(x)
        sizeof = len(x)
        # # self.progress_bar
        self.progress += sizeof / self.filesize * 100
        if self.progress_bar is None:
            print(int(self.progress))
        else:
            if self.progress_bar.value() != self.progress:
                self.progress_bar.setValue(self.progress)
        try:
            QgsApplication.processEvents()
        except NameError:
            QCoreApplication.instance().processEvents()
        finally:
            pass

    def run(self, url: Union[str, Path], download_folder: Union[Path, str],):
        # start by calling the start method

        self.url = Path(url)  # remote path
        self.download_folder = Path(download_folder)
        self.filename = self.url.name
        self.filesize = self.ftp.get_filesilze(self.url)
        self.ftp.get_filesilze(self.url)

        local_file_name = self.download_folder / self.filename
        self.ftp.download(self.url, local_file_name, callback=lambda x: self.__pbar(x))

        # HACK: Fill the pbar to full if it is not full at this stage.
        if self.progress_bar and self.progress_bar.value() < self.progress_bar.maximum():
            self.progress_bar.setValue(self.progress_bar.maximum())

        posix_path = local_file_name.as_posix()
        self.finished.emit(posix_path)
