# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/load_test_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_LoadTestDialog(object):
    def setupUi(self, LoadTestDialog):
        LoadTestDialog.setObjectName("LoadTestDialog")
        LoadTestDialog.resize(593, 226)
        self.gridLayout = QtWidgets.QGridLayout(LoadTestDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.line_edit_application_file = QtWidgets.QLineEdit(LoadTestDialog)
        self.line_edit_application_file.setObjectName("line_edit_application_file")
        self.gridLayout.addWidget(self.line_edit_application_file, 2, 1, 1, 1)
        self.label_application_file = QtWidgets.QLabel(LoadTestDialog)
        self.label_application_file.setObjectName("label_application_file")
        self.gridLayout.addWidget(self.label_application_file, 2, 0, 1, 1)
        self.label_folder_path = QtWidgets.QLabel(LoadTestDialog)
        self.label_folder_path.setObjectName("label_folder_path")
        self.gridLayout.addWidget(self.label_folder_path, 3, 0, 1, 1)
        self.line_edit_folder_path = QtWidgets.QLineEdit(LoadTestDialog)
        self.line_edit_folder_path.setObjectName("line_edit_folder_path")
        self.gridLayout.addWidget(self.line_edit_folder_path, 3, 1, 1, 1)
        self.button_folder_path = QtWidgets.QPushButton(LoadTestDialog)
        self.button_folder_path.setObjectName("button_folder_path")
        self.gridLayout.addWidget(self.button_folder_path, 3, 2, 1, 1)
        self.label_description = QtWidgets.QLabel(LoadTestDialog)
        self.label_description.setWordWrap(True)
        self.label_description.setObjectName("label_description")
        self.gridLayout.addWidget(self.label_description, 1, 0, 1, 3)
        self.button_application_file = QtWidgets.QPushButton(LoadTestDialog)
        self.button_application_file.setObjectName("button_application_file")
        self.gridLayout.addWidget(self.button_application_file, 2, 2, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton = QtWidgets.QPushButton(LoadTestDialog)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.gridLayout.addLayout(self.horizontalLayout, 4, 0, 1, 3)

        self.retranslateUi(LoadTestDialog)
        QtCore.QMetaObject.connectSlotsByName(LoadTestDialog)

    def retranslateUi(self, LoadTestDialog):
        _translate = QtCore.QCoreApplication.translate
        LoadTestDialog.setWindowTitle(_translate("LoadTestDialog", "Test-Modus"))
        self.label_application_file.setText(_translate("LoadTestDialog", "Pfad zur Anmeldungsliste: "))
        self.label_folder_path.setText(_translate("LoadTestDialog", "Pfad zum Ordner des Tests:"))
        self.button_folder_path.setText(_translate("LoadTestDialog", "Auswählen"))
        self.label_description.setText(_translate("LoadTestDialog", "Zum Bearbeiten der Anwesenheit benötigt das Programm eine aktuelle Anmeldungsliste. Diese kann unter TUWEL - Kurs Programmkonstruktion - Anmeldung zu Test X - Teilnehmer als \".txt\"-Datei heruntergeladen werden. \n"
"Ebenfalls wird der Pfad zum Ordner benötigt, in dem alle Anwesenheitslisten gespeichert werden sollen. "))
        self.button_application_file.setText(_translate("LoadTestDialog", "Auswählen"))
        self.pushButton.setText(_translate("LoadTestDialog", "Wechsle zum Test-Modus"))

