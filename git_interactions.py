# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'git_interactions.ui'
#
# Created by: PyQt5 UI code generator 5.5
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_GitDialog(object):
    def setupUi(self, GitDialog):
        GitDialog.setObjectName("GitDialog")
        GitDialog.resize(565, 268)
        self.gridLayout = QtWidgets.QGridLayout(GitDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.commit_message_label = QtWidgets.QLabel(GitDialog)
        self.commit_message_label.setObjectName("commit_message_label")
        self.gridLayout.addWidget(self.commit_message_label, 2, 0, 1, 1)
        self.button_box = QtWidgets.QDialogButtonBox(GitDialog)
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.button_box.setObjectName("button_box")
        self.gridLayout.addWidget(self.button_box, 4, 0, 1, 2)
        self.list_widget = QtWidgets.QListWidget(GitDialog)
        self.list_widget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.list_widget.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.list_widget.setObjectName("list_widget")
        self.gridLayout.addWidget(self.list_widget, 1, 0, 1, 1)
        self.explanation_label = QtWidgets.QLabel(GitDialog)
        self.explanation_label.setObjectName("explanation_label")
        self.gridLayout.addWidget(self.explanation_label, 0, 0, 1, 1)
        self.commit_message_line_edit = QtWidgets.QLineEdit(GitDialog)
        self.commit_message_line_edit.setObjectName("commit_message_line_edit")
        self.gridLayout.addWidget(self.commit_message_line_edit, 3, 0, 1, 1)

        self.retranslateUi(GitDialog)
        self.button_box.accepted.connect(GitDialog.accept)
        self.button_box.rejected.connect(GitDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(GitDialog)

    def retranslateUi(self, GitDialog):
        _translate = QtCore.QCoreApplication.translate
        GitDialog.setWindowTitle(_translate("GitDialog", "Commit und Push"))
        self.commit_message_label.setText(_translate("GitDialog", "<html><head/><body><p>Commit-Nachricht: <br>Als Platzhalter kann man &quot;{group_name}&quot; verwenden. <br>Dieser wird automatisch durch den Gruppennamen ersetzen.</p></body></html>"))
        self.explanation_label.setText(_translate("GitDialog", "<html><head/><body><p>Folgende geänderte Anwesenheitslisten wurden gefunden.<br>Markieren Sie diejenigen Dateien, die Sie ins PK-Repo commiten und pushen wollen. </p></body></html>"))
        self.commit_message_line_edit.setText(_translate("GitDialog", "Anwesenheit {group_name}"))

