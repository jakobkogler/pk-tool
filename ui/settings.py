# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settings.ui'
#
# Created by: PyQt5 UI code generator 5.5
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SettingsDialog(object):
    def setupUi(self, SettingsDialog):
        SettingsDialog.setObjectName("SettingsDialog")
        SettingsDialog.resize(565, 211)
        self.gridLayout = QtWidgets.QGridLayout(SettingsDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.username_combobox = QtWidgets.QComboBox(SettingsDialog)
        self.username_combobox.setObjectName("username_combobox")
        self.gridLayout.addWidget(self.username_combobox, 1, 1, 1, 1)
        self.line_edit_repo_path = QtWidgets.QLineEdit(SettingsDialog)
        self.line_edit_repo_path.setObjectName("line_edit_repo_path")
        self.gridLayout.addWidget(self.line_edit_repo_path, 0, 1, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(SettingsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 4, 0, 1, 3)
        self.button_select_repo_path = QtWidgets.QPushButton(SettingsDialog)
        self.button_select_repo_path.setObjectName("button_select_repo_path")
        self.gridLayout.addWidget(self.button_select_repo_path, 0, 2, 1, 1)
        self.label_repo_path = QtWidgets.QLabel(SettingsDialog)
        self.label_repo_path.setObjectName("label_repo_path")
        self.gridLayout.addWidget(self.label_repo_path, 0, 0, 1, 1)
        self.label_username = QtWidgets.QLabel(SettingsDialog)
        self.label_username.setObjectName("label_username")
        self.gridLayout.addWidget(self.label_username, 1, 0, 1, 1)
        self.git_interaction_check_box = QtWidgets.QCheckBox(SettingsDialog)
        self.git_interaction_check_box.setObjectName("git_interaction_check_box")
        self.gridLayout.addWidget(self.git_interaction_check_box, 2, 0, 1, 3)

        self.retranslateUi(SettingsDialog)
        self.buttonBox.accepted.connect(SettingsDialog.accept)
        self.buttonBox.rejected.connect(SettingsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SettingsDialog)

    def retranslateUi(self, SettingsDialog):
        _translate = QtCore.QCoreApplication.translate
        SettingsDialog.setWindowTitle(_translate("SettingsDialog", "Einstellungen"))
        self.button_select_repo_path.setText(_translate("SettingsDialog", "Auswählen"))
        self.label_repo_path.setText(_translate("SettingsDialog", "Pfad zum PK-Repo:"))
        self.label_username.setText(_translate("SettingsDialog", "Username:"))
        self.git_interaction_check_box.setText(_translate("SettingsDialog", "Git-Interaktionen aktivieren (experimentell)"))

