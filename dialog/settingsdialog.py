from PyQt5.QtWidgets import QDialog, QFileDialog
from ui.settings import Ui_SettingsDialog
from src.group_infos import GroupInfos

class SettingsDialog(QDialog, Ui_SettingsDialog):
    def __init__(self, settings):
        QDialog.__init__(self)
        self.setupUi(self)

        self.settings = settings
        pk_repo_path = self.settings.repo_path
        self.line_edit_repo_path.setText(pk_repo_path)
        self.update_username()

        if self.settings.use_git:
            self.git_interaction_check_box.setChecked(True)

        self.button_select_repo_path.clicked.connect(self.select_repo_path)
        self.buttonBox.accepted.connect(self.accept_settings)
        self.line_edit_repo_path.textChanged.connect(self.update_username)

    def update_username(self):
        group_infos = GroupInfos(repo_path=self.line_edit_repo_path.text())
        tutor_names = group_infos.tutor_names()

        self.username_combobox.clear()
        self.username_combobox.addItems(tutor_names)
        tutor_name = self.settings.username
        try:
            self.username_combobox.setCurrentIndex(tutor_names.index(tutor_name))
        except ValueError:
            pass

    def select_repo_path(self):
        pk_repo_path = QFileDialog.getExistingDirectory(self, 'Pfad zum PK-Repository', self.line_edit_repo_path.text(), QFileDialog.ShowDirsOnly)
        if pk_repo_path:
            self.line_edit_repo_path.setText(pk_repo_path)

    def accept_settings(self):
        self.settings.repo_path = self.line_edit_repo_path.text()
        self.settings.username = self.username_combobox.currentText()
        self.settings.use_git = self.git_interaction_check_box.isChecked()
