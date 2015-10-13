import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QFileDialog, QCheckBox, QWidget, QHBoxLayout
from PyQt5 import QtCore
from mainwindow import Ui_MainWindow
import os
import re
import io
from collections import namedtuple
from _datetime import datetime


Student = namedtuple('Student', 'name matrikelnr email')


class PkToolMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.name_files = []
        self.history_files = []
        self.history_index = None
        self.find_files()
        self.current_group_idx = 0
        self.write_lock = False
        self.checked_list = []
        self.open_file(0)

        self.files_combobox.currentIndexChanged.connect(self.open_file)
        self.action_export.triggered.connect(lambda: self.write_file(savefile=False))
        self.table_widget.cellChanged.connect(lambda: self.write_file(savefile=True))
        self.console.returnPressed.connect(self.execute_console)
        self.action_new.triggered.connect(lambda: self.open_file(self.files_combobox.currentIndex(), new=True))
        self.action_undo.triggered.connect(self.history_undo)
        self.action_redo.triggered.connect(self.history_redo)

    def find_files(self):
        r = re.compile('185\.A79 Programmkonstruktion .*_(.*?)_Überblick.txt')
        matches = [r.search(f) for f in os.listdir('.')]
        self.name_files = [m.group(0) for m in matches if m]
        shortcuts = [m.group(1) for m in matches if m]
        self.files_combobox.addItems(shortcuts)

    def attendance_changed(self):
        self.write_file(savefile=True)
        count = sum(chk.isChecked() for chk in self.checked_list)
        self.table_widget.setHorizontalHeaderItem(2, QTableWidgetItem('Anwesend {}/{}'.format(count,
                                                                                              len(self.checked_list))))


    def open_file(self, index, new=False):
        if self.history_index != None and self.history_index != len(self.history_files) - 1:
            self.write_file(savefile=True)

        # if self.current_group_idx != index:
        #     really = QMessageBox.question(self, 'Öffnen',
        #                                   'Möchten Sie die Gruppe wechseln?\n Alle Änderungenen werden gelöscht!',
        #                                   QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        #     if really != QMessageBox.Yes:
        #         self.files_combobox.setCurrentIndex(self.current_group_idx)
        #         return

        self.current_group_idx = index

        with open(self.name_files[index], 'r', encoding='utf-8') as f:
            students = []
            r = re.compile('\s+✔\s+(\D+)\s(\d+)\s(.*)\s?')
            for line in f:
                m = r.search(line)
                if m:
                    students.append(Student(*(m.group(i) for i in range(1, 4))))

        self.write_lock = True
        self.table_widget.clear()
        labels = 'Name;Matrikelnr.;Anwesend {:02}/{};Adhoc;Kommentar'.format(0, len(students)).split(';')
        self.table_widget.setRowCount(len(students))
        self.table_widget.setColumnCount(len(labels))
        self.table_widget.setHorizontalHeaderLabels(labels)

        self.checked_list = []

        for idx, student in enumerate(sorted(students, key=lambda s: s.matrikelnr)):
            name_item = QTableWidgetItem(student.name)
            name_item.setFlags(name_item.flags() & ~QtCore.Qt.ItemIsEditable)
            self.table_widget.setItem(idx, 0, name_item)

            matrikelnr_item = QTableWidgetItem(student.matrikelnr)
            matrikelnr_item.setFlags(matrikelnr_item.flags() & ~QtCore.Qt.ItemIsEditable)
            matrikelnr_item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.table_widget.setItem(idx, 1, matrikelnr_item)

            check_item = QWidget()
            chk_bx = QCheckBox()
            chk_bx.setCheckState(QtCore.Qt.Unchecked)
            chk_bx.stateChanged.connect(self.attendance_changed)
            lay_out = QHBoxLayout(check_item)
            lay_out.addWidget(chk_bx)
            lay_out.setAlignment(QtCore.Qt.AlignCenter)
            lay_out.setContentsMargins(0,0,0,0)
            check_item.setLayout(lay_out)
            self.checked_list.append(chk_bx)
            self.table_widget.setCellWidget(idx, 2, check_item)

            adhoc_item = QTableWidgetItem()
            adhoc_item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.table_widget.setItem(idx, 3, adhoc_item)

            self.table_widget.setItem(idx, 4, QTableWidgetItem())

        self.get_savefiles()
        self.history_index = len(self.history_files)
        if self.history_files and not new:
            self.history_undo()
            self.write_lock = False
        else:
            self.write_lock = False
            self.write_file(savefile=True)

        self.table_widget.resizeColumnsToContents()

    def get_savefiles(self):
        current_group = self.files_combobox.currentText()
        if os.path.exists('Saves'):
            self.history_files = sorted(f for f in os.listdir('Saves') if f.startswith(current_group))

    def history_undo(self):
        if self.history_index:
            self.history_index -= 1
            self.history_load()

    def history_redo(self):
        if self.history_index < len(self.history_files) - 1:
            self.history_index += 1
            self.history_load()

    def history_load(self):
        self.write_lock = True
        with open('Saves/' + self.history_files[self.history_index], 'r') as f:
            next(f)
            for line in f:
                matrikelnr, group, attendance, comment = line.strip().split(';')
                adhoc, *comment = comment.split()
                adhoc = adhoc.strip('%')
                comment = ' '.join(comment)

                for idx in range(self.table_widget.rowCount()):
                    if self.table_widget.item(idx, 1).text() == matrikelnr:
                        self.checked_list[idx].setCheckState(QtCore.Qt.Checked if attendance == 'an' else
                                                             QtCore.Qt.Unchecked)
                        self.table_widget.item(idx, 3).setText(adhoc)
                        self.table_widget.item(idx, 4).setText(comment)
        self.write_lock = False

    def write_file(self, savefile=True):
        if self.write_lock:
            return

        group_name = self.files_combobox.itemText(self.current_group_idx)
        if savefile:
            now = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
            file_name = 'Saves/{}_{}.csv'.format(group_name, now)
        else:
            file_name = QFileDialog.getSaveFileName(self, 'Export', group_name + '.csv', 'CSV (*.csv)')[0]
            if not file_name:
                return

        if not os.path.exists('Saves'):
            os.makedirs('Saves')

        with io.open(file_name, 'w', encoding='utf-8', newline='') as f:
            f.write('MatrNr;Gruppe;Kontrolle;Kommentar\n')
            for idx in range(self.table_widget.rowCount()):
                f.write('{};{};{};{}% {}\n'.format(
                    self.table_widget.item(idx, 1).text(),
                    self.files_combobox.currentText(),
                    'an' if self.checked_list[idx].isChecked() else 'ab',
                    self.table_widget.item(idx, 3).text() or '0',
                    self.table_widget.item(idx, 4).text()
                ))

        self.history_files.append(file_name.lstrip('Saves/'))
        self.history_index = len(self.history_files) - 1

    def find_index(self, name):
        indices = [i for i in range(self.table_widget.rowCount())
                   if name.lower() in self.table_widget.item(i, 0).text().lower()]
        return indices[0] if len(indices) == 1 else None

    def execute_console(self):
        try:
            commands = self.console.text().split(' ')
            name, command = commands[0], ' '.join(commands[1:])
            index = self.find_index(name)
            if index is not None:
                full_name = self.table_widget.item(index, 0).text()
                if command == 'a':
                    self.checked_list[index].setCheckState(QtCore.Qt.Checked)
                    template = '{} ist anwesend'
                elif command == 'b':
                    self.checked_list[index].setCheckState(QtCore.Qt.Unchecked)
                    template = '{} ist nicht anwesend'
                elif command.isdigit():
                    self.table_widget.item(index, 3).setText(command)
                    template = '{} erreicht {}%'
                else:
                    self.table_widget.item(index, 4).setText(command)
                    template = '{}: {}'
                self.console_output.setText(template.format(full_name, command))
            else:
                self.console_output.setText('Error: {}'.format(name))

        except IndexError:
            pass

        self.console.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PkToolMainWindow()
    window.show()
    sys.exit(app.exec_())
