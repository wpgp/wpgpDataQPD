import platform
import warnings
import gzip
from itertools import chain
from pathlib import Path
from typing import Any, Dict, List, Tuple, Union
import csv

import numpy as np

# Numpy version numbers
np_major, np_minor, np_micro = map(int, np.version.version.split('.'))


class WpCsvParser(object):

    def __init__(self, csv_file=Union[str, Path], **kwargs):

        self._csv_path = Path(csv_file)
        self.delimiter = kwargs.get('delimiter') or ','

        # Encoding
        # If provided use that, otherwise use the following heuristics
        self.encoding = kwargs.get('encoding')
        if self.encoding is None:
            if self.os == 'Windows':
                self.encoding = 'oem'  # only available from python 3.6 onwards

        # if still None default to 'utf-8'
        if self.encoding is None:
            self.encoding = 'unicode_escape'

        # Private
        self._df = None
        self._isos = None
        self._indexes = None

    @property
    def csv_path(self) -> str:
        """ The _obsolete_ path to the CSV file including the file extension. Posix compliant """
        res = self._csv_path
        res = Path(res)
        if not res.is_file():
            raise AttributeError('CSV file not found. Folder = %s' % res.parent)
        res = Path(res).as_posix()
        return res

    @property
    def df(self) -> np.ndarray:
        """
        Returns a numpy.ndarray that holds the data.
        Lazy loading.
        """
        if self._df is None:
            delimiter = self.delimiter
            encoding = self.encoding
            lines = []
            with gzip.open(self.csv_path, mode='rt', encoding=encoding) as fh:

                reader = csv.reader(fh, dialect='excel')
                for row_id, row in enumerate(reader):
                    lines.append(row)
                df = np.array(lines, dtype=object)

            self._df = df
        return self._df

    @property
    def isos(self) -> List[Tuple[str, str]]:
        """
        Returns a list of unique iso/name values. Filters out ISO3 that are more than 3 chars long.
        (e.g. IND_correct)
        :return: List(List(iso,english_name))
        """

        if self._isos is None:
            indexes = self.indexes
            idx_iso3 = indexes['idx_iso3']
            idx_name_english = indexes['idx_name_english']
            df = self.df[1:]  # remove header, work only with data
            isos = df[:, [idx_name_english, idx_iso3]].astype(str)

            # filter the uniques per row
            # axis parameter was introduced from  numpy 1.13 onwards. Unfortunately QGIS 3.0 - Standalone - ships with
            # numpy 1.12.
            if int(np_minor) >= 13:
                isos = np.unique(isos, axis=0)
            else:
                # iterates through the isos and filters the uniques keeping a records on how many rows under
                # that iso exist.
                from collections import Counter
                c = Counter()
                for k, v in isos:
                    c.update(('%s+%s' % (k, v),))  # Damn you python for making me do this
                isos = np.array(list(map(lambda x: x.split('+'), list(c.keys()))))

            # remove double quotes from strings if any
            # ['"ARM"', '"Armenia"'] -> ['ARM', 'Armenia']
            isos = list(map(lambda row: [str(x).replace('"', '') for x in row], isos))

            # remove the ISOs that are more than 3 letters long.
            # eg. IND_correct
            condition = np.char.str_len(np.array(isos)[:, 1]) == 3  # the 2nd column of each row should be 3 chars long
            isos = np.array(isos)[condition]

            self._isos = isos.copy().tolist()

        return self._isos

    @property
    def indexes(self) -> Dict[str, int]:
        """ Build the row Indexess. Each index represent the column order of the said attribute."""

        if self._indexes is None:
            indexes = dict()
            header = self.df[0]
            idx_id = np.where(header == 'ID')[0][0]
            idx_iso3 = np.where(header == 'ISO3')[0][0]
            idx_name_english = np.where(header == 'Country')[0][0]
            idx_cvt_name = np.where(header == 'Covariate')[0][0]
            idx_path_to_raster = np.where(header == 'PathToRaster')[0][0]
            idx_description = np.where(header == 'Description')[0][0]

            # column position in the csv
            indexes['idx_iso3'] = idx_iso3
            indexes['idx_name_english'] = idx_name_english
            indexes['idx_cvt_name'] = idx_cvt_name
            indexes['idx_path_to_raster'] = idx_path_to_raster
            indexes['idx_description'] = idx_description
            indexes['idx_id'] = idx_id

            # for k, v in indexes.items():
            #     print(k, v)

            self._indexes = indexes.copy()

        return self._indexes

    def products_per_iso(self, iso: str) -> Union[Tuple[list, list, list], List[Tuple[Any, Any, Any]]]:
        # Name, Description, FTP_PATH

        _df = self.df[1:, :]
        idx_iso = self.indexes['idx_iso3']
        idx = np.where(_df[:, idx_iso] == iso)
        if len(idx[0]) == 0:
            iso = '"' + iso + '"'
            idx = np.where(_df[:, idx_iso] == iso)
        if len(idx[0]) == 0:
            warnings.warn('Warning, no products where found for this ISO. Check spelling')
            return [], [], []

        idx_name, idx_description, path_to_raster_idx, = self.indexes['idx_cvt_name'], \
                                                         self.indexes['idx_description'], \
                                                         self.indexes['idx_path_to_raster']

        per_iso_entries = _df[idx][:, [idx_name, idx_description, path_to_raster_idx]]
        name, description, path_to_raster = np.split(per_iso_entries, 3, axis=1)

        # clean double quotes if any
        name = np.core.defchararray.replace(name.astype(str), '"', '')
        path_to_raster = np.core.defchararray.replace(path_to_raster.astype(str), '"', '')
        description = np.core.defchararray.replace(description.astype(str), '"', '')

        name, description, path = list(chain.from_iterable(name.tolist())), \
                                  list(chain.from_iterable(description.tolist())), \
                                  list(chain.from_iterable(path_to_raster.tolist())),

        return list(zip(name, description, path))

    @property
    def os(self):
        return platform.system()
