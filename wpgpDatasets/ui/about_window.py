# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/about_window.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AboutDialog(object):
    def setupUi(self, AboutDialog):
        AboutDialog.setObjectName("AboutDialog")
        AboutDialog.resize(258, 81)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(AboutDialog.sizePolicy().hasHeightForWidth())
        AboutDialog.setSizePolicy(sizePolicy)
        self.gridLayout_2 = QtWidgets.QGridLayout(AboutDialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.lbl_text = QtWidgets.QLabel(AboutDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_text.sizePolicy().hasHeightForWidth())
        self.lbl_text.setSizePolicy(sizePolicy)
        self.lbl_text.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.lbl_text.setFrameShadow(QtWidgets.QFrame.Raised)
        self.lbl_text.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.lbl_text.setObjectName("lbl_text")
        self.gridLayout.addWidget(self.lbl_text, 0, 0, 1, 2)
        self.lbl_png = QtWidgets.QLabel(AboutDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_png.sizePolicy().hasHeightForWidth())
        self.lbl_png.setSizePolicy(sizePolicy)
        self.lbl_png.setObjectName("lbl_png")
        self.gridLayout.addWidget(self.lbl_png, 2, 0, 1, 2)
        self.btn_ok = QtWidgets.QPushButton(AboutDialog)
        self.btn_ok.setObjectName("btn_ok")
        self.gridLayout.addWidget(self.btn_ok, 3, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(AboutDialog)
        QtCore.QMetaObject.connectSlotsByName(AboutDialog)

    def retranslateUi(self, AboutDialog):
        _translate = QtCore.QCoreApplication.translate
        AboutDialog.setWindowTitle(_translate("AboutDialog", "Dialog"))
        self.lbl_text.setText(_translate("AboutDialog", "TextLabel"))
        self.lbl_png.setText(_translate("AboutDialog", "PNG_HOLDER"))
        self.btn_ok.setText(_translate("AboutDialog", "Ok"))

