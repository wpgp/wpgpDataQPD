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
        self.urls = None
        self.download_folder = None
        self.total_filesize = 0
        self.progress_bar = progress_bar
        self.progress = 0

    def __pbar(self, x):
        # sizeof = sys.getsizeof(x)
        sizeof = len(x)
        # # self.progress_bar
        self.progress += sizeof / self.total_filesize * 100
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

    def run(self, urls: Union[str, Path], download_folder: Union[Path, str],):
        self.urls = list(map(Path, urls))  # remote paths
        self.download_folder = Path(download_folder)

        for url in self.urls:
            self.total_filesize = self.ftp.get_total_filesize(self.urls)
            local_file_name = self.download_folder / url.name
            self.ftp.download(url, local_file_name, callback=lambda x: self.__pbar(x))

        # HACK: Fill the pbar to full if it is not full at this stage.
        if self.progress_bar and self.progress_bar.value() < self.progress_bar.maximum():
            self.progress_bar.setValue(self.progress_bar.maximum())

        posix_path = local_file_name.as_posix()
        self.finished.emit(posix_path)
