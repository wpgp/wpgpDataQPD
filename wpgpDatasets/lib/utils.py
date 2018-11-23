import os
import sys
import gzip
import logging
import platform
from hashlib import md5
from typing import Union
from pathlib import Path

from PyQt5.QtCore import QFileInfo
from qgis.core import QgsRasterLayer

from .errors import wpException



def md5_digest(file: Union[Path, str], gz=False)->str:
    """
     Returns the MD5 signature of the file. If the file is gz'ed, extract it contains before calculating.
    :param file: path to the file to generate the md5 signature.
    :param gz: If the file is compressed by the gz library.
    :return: MD5 hash string

    """
    file = Path(file)
    # if the file doesn't exist, return 0
    if not file.is_file():
        return '0'

    m = md5()
    if file.suffixes[-1].lower() == '.gz':
        gz = True

    # open/read the file with gzip module.
    if gz:
        m.update(gzip.open(file.as_posix()).read())
    else:
        m.update(file.open(mode='rb').read()).hex()

    return m.digest().hex()


def qgis3_add_raster_to_project(iface, raster_path: Path) -> bool:
    """
    Adds the Raster(raster_path) at the current open qgis project

    :type iface: qgis.gui.QgisInterface
    :type raster_path: Path
    """

    # TODO: Refactor: NV: Feels like incorrect usage of the APIs
    q_file_info = QFileInfo(raster_path.as_posix())
    q_base_name = q_file_info.baseName()
    q_raster_layer = QgsRasterLayer(q_file_info.filePath(), q_base_name)
    if q_raster_layer.isValid():
        iface.addRasterLayer(raster_path.as_posix(), raster_path.name)

    return True


def get_default_download_directory() -> str:
    system = platform.system()
    if system == 'Windows':
        if sys.version_info.major == 3:
            import winreg
        else:
            import __winreg as winreg

        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             r'Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders')
        path, _ = winreg.QueryValueEx(key, 'desktop')
    elif system == 'Linux':
        path = os.path.expanduser('~')

    # for mac? others? a safe default
    else:
        path = os.path.expanduser('~')

    path = Path(path).as_posix()  # make the path posix compliant
    return path


def are_same(this: Path, other: Path) -> bool:
    """Compare if two files are the same or not, using MD5 hash. True, are the same. False are different"""

    # this function reads the whole file into memory.
    # For big tiffs that would slow things considerably

    this_md5 = md5(this.read_bytes()).hexdigest()
    other_md5 = md5(other.read_bytes()).hexdigest()

    return this_md5 == other_md5


def resolve(name) -> Path:
    """Provided a name, returns <module_path>/name Path object."""
    dirname = Path(__file__).parent.parent
    return dirname.joinpath(name)


def has_internet() -> bool:
    import urllib.request as req
    from urllib.error import URLError
    target = 'http://www.google.com/'
    try:
        payload = req.urlopen(target).read(100)
    except URLError:
        return False

    # empty payload, means we can't go through
    if not len(payload):
        return False

    # Finally
    return True


BASE_ROOT = resolve('.')
CSV_SIGNATURE = md5_digest(BASE_ROOT / 'media/wpgpDatasets.csv.gz')
