import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QTableWidgetItem, QFileDialog, QCheckBox, QWidget, \
    QHBoxLayout, QMessageBox
from PyQt5 import QtCore
from PyQt5.QtCore import QSettings
from mainwindow import Ui_MainWindow
from settings import Ui_SettingsDialog
import os
import re
import io
from collections import namedtuple
from _datetime import datetime

GroupInfos = namedtuple('GroupInfos', 'instructor, tutor1, tutor2')
Group = namedtuple('Group', 'name type students')
Student = namedtuple('Student', 'name matrikelnr email group_name')


class PkToolMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.group_infos = dict()
        self.groups = dict()

        self.settings = QSettings('settings.ini', QSettings.IniFormat)
        pk_repo_path = self.settings.value('Path/pk_repo', '')
        if pk_repo_path:
            self.get_group_infos()
            self.read_group_files()

        # self.find_files()
        # self.current_group_idx = 0
        # self.write_lock = False
        # if self.name_files:
        #     self.open_file(0)
        # else:
        #     QMessageBox().about(self, 'Keine Teilnehmerlisten gefunden',
        #                         '\n'.join(['Um das Programm verwenden zu können, müssen Sie zuerst die Teilnehmerlisten',
        #                                    'von Tuwel downloaden und in dieses Verzeichnis kopieren. Die findet man unter',
        #                                    '"Programmkonstruktion - Anmeldungen - Übungsanmeldung (Normale Gruppen) - Teilnehmer/innen". ',
        #                                    'Dort bei den jeweiligen Gruppen die .txt (z.B. 185.A79...Überblick.txt) nehmen.']))
        #
        # self.group_combobox.currentIndexChanged.connect(self.open_file)
        # self.action_export.triggered.connect(lambda: self.write_file(savefile=False))
        # self.table_widget.cellChanged.connect(lambda: self.write_file(savefile=True))
        # self.console.returnPressed.connect(self.execute_console)
        # self.action_new.triggered.connect(lambda: self.open_file(self.group_combobox.currentIndex(), new=True))
        # self.action_add_student.triggered.connect(self.add_row)

        self.action_settings.triggered.connect(self.open_settings)
        self.group_type_combobox.currentIndexChanged.connect(self.fill_group_names_combobox)
        self.group_combobox.currentIndexChanged.connect(self.populate_lesson_numbers)
        self.lesson_combobox.currentIndexChanged.connect(self.load_group_data)

    def open_settings(self):
        """Opens the settings-dialog, which allows to define the path to the pk-repo and the username
        Updates everything after closing.
        """
        settings_dialog = SettingsDialog(self.settings, self.group_infos)
        settings_dialog.exec_()
        self.fill_group_names_combobox()

    def read_group_files(self):
        """Reads the files 'groups_fortgeschritten.txt' und 'groups_normal.txt',
        and extracts all groups and student data.
        Afterwards it fills all combo-boxes and load the first file
        """
        path_template = self.settings.value('Path/pk_repo', '') + '/Anwesenheiten/Anmeldung/groups_{group_type}.txt'

        for group_type in 'fortgeschritten', 'normal':
            with open(path_template.format(group_type=group_type), 'r', encoding='utf-8') as f:
                group_name_regex = re.compile('(mo|di|mi|do|fr)\d{2}\w')
                student_regex = re.compile('\s+[+✔]\s+(\D+)\s(\d+)\s(.*)\s?')

                students = []
                group_name = ''

                for line in f:
                    group_name_match = group_name_regex.search(line)
                    students_match = student_regex.search(line)

                    if group_name_match:
                        if students:
                            self.groups[group_name] = Group(group_name, group_type, students)
                            students = []
                        group_name = group_name_match.group(0)
                    elif students_match:
                        students.append(Student(*([students_match.group(i) for i in range(1, 4)] + [group_name])))

            if students:
                self.groups[group_name] = Group(group_name, group_type, students)

        self.group_type_combobox.addItems('Meine Alle Normal Fortgeschritten'.split())
        self.fill_group_names_combobox()
        self.populate_lesson_numbers()
        self.load_group_data()

    def get_group_infos(self):
        """Reads the file 'GRUPPEN.txt' from the pk-repo,
        and extracts all groups and the names of the instructor and the tutors.
        Saves this data as a dict.
        """
        path = self.settings.value('Path/pk_repo', '') + '/GRUPPEN.txt'

        group_name_regex = re.compile('(mo|di|mi|do|fr)\d{2}\w')

        with open(path, 'r', encoding='utf-8') as f:
            group_name = ''
            instructor = ''
            tutor1 = ''
            tutor2 = ''

            for line in f:
                match = group_name_regex.search(line)
                if match:
                    if group_name:
                        self.group_infos[group_name] = GroupInfos(instructor, tutor1, tutor2)
                    group_name = match.group(0)
                else:
                    extract_name = lambda: line.split('=')[-1].strip()
                    if line.startswith('leiter'):
                        instructor = extract_name()
                    if line.startswith('tutor1'):
                        tutor1 = extract_name()
                    if line.startswith('tutor2'):
                        tutor2 = extract_name()

            if group_name:
                self.group_infos[group_name] = GroupInfos(instructor, tutor1, tutor2)

    def fill_group_names_combobox(self):
        """Populate the combobox with all the group names,
        that apply for the group type specified in the form.
        """
        type_index = self.group_type_combobox.currentIndex()
        allowed_types = []

        if type_index > 0:
            if type_index != 2:
                allowed_types.append('fortgeschritten')
            if type_index != 3:
                allowed_types.append('normal')
            group_names = [group.name for group in self.groups.values() if group.type in allowed_types]
        else:
            username = self.settings.value('Personal/username', '')
            group_names = [group.name for group in self.groups.values() if self.group_infos[group.name].tutor1 == username or
                           self.group_infos[group.name].tutor2 == username]

        self.group_combobox.clear()
        group_names.sort(key=lambda name: ('mo di mi do fr'.split().index(name[:2]),name[2:]))
        self.group_combobox.addItems(group_names)

    def load_group_data(self):
        """Load all data for a specific group.
        It updates the names of the instructor and tutors and loads the last available csv-file for this group.
        """
        group_name = self.group_combobox.currentText()
        try:
            infos = self.group_infos[group_name]
            self.label_instructor_name.setText(infos.instructor)
            self.label_tutor1_name.setText(infos.tutor1)
            self.label_tutor2_name.setText(infos.tutor2)
        except KeyError:
            pass

        self.table_widget.clear()
        self.table_widget.setRowCount(0)

        if not self.lesson_combobox.currentText():
            self.table_widget.setColumnCount(0)
            return

        labels = 'Name;Matrikelnr.;Gruppe;Anwesend 00/00;Adhoc;Kommentar'.split(';')
        self.table_widget.setColumnCount(len(labels))
        self.table_widget.setSortingEnabled(False)
        self.table_widget.setHorizontalHeaderLabels(labels)

        for student in self.groups[group_name].students:
            self.add_row_to_table(student)

        path_template = self.settings.value('Path/pk_repo', '') + \
                '/Anwesenheiten/Uebungen/{nr}/{group_name}_ue{nr_plus_1}.csv'
        lesson_nr = int(self.lesson_combobox.currentText())
        path = path_template.format(nr=lesson_nr, group_name=group_name, nr_plus_1=lesson_nr+1)
        self.load_csv_file(path)

        # self.update_checkbox_data()

        self.table_widget.resizeColumnsToContents()
        self.table_widget.setSortingEnabled(True)
        self.table_widget.sortByColumn(0, QtCore.Qt.AscendingOrder)

    def add_row_to_table(self, student):
        """Adds a new row to the table and fills this row with the student's data
        """
        idx = self.table_widget.rowCount()
        self.table_widget.setRowCount(idx + 1)

        name_item = QTableWidgetItem(student.name)
        name_item.setFlags(name_item.flags() & ~QtCore.Qt.ItemIsEditable)
        self.table_widget.setItem(idx, 0, name_item)

        matrikelnr_item = QTableWidgetItem(student.matrikelnr)
        matrikelnr_item.setFlags(matrikelnr_item.flags() & ~QtCore.Qt.ItemIsEditable)
        matrikelnr_item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.table_widget.setItem(idx, 1, matrikelnr_item)

        group_item = QTableWidgetItem(student.group_name)
        group_item.setFlags(matrikelnr_item.flags() & ~QtCore.Qt.ItemIsEditable)
        group_item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.table_widget.setItem(idx, 2, group_item)

        check_item = QTableWidgetItem()
        check_item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.table_widget.setItem(idx, 3, check_item)
        check_widget = QWidget()
        chk_bx = QCheckBox()
        chk_bx.setCheckState(QtCore.Qt.Unchecked)
        chk_bx.stateChanged.connect(self.attendance_changed)
        chk_bx.clicked.connect(self.update_checkbox_data)
        lay_out = QHBoxLayout(check_widget)
        lay_out.addWidget(chk_bx)
        lay_out.setAlignment(QtCore.Qt.AlignCenter)
        lay_out.setContentsMargins(0,0,0,0)
        check_widget.setLayout(lay_out)
        self.table_widget.setCellWidget(idx, 3, check_widget)
        ckb = self.table_widget.cellWidget(idx, 3).layout().itemAt(0)

        adhoc_item = QTableWidgetItem()
        adhoc_item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.table_widget.setItem(idx, 4, adhoc_item)

        self.table_widget.setItem(idx, 5, QTableWidgetItem())

    def populate_lesson_numbers(self):
        """Finds the csv files for this group and populates the combobox
        """
        group_name = self.group_combobox.currentText()
        path_template = self.settings.value('Path/pk_repo', '') + \
                        '/Anwesenheiten/Uebungen/{nr}/{group_name}_ue{nr_plus_1}.csv'
        lessons = []
        for lesson_nr in range(99):
            path = path_template.format(nr=lesson_nr, group_name=group_name, nr_plus_1=lesson_nr+1)
            if os.path.isfile(path):
                lessons.append(str(lesson_nr))
            else:
                break

        self.lesson_combobox.clear()
        self.lesson_combobox.addItems(lessons)

    def load_csv_file(self, path):
        """Load a lesson-csv-file and update the table with it's data
        """
        with open(path, 'r', encoding='utf-8') as f:
            next(f)
            for line in f:
                matrikelnr, group_name, attendance, comment = line.strip().split(';')
                adhoc, *comment = comment.split()
                adhoc = adhoc.strip('%')
                if adhoc == '0':
                    adhoc = ''
                comment = ' '.join(comment)

                indices = [idx for idx in range(self.table_widget.rowCount())
                               if self.table_widget.item(idx, 1).text() == matrikelnr]
                if len(indices) == 1:
                    idx = indices[0]
                else:
                    idx = self.table_widget.rowCount()
                    new_student = None
                    for group in self.groups.values():
                        for student in group.students:
                            if student.matrikelnr == matrikelnr:
                                new_student = student
                    if new_student:
                        self.add_row_to_table(new_student)
                    else:
                        self.add_row_to_table(Student('', matrikelnr, '', group_name))

                self.table_widget.item(idx, 1).setText(matrikelnr)
                self.table_widget.item(idx, 2).setText(group_name)
                self.get_checkbox(idx).setCheckState(QtCore.Qt.Checked if attendance == 'an' else
                                                     QtCore.Qt.Unchecked)
                self.table_widget.item(idx, 4).setText(adhoc)
                self.table_widget.item(idx, 5).setText(comment)

    def get_checkbox(self, index):
        """Returns the checkbox for a specific index
        """
        return self.table_widget.cellWidget(index, 3).layout().itemAt(0).widget()

    def attendance_changed(self):
        """Update the attendance-statistic
        """
        count = sum(self.get_checkbox(index).isChecked() for index in range(self.table_widget.rowCount()))
        attendance = 'Anwesend {}/{}'.format(count, self.table_widget.rowCount())
        self.table_widget.setHorizontalHeaderItem(3, QTableWidgetItem(attendance))

    def update_checkbox_data(self):
        for idx in range(self.table_widget.rowCount()):
            self.table_widget.item(idx, 3).setData(0, int(self.get_checkbox(idx).isChecked()))

    def get_savefiles(self):
        current_group = self.group_combobox.currentText()
        if os.path.exists('Saves'):
            self.history_files = sorted(set(f for f in os.listdir('Saves') if f.startswith(current_group)))

    def write_file(self, savefile=True):

        group_name = self.group_combobox.itemText(self.current_group_idx)
        if savefile:
            now = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
            file_name = 'Saves/{}_{}.csv'.format(group_name, now)
        else:
            file_name = QFileDialog.getSaveFileName(self, 'Export', group_name + '_ueX.csv', 'CSV (*.csv)')[0]
            if not file_name:
                return

        if not os.path.exists('Saves'):
            os.makedirs('Saves')

        with io.open(file_name, 'w', encoding='utf-8', newline='') as f:
            f.write('MatrNr;Gruppe;Kontrolle;Kommentar\n')
            for idx in range(self.table_widget.rowCount()):
                if self.table_widget.item(idx, 1).text():
                    f.write('{};{};{};{}% {}\n'.format(
                        self.table_widget.item(idx, 1).text(),
                        self.table_widget.item(idx, 2).text() or '0',
                        'an' if self.get_checkbox(idx).isChecked() else 'ab',
                        self.table_widget.item(idx, 4).text() or '0',
                        self.table_widget.item(idx, 5).text()
                    ))

        self.history_files.append(file_name[6:])
        self.history_index = len(self.history_files) - 1

    def find_index(self, name):
        indices = [i for i in range(self.table_widget.rowCount())
                   if name.lower() in self.table_widget.item(i, 0).text().lower()]
        return indices[0] if len(indices) == 1 else indices

    def execute_console(self):
        try:
            commands = self.console.text().split(' ')
            name, command = commands[0], ' '.join(commands[1:])
            index = self.find_index(name)
            if isinstance(index, int):
                full_name = self.table_widget.item(index, 0).text()
                if command == 'a':
                    self.get_checkbox(index).setCheckState(QtCore.Qt.Checked)
                    template = '{} ist anwesend'
                elif command == 'b':
                    self.get_checkbox(index).setCheckState(QtCore.Qt.Unchecked)
                    template = '{} ist nicht anwesend'
                elif command.isdigit():
                    self.table_widget.item(index, 4).setText(command)
                    template = '{} erreicht {}%'
                else:
                    self.table_widget.item(index, 5).setText(command)
                    template = '{}: {}'
                self.console_output.setText(template.format(full_name, command))
            else:
                if len(index) == 0:
                    error = 'Der Student "{}" wurde nicht gefunden.'
                else:
                    error = 'Mehrere Studenten treffen auf "{}" zu.'
                self.console_output.setText('Error: ' + error.format(name))

        except IndexError:
            pass

        self.console.clear()


class SettingsDialog(QDialog, Ui_SettingsDialog):
    def __init__(self, settings, group_infos):
        QDialog.__init__(self)
        self.setupUi(self)

        self.settings = settings
        pk_repo_path = self.settings.value('Path/pk_repo', '')
        self.line_edit_repo_path.setText(pk_repo_path)

        tutor_names = sorted(set([''] + [group.tutor1 for group in group_infos.values()] +
                                 [group.tutor2 for group in group_infos.values()]))
        self.username_combobox.addItems(tutor_names)
        tutor_name = self.settings.value('Personal/username', '')
        try:
            self.username_combobox.setCurrentIndex(tutor_names.index(tutor_name))
        except ValueError:
            pass

        self.button_select_repo_path.clicked.connect(self.select_repo_path)
        self.buttonBox.accepted.connect(self.accept_settings)

    def select_repo_path(self):
        pk_repo_path = QFileDialog.getExistingDirectory(self, 'Pfad zum PK-Repository', self.line_edit_repo_path.text(), QFileDialog.ShowDirsOnly)
        if pk_repo_path:
            self.line_edit_repo_path.setText(pk_repo_path)

    def accept_settings(self):
        self.settings.setValue('Path/pk_repo', self.line_edit_repo_path.text())
        self.settings.setValue('Personal/username', self.username_combobox.currentText())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PkToolMainWindow()
    window.show()
    sys.exit(app.exec_())
