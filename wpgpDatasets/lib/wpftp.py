# functions
import gzip
import os
import ftplib
import logging
import shutil

from io import BytesIO
from typing import Union
from pathlib import Path
from socket import gaierror, error
from configparser import ConfigParser
from tempfile import TemporaryDirectory


from .utils import md5_digest


class wpFtp(object):
    """
    Convenience Class for ftp operations.
    ftp = wpFtp(server,username,password)
    """
    # password = ftp_details.password
    # username = ftp_details.username
    # server = ftp_details.server
    timeout = 10  # ftp timeout, in seconds
    logger = logging.getLogger('library::wpFtp')
    logger.setLevel(logging.INFO)

    def __new__(cls, server='', username='anonymous', password='', config: ConfigParser = None):
        # if something goes wrong, return None
        try:
            ftp = ftplib.FTP(server, username, password, timeout=cls.timeout)
            cls.logger.info('FTP connection ok. Adress: %s, username: %s, password: %s' % (server, username, password))
        except gaierror:
            cls.logger.error('getaddrinfo failed. Target Server was: %s' % server)
            return None
        except ftplib.error_perm as e:
            cls.logger.error('Permision Error: %s' % str(e))
            return None
        except TimeoutError as e:
            cls.logger.error('Timeout Error. Is an FTP running at %s ?' % server)
            return None
        # socket.error
        except error as e:
            cls.logger.error('socket error. error was %s\n' % str(e))
            return None
        instance = super().__new__(cls)
        instance.ftp = ftp
        instance.username = username
        instance.password = password
        instance.server = server
        return instance

    def __init__(self, server='', username='anonymous', password='', config: ConfigParser = None):
        self.config = config
        self.ftp.sendcmd("TYPE i")  # switch to binary mode

    @property
    def csv_signature(self) -> str:
        bio = BytesIO()
        ftp_sig_file = self.config['ftp']['sig']
        p = Path(ftp_sig_file)
        self.ftp.retrbinary('RETR ' + p.as_posix(), bio.write)
        bio.seek(0)
        result = bio.read().decode('utf-8')
        result = result.strip()
        result = result.split(' ')[0]
        return result

    def __repr__(self):
        return type(self).__name__ + '@' + self.server

    def __del__(self):
        self.ftp.close()

    @property
    def newer_version_exists(self) -> bool:
        """
        Checks if a new version exists in the ftp server
        :return: bool
        """
        local_csv_file_gz = self.config['app']['csv_file_gz']
        local_csv_file_gz = Path(local_csv_file_gz)
        if not local_csv_file_gz.is_file():
            return True

        return self.csv_signature != md5_digest(local_csv_file_gz)

    def get_filesilze(self, ftp_absolute_path: Path) -> int or None:
        """ Returns the filesize from the ftp. Returns None if the file is not in the ftp """
        filesize = self.ftp.size(ftp_absolute_path.as_posix())
        # if response_code != '213':
        #     raise wpException("Not ok return code (%s), when tried to retrieve filesize" % response_code)
        if filesize >= 0:
            return filesize
        return None

    def download(self, from_ftp_absolute_path: Union[str, Path],
                 to_local_absolute_path: Union[str, Path], callback=None) -> Path:
        """ Download a file from the remote ftp, stores is locally.
        If file exists locally, it is removed beforehand.
        :return Path object to file.
        :rtype Path
        """
        from_ftp_absolute_path = Path(from_ftp_absolute_path)
        to_local_absolute_path = Path(to_local_absolute_path)

        if self.get_filesilze(from_ftp_absolute_path) is None:
            raise TypeError
        if to_local_absolute_path.is_file():
            os.remove(to_local_absolute_path.as_posix())
        with to_local_absolute_path.open('wb') as fp:
            def __callback(data):
                fp.write(data)
                if callback:
                    callback(data)

            self.ftp.retrbinary('RETR ' + from_ftp_absolute_path.as_posix(), __callback)

        return to_local_absolute_path

    def dl_wpgpDatasets(self)->Path:
        """
        Get the manifest file dl_wpgpDatasets from the ftp
        Compress it and save it in the path defined in the config.ini
        """

        remote_file = Path(self.config['ftp']['manifest'])
        local_file = Path(self.config['app']['csv_file_gz'])

        with TemporaryDirectory() as t_dir:
            output_t_file = Path(t_dir) / remote_file.name
            csv_file = self.download(remote_file, output_t_file)

            with csv_file.open(mode='rb') as f_in:
                with gzip.open(local_file, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)

        return local_file
