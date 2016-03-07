# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'load_test_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_LoadTestDialog(object):
    def setupUi(self, LoadTestDialog):
        LoadTestDialog.setObjectName("LoadTestDialog")
        LoadTestDialog.resize(593, 583)
        self.gridLayout = QtWidgets.QGridLayout(LoadTestDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.list_groups = QtWidgets.QListWidget(LoadTestDialog)
        self.list_groups.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.list_groups.setObjectName("list_groups")
        self.gridLayout.addWidget(self.list_groups, 5, 0, 1, 3)
        self.folder_combobox = QtWidgets.QComboBox(LoadTestDialog)
        self.folder_combobox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.folder_combobox.setObjectName("folder_combobox")
        self.gridLayout.addWidget(self.folder_combobox, 3, 1, 1, 1)
        self.line_edit_application_file = QtWidgets.QLineEdit(LoadTestDialog)
        self.line_edit_application_file.setObjectName("line_edit_application_file")
        self.gridLayout.addWidget(self.line_edit_application_file, 2, 1, 1, 1)
        self.label_application_file = QtWidgets.QLabel(LoadTestDialog)
        self.label_application_file.setObjectName("label_application_file")
        self.gridLayout.addWidget(self.label_application_file, 2, 0, 1, 1)
        self.label_folder_path = QtWidgets.QLabel(LoadTestDialog)
        self.label_folder_path.setObjectName("label_folder_path")
        self.gridLayout.addWidget(self.label_folder_path, 3, 0, 1, 1)
        self.button_application_file = QtWidgets.QPushButton(LoadTestDialog)
        self.button_application_file.setObjectName("button_application_file")
        self.gridLayout.addWidget(self.button_application_file, 2, 2, 1, 1)
        self.button_load_test_slots = QtWidgets.QPushButton(LoadTestDialog)
        self.button_load_test_slots.setObjectName("button_load_test_slots")
        self.gridLayout.addWidget(self.button_load_test_slots, 6, 0, 1, 3)
        self.label_description = QtWidgets.QLabel(LoadTestDialog)
        self.label_description.setWordWrap(True)
        self.label_description.setObjectName("label_description")
        self.gridLayout.addWidget(self.label_description, 1, 0, 1, 3)
        self.label_load_explanation = QtWidgets.QLabel(LoadTestDialog)
        self.label_load_explanation.setWordWrap(True)
        self.label_load_explanation.setObjectName("label_load_explanation")
        self.gridLayout.addWidget(self.label_load_explanation, 4, 0, 1, 3)

        self.retranslateUi(LoadTestDialog)
        QtCore.QMetaObject.connectSlotsByName(LoadTestDialog)

    def retranslateUi(self, LoadTestDialog):
        _translate = QtCore.QCoreApplication.translate
        LoadTestDialog.setWindowTitle(_translate("LoadTestDialog", "Laden der Anmeldungsliste für einen Test"))
        self.label_application_file.setText(_translate("LoadTestDialog", "Pfad zur Anmeldungsliste: "))
        self.label_folder_path.setText(_translate("LoadTestDialog", "Test-Name:"))
        self.button_application_file.setText(_translate("LoadTestDialog", "Auswählen"))
        self.button_load_test_slots.setText(_translate("LoadTestDialog", "Lade die ausgewählten Slots"))
        self.label_description.setText(_translate("LoadTestDialog", "Zum Bearbeiten der Anwesenheit benötigt das Programm eine aktuelle Anmeldungsliste. Diese kann unter TUWEL - Kurs Programmkonstruktion - Anmeldung zu Test X - Teilnehmer als \".txt\"-Datei heruntergeladen werden. \n"
"Ebenfalls wird der Testname (Testnummer) benötigt. "))
        self.label_load_explanation.setText(_translate("LoadTestDialog", "Wählen Sie die Testslots aus, die Sie laden möchten. Von diesen werden sofort csv-Dateien erstellt, die Sie danach mit diesem Programm bearbeiten können. \n"
"Falls außer ihnen auch noch andere Personen die Anwesenheit der Studenten kontroliert, sollten Sie nur ihre Testslots laden. Oder zumindest die erstellten csv-Dateien nach dem Erstellen sofort mit Git commiten und pushen. "))

