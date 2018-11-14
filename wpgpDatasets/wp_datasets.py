# -*- coding: utf-8 -*-
import configparser
from pathlib import Path

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction

from .wp_datasets_dialog import WpMainWindow

# Global Variables
BASE_DIR = Path(__file__).parent  # Path object
CSV_FILE_GZ = Path(BASE_DIR / 'media' / 'wpgpDatasets.csv.gz')
INI_FILE = Path(BASE_DIR / 'config.ini')


class WpDatasets:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):

        self.iface = iface

        self.canvas = iface.mapCanvas()
        # initialize plugin directory
        self.plugin_dir = BASE_DIR


        # Class methods
        self.dialog = None

        # Declare instance attributes
        self.actions = []
        self.menu = u'&wp_datasets'
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'wpgpDatasets')
        self.toolbar.setObjectName(u'wpgpDatasets')

    def add_action(self, icon_path: str, text: str, callback, enabled_flag: bool = True,
                   add_to_menu: str = 'plugins', add_to_toolbar: bool = True,
                   status_tip: str = None, whats_this: str = None, parent=None):

        """
        Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            menu_action = None
            if add_to_menu == 'plugins':
                menu_action = self.iface.addPluginToMenu
            elif add_to_menu == 'rasters':
                menu_action = self.iface.addPluginToRasterMenu
            elif add_to_menu == 'vectors':
                menu_action = self.iface.addPluginToVectorMenu
            elif add_to_menu == 'web':
                menu_action = self.iface.addPluginToWebMenu
            if menu_action is None:
                raise AttributeError("add_to_menu should be a choice between plugins, rasters, vectors, web")

            menu_action(self.menu, action)

        self.actions.append(action)

        return action

    # noinspection PyPep8Naming
    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""
        # Required

        icon_path = BASE_DIR / 'media' / 'wp.ico'
        self.add_action(
                icon_path.as_posix(),
                text=u'Download WorldPop Global Dataset',
                callback=self.run,
                parent=self.iface.mainWindow(),
                status_tip='Download WorldPop Global Dataset'
        )

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        # Required
        for action in self.actions:
            self.iface.removePluginMenu(u'&wp_datasets', action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

    def run(self):
        """Run method that performs all the real work"""

        config = configparser.ConfigParser()
        config.read(INI_FILE.as_posix())
        config['app']['csv_file_gz'] = CSV_FILE_GZ.as_posix()

        self.dialog = WpMainWindow(iface=self.iface, config=config)

        self.dialog.show()
