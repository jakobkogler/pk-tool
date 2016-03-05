import re
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

        self.button_application_file.pressed.connect(self.load_application_list)
        self.button_folder_path.pressed.connect(self.load_folder_path)

    def load_application_list(self):
        path, _ = QFileDialog.getOpenFileName(self, 'Pfad zur Anmeldungsliste',
                                              self.line_edit_application_file.text(), 'Textdatei (*.txt)')
        self.line_edit_application_file.setText(path)

        pattern = re.compile(r'(Test\d+)')
        match = pattern.search(path)
        if match:
            test_name = match.group(1)
            path_to_folder = '{}/Anwesenheiten/Tests/{}'.format(self.settings.repo_path, test_name)
            if os.path.isdir(path_to_folder):
                self.line_edit_folder_path.setText(path_to_folder)

    def load_folder_path(self):
        path = QFileDialog.getExistingDirectory(self, 'Pfad zum Ordner des Tests',
                                                self.line_edit_folder_path.text(), QFileDialog.ShowDirsOnly)
        self.line_edit_folder_path.setText(path)

