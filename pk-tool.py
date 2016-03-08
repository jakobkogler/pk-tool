import io
import os
import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QInputDialog, QMessageBox
from ui.mainwindow import Ui_MainWindow
from src.group_infos import GroupInfos
from src.settings import Settings
from dialog.settingsdialog import SettingsDialog
from src.git_interactions import GitInteractions
from dialog.gitdialog import GitDialog
from dialog.load_test_dialog import LoadTestDialog
from src.group import Group


class PkToolMainWindow(QMainWindow, Ui_MainWindow):
    """
    Application which allows to manage the csv-attendance-files from the pk-repo.
    """

    def __init__(self):
        """
        Initialize everything. Connect signals and slots. Read repo.
        """
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.group_infos = GroupInfos(repo_path='')
        self.csv_files = dict()

        self.settings = Settings()
        self.git_interactions = GitInteractions(self.settings, self.action_commit_and_push)

        self.file_combobox.currentIndexChanged.connect(self.load_group_data)
        self.group_combobox.currentIndexChanged.connect(self.populate_files)
        self.group_type_combobox.currentIndexChanged.connect(self.fill_group_names_combobox)
        self.console.returnPressed.connect(self.execute_console)
        self.action_new.triggered.connect(self.new_csv)
        self.action_add_student.triggered.connect(self.new_student)
        self.action_undo.triggered.connect(self.table_widget.undo_history)
        self.action_redo.triggered.connect(lambda: self.table_widget.undo_history(True))
        self.action_about.triggered.connect(self.show_about)
        self.action_settings.triggered.connect(self.open_settings)
        self.action_get_email.triggered.connect(self.get_email)
        self.action_commit_and_push.triggered.connect(self.open_git_dialog)
        self.action_load_test_applications.triggered.connect(self.open_load_test_mode)

        self.read_repo()
        if not self.settings.repo_path:
            self.open_settings()

    def show_about(self):
        """
        Opens a messagebox that shows informations about this application.
        """
        QMessageBox.about(self, 'About', 'https://github.com/jakobkogler/pk-tool')

    def open_settings(self):
        """
        Opens the settings-dialog, which allows to define the path to the pk-repo and the username.
        Updates everything after closing.
        """
        settings_dialog = SettingsDialog(self.settings)
        settings_dialog.exec_()
        self.read_repo()

    def open_git_dialog(self):
        """
        Open a dialog for commiting files to git.
        """
        if self.settings.use_git:
            git_dialog = GitDialog(self.git_interactions)
            git_dialog.exec_()

    def open_load_test_mode(self):
        """
        Opens a dialog that allows to load a registration file for a test and loads the test attendance csv-files.
        """
        load_test_mode_dialog = LoadTestDialog(self.settings)
        if load_test_mode_dialog.exec_():
            for group in load_test_mode_dialog.selected_groups:
                self.table_widget.group_infos.groups[group.name] = group
            self.group_type_combobox.setCurrentIndex(4)
            self.group_type_combobox.setDisabled(True)
            self.action_new.setDisabled(True)
            self.populate_files()

    def read_repo(self):
        """
        Read all important data from the pk-repo and fill all comboboxes accordingly
        """
        self.git_interactions.pull_and_react()
        self.group_infos = GroupInfos(repo_path=self.settings.repo_path)
        self.table_widget.connect(self.group_infos, self.action_undo, self.action_redo,
                                  self.get_csv_path, self.write_console)

        self.group_type_combobox.currentIndexChanged.disconnect()

        self.group_type_combobox.clear()
        self.group_type_combobox.addItems('Meine Alle Normal Fortgeschritten Tests'.split())

        self.group_type_combobox.currentIndexChanged.connect(self.fill_group_names_combobox)
        self.fill_group_names_combobox()

    def write_console(self, text):
        """
        Write a text to the console.
        """
        self.console_output.setText(text)

    def fill_group_names_combobox(self):
        """
        Populate the combobox with all the group names, that apply for the group type specified in the form.
        """
        type_index = self.group_type_combobox.currentIndex()

        if type_index == 0:
            tutor_name = self.settings.username
            group_names = self.group_infos.get_involved_groups(tutor_name)
        elif type_index < 4:
            allowed_types = []
            if type_index == 1:
                allowed_types = ['normal', 'fortgeschritten']
            elif type_index == 2:
                allowed_types = ['normal']
            elif type_index == 3:
                allowed_types = ['fortgeschritten']
            group_names = self.group_infos.get_group_names(allowed_types=allowed_types)
        else:
            path_to_folders = '{}/Anwesenheiten/Tests/'.format(self.settings.repo_path)
            group_names = sorted(os.listdir(path_to_folders))

        if group_names:
            self.group_combobox.currentIndexChanged.disconnect()

            self.group_combobox.clear()
            if type_index < 4:
                group_names.sort(key=lambda name: ('mo di mi do fr'.split().index(name[:2]), name[2:]))
                self.label_group.setText('Gruppe:')
                self.label_file.setText('Übung:')
            else:
                group_names.sort()
                self.label_group.setText('Testnummer:')
                self.label_file.setText('Slot:')

            self.group_combobox.addItems(group_names)

            self.group_combobox.currentIndexChanged.connect(self.populate_files)
            self.populate_files()

    def new_student(self):
        """
        Adds a new student to the current table.
        """
        matrikelnr, ok = QInputDialog.getText(self, 'Neuen Studenten hinzufügen', 'Matrikelnummer:')
        if ok and matrikelnr:
            self.table_widget.new_student(matrikelnr)

    def load_group_data(self):
        """
        Load all data for a specific group.
        It updates the names of the instructor and tutors and loads the last available csv-file for this group.
        """
        group_name = self.group_combobox.currentText()
        try:
            info = self.group_infos.get_group_info(group_name)
            self.label_instructor_name.setText(info.instructor)
            self.label_tutor1_name.setText(info.tutor1)
            self.label_tutor2_name.setText(info.tutor2)
        except KeyError:
            pass

        group = self.group_infos.get_group_info(group_name)
        if self.group_type_combobox.currentIndex() == 4:
            group = Group(self.file_combobox.currentText())

        self.table_widget.setup_table(group)
        if self.file_combobox.count():
            self.table_widget.load_csv_file(self.get_csv_path(), self.group_type_combobox.currentIndex() == 4)

    def get_email(self):
        """
        Determine all email-adresses from the current group and push the into the clipboard.
        """
        clipboard = QApplication.clipboard()
        group_name = self.group_combobox.currentText()
        group = self.group_infos.get_group_info(group_name)
        emails = [student.email for student in group.students]
        clipboard.setText(', '.join(emails))

    def get_csv_path(self):
        """
        Returns the path to the current csv-file
        """
        return self.csv_files[self.file_combobox.currentText()]

    def new_csv(self):
        """
        Generate a new csv-file for this group.
        """
        path_suggestion = '/Anwesenheiten/Uebungen/' + self.group_combobox.currentText() + '_ue' + \
                          str(len(self.file_combobox) + 1) + '.csv'

        directory = self.settings.repo_path
        path = QFileDialog.getSaveFileName(self, 'Neue CSV-Datei', directory + path_suggestion, '*.csv')[0]
        if not path:
            return

        if not path.endswith('.csv'):
            path += '.csv'

        with io.open(path, 'w', encoding='utf-8', newline='') as f:
            f.write('MatrNr;Gruppe;Kontrolle;Kommentar\n')

        self.populate_files()
        index = self.file_combobox.count() - 1
        for i in range(self.file_combobox.count()):
            if path.endswith(self.file_combobox.itemText(i)):
                index = i
        self.file_combobox.setCurrentIndex(index)

    def populate_files(self):
        """
        Finds the csv files for this group and populates the combobox
        """
        self.file_combobox.currentIndexChanged.disconnect()

        if (self.group_type_combobox.currentIndex() < 4):
            group_name = self.group_combobox.currentText()
            self.csv_files = self.get_csv_files(group_name)

            self.file_combobox.clear()
            self.file_combobox.addItems(sorted(self.csv_files.keys()))
            self.file_combobox.setCurrentIndex(self.file_combobox.count() - 1)
        else:
            test_folder = self.group_combobox.currentText()
            self.csv_files = self.get_test_files(test_folder)
            self.file_combobox.clear()
            self.file_combobox.addItems(sorted(self.csv_files.keys()))
            self.file_combobox.setCurrentIndex(0)

        self.file_combobox.currentIndexChanged.connect(self.load_group_data)
        self.load_group_data()

    def get_test_files(self, test_folder):
        path = self.settings.repo_path + '/Anwesenheiten/Tests/' + test_folder + '/'
        return {name.rstrip('.csv'): os.path.join(root, name)
                for root, dirs, files in os.walk(path)
                for name in files
                if name.endswith('.csv')}

    def get_csv_files(self, group_name):
        path = self.settings.repo_path + '/Anwesenheiten/Uebungen/'
        return {os.path.basename(root): os.path.join(root, name)
                for root, dirs, files in os.walk(path)
                for name in files
                if name.startswith(group_name)
                if name != 'placeholder'}

    def execute_console(self):
        """
        Executes a command from the console
        'name a' checks the attendance
        'name b' unchecks the attendance
        'name number' writes the adhoc-points
        'name other' writes a comment
        """
        try:
            commands = self.console.text().split(' ')
            identification, command = commands[0], ' '.join(commands[1:])
            index = self.table_widget.index_of_student(identification)
            if index >= 0:
                if command == 'a':
                    self.table_widget.get_checkbox(index).setCheckState(QtCore.Qt.Checked)
                elif command == 'b':
                    self.table_widget.get_checkbox(index).setCheckState(QtCore.Qt.Unchecked)
                elif command.isdigit():
                    self.table_widget.item(index, 4).setText(command)
                else:
                    self.table_widget.item(index, 5).setText(command)
            else:
                if index == -1:
                    error = 'Der Student "{}" wurde nicht gefunden.'
                else:
                    error = 'Mehrere Studenten treffen auf "{}" zu.'
                self.write_console('Error: ' + error.format(identification))
        except IndexError:
            pass

        self.console.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PkToolMainWindow()
    window.show()
    sys.exit(app.exec_())
