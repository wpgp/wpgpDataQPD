# -*- coding: utf-8 -*-
__author__ = 'Nikolaos Ves'
__email__ = 'vesnikos@gmail.com'
__version__ = '0.1.0'

from qgis.gui import QgisInterface


# noinspection PyPep8Naming
def classFactory(iface: QgisInterface):  # pylint: disable=invalid-name
    """Load WpDatasets class from file WpDatasets."""

    # type iface: QgsInterface
    from .wp_datasets import WpDatasets
    return WpDatasets(iface)
  
