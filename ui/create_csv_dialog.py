# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'create_csv_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_CreateCSVDialog(object):
    def setupUi(self, CreateCSVDialog):
        CreateCSVDialog.setObjectName("CreateCSVDialog")
        CreateCSVDialog.resize(593, 111)
        self.gridLayout = QtWidgets.QGridLayout(CreateCSVDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(CreateCSVDialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.file_combobox = QtWidgets.QComboBox(CreateCSVDialog)
        self.file_combobox.setObjectName("file_combobox")
        self.gridLayout.addWidget(self.file_combobox, 0, 1, 1, 1)
        self.create_button = QtWidgets.QPushButton(CreateCSVDialog)
        self.create_button.setObjectName("create_button")
        self.gridLayout.addWidget(self.create_button, 1, 0, 1, 2)

        self.retranslateUi(CreateCSVDialog)
        QtCore.QMetaObject.connectSlotsByName(CreateCSVDialog)

    def retranslateUi(self, CreateCSVDialog):
        _translate = QtCore.QCoreApplication.translate
        CreateCSVDialog.setWindowTitle(_translate("CreateCSVDialog", "Erzeuge ein neues CSV-Datei für eine Übung"))
        self.label.setText(_translate("CreateCSVDialog", "Für welche Übung möchten Sie eine CSV-Datei erzeugen?"))
        self.create_button.setText(_translate("CreateCSVDialog", "Erzeuge CSV-Datei"))

