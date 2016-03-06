import os
from PyQt5.QtWidgets import QDialog, QFileDialog
from ui.load_test_dialog import Ui_LoadTestDialog
from src.settings import Settings


class LoadTestDialog(QDialog, Ui_LoadTestDialog):
    """
    Dialog to add and commit files to the pk-repo.
    """

    def __init__(self, settings: Settings):
        """
        Initialize everything.
        """
        QDialog.__init__(self)
        self.setupUi(self)

        self.settings = settings
        self.path_to_folders = '{}/Anwesenheiten/Tests/'.format(self.settings.repo_path)
        self.test_folders = sorted(os.listdir(self.path_to_folders))
        self.folder_combobox.addItems(self.test_folders)

        self.button_application_file.pressed.connect(self.find_application_list)
        self.button_load_application_list.pressed.connect(self.load_application_list)

    def find_application_list(self):
        path, _ = QFileDialog.getOpenFileName(self, 'Pfad zur Anmeldungsliste',
                                              self.line_edit_application_file.text(), 'Textdatei (*.txt)')
        self.line_edit_application_file.setText(path)

        for idx, folder in enumerate(self.test_folders):
            if folder in path:
                self.folder_combobox.setCurrentIndex(idx)
                break

    def load_application_list(self):
        pass