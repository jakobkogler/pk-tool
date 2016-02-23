import io
import os
import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QInputDialog, QMessageBox
from ui.mainwindow import Ui_MainWindow
from src.group_infos import GroupInfos
from src.settings import Settings
from dialog.settingsdialog import SettingsDialog
from dialog.gitdialog import GitDialog

use_git = True
try:
    import git
except ImportError:
    use_git = False


class PkToolMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, use_git):
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.group_infos = GroupInfos(repo_path='')
        self.csv_files = dict()

        self.table_widget.set_action_undo(self.action_undo)
        self.table_widget.set_action_redo(self.action_redo)
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

        self.settings = Settings()
        self.settings.use_git = self.settings.use_git and use_git

        self.try_reading_repo()

    def try_git_pull(self):
        pk_repo_path = self.settings.repo_path
        if pk_repo_path and self.settings.use_git:
            try:
                self.repo = git.Repo(pk_repo_path)
                o = self.repo.remotes.origin
                info = o.pull()[0]

                if info.flags & (git.Fetchinfo.ERROR | git.Fetchinfo.REJECTED):
                    self.settings.use_git = False
            except:
                self.settings.use_git = False
            if not self.settings.use_git:
                QMessageBox.about(self, 'Fehler', 'Es gab einen Fehler beim Pullen des Git-Repos. \n'
                                  'Git-Interaktionen wurden für diese Session ausgeschaltet.')

        if self.settings.use_git:
            self.action_commit_and_push.setEnabled(True)
        else:
            self.action_commit_and_push.setDisabled(True)

    def get_changed_or_untracked_files(self):
        self.repo.head.reset(index=True, working_tree=False)
        files = self.repo.untracked_files + [info.a_path for info in self.repo.index.diff(None)]
        return files

    def show_about(self):
        QMessageBox.about(self, 'About', 'https://github.com/jakobkogler/pk-tool')

    def open_settings(self):
        """Opens the settings-dialog, which allows to define the path to the pk-repo and the username
        Updates everything after closing.
        """
        settings_dialog = SettingsDialog(self.settings)
        settings_dialog.exec_()

        self.try_reading_repo()

    def try_reading_repo(self):
        self.try_git_pull()
        self.group_infos = GroupInfos(repo_path=self.settings.repo_path)
        self.table_widget.set_group_infos(self.group_infos)

        self.group_type_combobox.currentIndexChanged.disconnect()

        self.group_type_combobox.clear()
        self.group_type_combobox.addItems('Meine Alle Normal Fortgeschritten'.split())

        self.group_type_combobox.currentIndexChanged.connect(self.fill_group_names_combobox)
        self.fill_group_names_combobox()

    def fill_group_names_combobox(self):
        """Populate the combobox with all the group names,
        that apply for the group type specified in the form.
        """
        type_index = self.group_type_combobox.currentIndex()

        if type_index == 0:
            tutor_name = self.settings.username
            group_names = self.group_infos.get_involved_groups(tutor_name)
        else:
            allowed_types = []
            if type_index == 1:
                allowed_types = ['normal', 'fortgeschritten']
            elif type_index == 2:
                allowed_types = ['normal']
            elif type_index == 3:
                allowed_types = ['fortgeschritten']
            group_names = self.group_infos.get_group_names(allowed_types=allowed_types)

        self.group_combobox.currentIndexChanged.disconnect()

        self.group_combobox.clear()
        group_names.sort(key=lambda name: ('mo di mi do fr'.split().index(name[:2]), name[2:]))
        self.group_combobox.addItems(group_names)

        self.group_combobox.currentIndexChanged.connect(self.populate_files)
        self.populate_files()

    def new_student(self):
        matrikelnr, ok = QInputDialog.getText(self, 'Neuen Studenten hinzufügen', 'Matrikelnummer:')
        if ok and matrikelnr:
            self.table_widget.new_student(matrikelnr)

    def load_group_data(self):
        """Load all data for a specific group.
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
        self.table_widget.prepair_table(group)
        if self.file_combobox.count():
            self.table_widget.load_csv_file(self.get_csv_path())

    def get_email(self):
        clipboard = QApplication.clipboard(self)
        group_name = self.group_combobox.currentText()
        group = self.group_infos.get_group_info(group_name)
        emails = [student.email for student in group.students]
        clipboard.setText(', '.join(emails))

    def get_csv_path(self):
        """Returns the path to the csv-file
        """
        return self.csv_files[self.file_combobox.currentText()]

    def new_csv(self):
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
        """Finds the csv files for this group and populates the combobox
        """

        self.file_combobox.currentIndexChanged.disconnect()

        group_name = self.group_combobox.currentText()
        path = self.settings.repo_path + '/Anwesenheiten/Uebungen/'
        self.csv_files = {os.path.join(os.path.basename(root), name): os.path.join(root, name)
                          for root, dirs, files in os.walk(path)
                          for name in files
                          if name.startswith(group_name)}

        self.file_combobox.clear()
        self.file_combobox.addItems(sorted(self.csv_files.keys()))
        self.file_combobox.setCurrentIndex(self.file_combobox.count() - 1)

        self.file_combobox.currentIndexChanged.connect(self.load_group_data)
        self.load_group_data()

    def execute_console(self):
        """Executes a command from the console
        'name a' checks the attendance
        'name b' unchecks the attendance
        'name number' writes the adhoc-points
        'name other' writes a comment
        """
        try:
            commands = self.console.text().split(' ')
            identification, command = commands[0], ' '.join(commands[1:])
            index = self.find_index(identification)
            if isinstance(index, int):
                if command == 'a':
                    self.table_widget.get_checkbox(index).setCheckState(QtCore.Qt.Checked)
                elif command == 'b':
                    self.table_widget.get_checkbox(index).setCheckState(QtCore.Qt.Unchecked)
                elif command.isdigit():
                    self.table_widget.item(index, 4).setText(command)
                else:
                    self.table_widget.item(index, 5).setText(command)
            else:
                if len(index) == 0:
                    error = 'Der Student "{}" wurde nicht gefunden.'
                else:
                    error = 'Mehrere Studenten treffen auf "{}" zu.'
                self.write_console('Error: ' + error.format(identification))
        except IndexError:
            pass

        self.console.clear()

    def write_console(self, text):
        self.console_output.setText(text)

    def open_git_dialog(self):
        if self.settings.use_git:
            git_dialog = GitDialog(self.repo, self.get_changed_or_untracked_files())
            git_dialog.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PkToolMainWindow(use_git)
    window.show()
    sys.exit(app.exec_())
