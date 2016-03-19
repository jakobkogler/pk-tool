import os
import io
from PyQt5.QtWidgets import QDialog
from PyQt5 import QtCore
from ui.create_csv_dialog import Ui_CreateCSVDialog
from src.settings import Settings


class CreateCSVDialog(QDialog, Ui_CreateCSVDialog):
    """
    Dialog for creating new csv files for lessons
    """

    def __init__(self, settings: Settings, group_name: str):
        """
        Initialize everything.
        """
        QDialog.__init__(self)
        self.setupUi(self)

        self.settings = settings
        self.group_name = group_name
        self.selected_file = ''

        self.fill_folder()

        self.create_button.pressed.connect(self.create_file)

    def fill_folder(self):
        """Fill combobox with options for possible lessons"""
        path = self.settings.repo_path + '/Anwesenheiten/Uebungen/'
        all_lessons = {os.path.basename(root) for root, dirs, files in os.walk(path)}
        all_lessons.remove('')
        already_used_lessons = {os.path.basename(root) for root, dirs, files in os.walk(path)
                                for name in files if self.group_name in name}
        possible_lessons = sorted(all_lessons - already_used_lessons)
        self.file_combobox.addItems(possible_lessons)

    def create_file(self):
        """Create the CSV-File."""
        path = '{}/Anwesenheiten/Uebungen/{}/{}.csv'.format(self.settings.repo_path,
                                                            self.file_combobox.currentText(), self.group_name)

        if not os.path.exists(path):
            with io.open(path, 'w', encoding='utf-8', newline='') as f:
                f.write('MatrNr;Gruppe;Kontrolle;Kommentar\n')

        self.selected_file = self.file_combobox.currentText()
        self.close()
