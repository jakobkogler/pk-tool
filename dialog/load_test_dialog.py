import os
import re
import io
from PyQt5.QtWidgets import QDialog, QFileDialog
from ui.load_test_dialog import Ui_LoadTestDialog
from src.settings import Settings
from src.group_infos import GroupInfos, Student
from src.group import Group


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
        self.groups = []
        self.selected_groups = []

        self.button_application_file.pressed.connect(self.find_application_list)
        self.button_load_test_slots.pressed.connect(self.load_test_slots)
        self.line_edit_application_file.textChanged.connect(self.load_groups)

    def find_application_list(self):
        path, _ = QFileDialog.getOpenFileName(self, 'Pfad zur Anmeldungsliste',
                                              self.line_edit_application_file.text(), 'Textdatei (*.txt)')
        self.line_edit_application_file.setText(path)

        for idx, folder in enumerate(self.test_folders):
            if folder.lower() in ''.join(c for c in path.lower() if c != ' '):
                self.folder_combobox.setCurrentIndex(idx)
                break

    def load_groups(self):
        path = self.line_edit_application_file.text()

        test_name_regex = re.compile(r'[\w\s]+\s\d\d:\d\d')
        student_regex = re.compile(r'\s+[+✔]\s+(\D+)\s(\d+)\s(.*)\s?')

        self.groups = []
        for part in GroupInfos.split_file_into_parts(path, test_name_regex):
            group_name = test_name_regex.search(part[0]).group(0)
            group = Group(group_name, 'Test')

            for line in part[1:]:
                match = student_regex.search(line)
                if match:
                    group.add_student(Student(*([match.group(i) for i in range(1, 4)] + [group_name])))

            self.groups.append(group)

        group_names = [group.name for group in self.groups]
        self.list_groups.clear()
        self.list_groups.addItems(group_names)

    def load_test_slots(self):
        self.selected_groups = [self.groups[idx.row()] for idx in self.list_groups.selectedIndexes()]

        for group in self.selected_groups:
            group_name = group.name
            group_name = ''.join(c for c in group_name.lower() if 'a' <= c <= 'z')
            time_regex = re.compile(r'(\d\d):\d\d')
            match = time_regex.search(group.name)
            if match:
                group_name += match.group(1)

            path = '{repo}/Anwesenheiten/Tests/{folder}/{group_name}.csv'.format(repo=self.settings.repo_path,
                                                                                 folder=self.folder_combobox.currentText(),
                                                                                 group_name=group_name)
            data = self.load_file(path)

            for student in group.students:
                for entry in data:
                    if entry[0] == student.matrikelnr:
                        break
                else:
                    data.append((student.matrikelnr, group_name, 'ab', ''))

            self.export_csv(path, data)

        self.close()

    def load_file(self, path):
        data = []
        try:
            with open(path, 'r', encoding='utf-8') as file:
                next(file)  # skip header
                for line in file:
                    matrikelnr, group_name, attendance, comment = line.strip().split(';')
                    data.append((matrikelnr, group_name, attendance, comment))
        except FileNotFoundError:
            pass

        return data

    def export_csv(self, path, data):
        """
        Write the opened table to a csv-file
        """
        with io.open(path, 'w', encoding='utf-8', newline='') as f:
            f.write('MatrNr;Gruppe;Kontrolle;Kommentar\n')
            for d in data:
                f.write('{};{};{};{}\n'.format(*d))
