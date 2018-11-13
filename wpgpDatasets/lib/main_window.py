# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/main_window.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_wpMainWindow(object):
    def setupUi(self, wpMainWindow):
        wpMainWindow.setObjectName("wpMainWindow")
        wpMainWindow.resize(400, 330)
        wpMainWindow.setSizeGripEnabled(False)
        wpMainWindow.setModal(False)
        self.horizontalLayout = QtWidgets.QHBoxLayout(wpMainWindow)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.MainGrid = QtWidgets.QGridLayout()
        self.MainGrid.setContentsMargins(0, -1, -1, -1)
        self.MainGrid.setHorizontalSpacing(6)
        self.MainGrid.setVerticalSpacing(8)
        self.MainGrid.setObjectName("MainGrid")
        self.btn_browse = QtWidgets.QPushButton(wpMainWindow)
        self.btn_browse.setToolTip("")
        self.btn_browse.setObjectName("btn_browse")
        self.MainGrid.addWidget(self.btn_browse, 2, 3, 1, 1)
        self.cbox_add_to_layer = QtWidgets.QCheckBox(wpMainWindow)
        self.cbox_add_to_layer.setToolTip("")
        self.cbox_add_to_layer.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.cbox_add_to_layer.setText("")
        self.cbox_add_to_layer.setChecked(True)
        self.cbox_add_to_layer.setTristate(False)
        self.cbox_add_to_layer.setObjectName("cbox_add_to_layer")
        self.MainGrid.addWidget(self.cbox_add_to_layer, 3, 1, 1, 1)
        self.wp_header = QtWidgets.QLabel(wpMainWindow)
        self.wp_header.setToolTip("")
        self.wp_header.setScaledContents(True)
        self.wp_header.setObjectName("wp_header")
        self.MainGrid.addWidget(self.wp_header, 0, 0, 1, 1)
        self.btn_close = QtWidgets.QPushButton(wpMainWindow)
        self.btn_close.setToolTip("")
        self.btn_close.setObjectName("btn_close")
        self.MainGrid.addWidget(self.btn_close, 4, 3, 1, 1)
        self.pb_progressBar = QtWidgets.QProgressBar(wpMainWindow)
        self.pb_progressBar.setToolTip("")
        self.pb_progressBar.setProperty("value", 24)
        self.pb_progressBar.setObjectName("pb_progressBar")
        self.MainGrid.addWidget(self.pb_progressBar, 3, 2, 1, 2)
        self.btn_about = QtWidgets.QPushButton(wpMainWindow)
        self.btn_about.setToolTip("")
        self.btn_about.setObjectName("btn_about")
        self.MainGrid.addWidget(self.btn_about, 4, 0, 1, 1)
        self.btn_download = QtWidgets.QPushButton(wpMainWindow)
        self.btn_download.setToolTip("")
        self.btn_download.setObjectName("btn_download")
        self.MainGrid.addWidget(self.btn_download, 4, 2, 1, 1)
        self.tree_widget = QtWidgets.QTreeWidget(wpMainWindow)
        self.tree_widget.setToolTip("")
        self.tree_widget.setObjectName("tree_widget")
        self.tree_widget.headerItem().setText(0, "1")
        self.MainGrid.addWidget(self.tree_widget, 1, 0, 1, 4)
        self.lbl_add_to_layer = QtWidgets.QLabel(wpMainWindow)
        self.lbl_add_to_layer.setToolTip("")
        self.lbl_add_to_layer.setObjectName("lbl_add_to_layer")
        self.MainGrid.addWidget(self.lbl_add_to_layer, 3, 0, 1, 1)
        self.le_directory = QtWidgets.QLineEdit(wpMainWindow)
        self.le_directory.setToolTip("")
        self.le_directory.setObjectName("le_directory")
        self.MainGrid.addWidget(self.le_directory, 2, 0, 1, 3)
        self.horizontalLayout.addLayout(self.MainGrid)

        self.retranslateUi(wpMainWindow)
        QtCore.QMetaObject.connectSlotsByName(wpMainWindow)

    def retranslateUi(self, wpMainWindow):
        _translate = QtCore.QCoreApplication.translate
        wpMainWindow.setWindowTitle(_translate("wpMainWindow", "Dialog"))
        self.btn_browse.setText(_translate("wpMainWindow", "Browse"))
        self.wp_header.setText(_translate("wpMainWindow", "<html><head/><body><p><span style=\" font-size:16pt; font-weight:600;\">WorldPop Dataset</span></p></body></html>"))
        self.btn_close.setText(_translate("wpMainWindow", "Close"))
        self.btn_about.setText(_translate("wpMainWindow", "About"))
        self.btn_download.setText(_translate("wpMainWindow", "Download"))
        self.lbl_add_to_layer.setText(_translate("wpMainWindow", "Add downloaded file into Layer List"))

