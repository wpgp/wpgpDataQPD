import configparser
import sys
import platform
from pathlib import Path
from typing import Union

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QFileDialog, QHeaderView, QMessageBox, QTreeWidgetItem

from qgis.gui import QgisInterface

from .lib import WpCsvParser
from .lib.utils import qgis3_add_raster_to_project, get_default_download_directory
from .lib.about_window import Ui_AboutDialog
from .lib.downloader import DownloadThread
from .lib.main_window import Ui_wpMainWindow

BASE_DIR = Path(__file__).parent

UI_FILE = BASE_DIR / 'ui' / 'main_window.ui'
assert UI_FILE.is_file()


class WpMainWindow(QtWidgets.QDialog, Ui_wpMainWindow):

    def __init__(self,  config: configparser.ConfigParser, iface: QgisInterface, parent=None):
        super(WpMainWindow, self).__init__(parent=parent)
        self.iface = iface
        self.config = config
        csv_file_gz = config['app']['csv_file_gz']
        self.csv_dataset = WpCsvParser(csv_file=csv_file_gz)

        self.setupUi(self)

        # Init stage
        self.setWindowTitle('World Pop Downloader')
        self._download_folder = None
        self.le_directory.setText(self._download_folder)
        self.le_directory.setPlaceholderText('/path/to/download/folder')

        self.pb_progressBar.setValue(0)
        icon = BASE_DIR / 'media' / 'wp.ico'
        self.setWindowIcon(QIcon(QPixmap(icon.as_posix())))

        # TREE WIDGET
        self.tree_widget.setColumnCount(2)
        self.tree_widget.setHeaderLabels(['Name', 'Description'])
        self.tree_widget.setSortingEnabled(True)
        self.tree_widget.header().setResizeContentsPrecision(500)
        self.tree_widget.header().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        if platform.system == 'Windows':
            self.tree_widget.header().resizeSections()

        # Add the data to the TreeWidget

        # Adding data
        self._add_items()
        # and sort
        self.tree_widget.sortItems(0, QtCore.Qt.AscendingOrder)

        # Connections
        self.btn_close.clicked.connect(self.close)
        self.btn_about.clicked.connect(self._about_dialog)
        self.btn_browse.clicked.connect(self._file_dialog)
        self.btn_download.clicked.connect(self._download)

    @property
    def isos(self):
        isos = self.csv_dataset.isos
        return isos

    def _after_download(self, local_file: str):
        self.btn_download.setEnabled(True)
        self.btn_close.setEnabled(True)
        if self.cbox_add_to_layer.isChecked():
            raster_path = Path(local_file)
            qgis3_add_raster_to_project(self.iface, raster_path=raster_path)

    def _download(self) -> Union[str, None]:

        # check if download folder is correct
        if self._download_folder is None:
            self._file_dialog()
        # user has selected 'Cancel' when instructed to select a folder
        if self._download_folder is None:
            return

        if not Path(self._download_folder).is_dir():
            self._file_dialog()
        if not Path(self._download_folder).is_dir():
            return

        # Grab and check it the URL  exists from the TreeWidget, then pass it at the download function

        item = self.tree_widget.selectedItems()
        if len(item) == 0:
            return
        item = item[0]

        # 3d index of the item contains the ftp path of the object to download
        URL = item.data(2, QtCore.Qt.DisplayRole)

        # Show warning that the user has not selected a valid selection.
        if URL is None:
            QMessageBox.information(self, 'Invalid Selection', 'Please select any of the child products to download.',
                                    QMessageBox.Ok)
            return

        self._do_download(URL)

    def _do_download(self, url: Union[str, Path]):

        self.btn_download.setEnabled(False)
        self.btn_close.setEnabled(False)

        dl = DownloadThread(progress_bar=self.pb_progressBar,
                            parent=self, server=self.config['ftp']['server'])
        dl.finished.connect(self._after_download)
        dl.run(url=url, download_folder=self._download_folder)

    def _add_items(self):
        for iso_idx, (iso_name, iso_iso3) in enumerate(self.isos):
            top_item = QTreeWidgetItem((iso_name, iso_iso3))
            products_per_iso = self.csv_dataset.products_per_iso(iso_iso3)
            _ = [QTreeWidgetItem(x) for x in products_per_iso]
            top_item.addChildren(_)
            self.tree_widget.addTopLevelItem(top_item)

    def _about_dialog(self):
        text = self.config['app']['about_text'] or 'Text not found!'
        png = BASE_DIR / 'media' / 'logo.png'  # BASE_DIR is Path object
        logo = QPixmap(png.as_posix(), "PNG")
        logo = logo.scaled(324, 186)  # 10% of the original size

        class About(Ui_AboutDialog):
            def __init__(self, parent):
                super().__init__(parent)
                self.setupUi(self)
                self.gridLayout.setSizeConstraint(3)  # set fixed size
                self.lbl_text.setWordWrap(True)

        about_dialog = About(self)
        about_dialog.lbl_text.setText(text)

        about_dialog.lbl_png.setText('')
        about_dialog.lbl_png.setPixmap(logo)

        # disable resizing
        about_dialog.setFixedSize(about_dialog.sizeHint())

        about_dialog.btn_ok.clicked.connect(lambda x: about_dialog.close())  # close on click
        about_dialog.exec()

    def _file_dialog(self):
        caption = 'Please select a folder to download the product'
        default_root = self._download_folder
        if default_root is None:
            default_root = get_default_download_directory()

        if not Path(default_root).is_dir():
            default_root = get_default_download_directory()

        # if user press cancel, it returns an Empty string
        dirname = QFileDialog().getExistingDirectory(self, caption=caption, directory=default_root,
                                                     options=QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
                                                             | QFileDialog.ReadOnly)

        if not dirname == '':
            self._download_folder = dirname

        self.le_directory.setText(dirname)
