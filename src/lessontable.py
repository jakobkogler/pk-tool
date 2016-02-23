import io
from PyQt5 import QtCore
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QWidget, QCheckBox, QHBoxLayout
from src.group import Group
from src.group_infos import Student


class LessonTable(QTableWidget):
    def __init__(self, widget):
        super().__init__(widget)
        self.write_lock = False
        self.history = []
        self.history_foreward = []
        self.current_data = []
        self.history_lock = False

        self.cellChanged.connect(self.export_csv)

    def prepair_table(self, group: Group):
        self.write_lock = True
        self.history = []
        self.history_foreward = []
        self.clear()
        self.setRowCount(0)

        if not group.name:
            self.setColumnCount(0)
            return

        self.group = group
        labels = 'Name;Matrikelnr.;Gruppe;Anwesend 00/00;Adhoc;Kommentar'.split(';')
        self.setColumnCount(len(labels))
        self.setSortingEnabled(False)
        self.setHorizontalHeaderLabels(labels)

        for student in group.students:
            self.add_row_to_table(student)

    def add_row_to_table(self, student: Student):
        """Adds a new row to the table and fills this row with the student's data
        """

        idx = self.rowCount()
        self.setRowCount(idx + 1)

        name_item = QTableWidgetItem(student.name)
        name_item.setFlags(name_item.flags() & ~QtCore.Qt.ItemIsEditable)
        self.setItem(idx, 0, name_item)

        matrikelnr_item = QTableWidgetItem(student.matrikelnr)
        matrikelnr_item.setFlags(matrikelnr_item.flags() & ~QtCore.Qt.ItemIsEditable)
        matrikelnr_item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.setItem(idx, 1, matrikelnr_item)

        group_item = QTableWidgetItem(student.group_name)
        group_item.setFlags(matrikelnr_item.flags() & ~QtCore.Qt.ItemIsEditable)
        group_item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.setItem(idx, 2, group_item)

        check_item = QTableWidgetItem()
        check_item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.setItem(idx, 3, check_item)
        check_widget = QWidget()
        chk_bx = QCheckBox()
        chk_bx.setCheckState(QtCore.Qt.Unchecked)
        chk_bx.stateChanged.connect(self.attendance_changed)
        lay_out = QHBoxLayout(check_widget)
        lay_out.addWidget(chk_bx)
        lay_out.setAlignment(QtCore.Qt.AlignCenter)
        lay_out.setContentsMargins(0, 0, 0, 0)
        check_widget.setLayout(lay_out)
        self.setCellWidget(idx, 3, check_widget)

        adhoc_item = QTableWidgetItem()
        adhoc_item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.setItem(idx, 4, adhoc_item)

        self.setItem(idx, 5, QTableWidgetItem())

    def attendance_changed(self):
        """Update the attendance-statistic
        """
        self.export_csv()
        count = sum(self.get_checkbox(index).isChecked() for index in range(self.rowCount()))
        attendance = 'Anwesend {}/{}'.format(count, self.rowCount())
        self.setHorizontalHeaderItem(3, QTableWidgetItem(attendance))

    def get_checkbox(self, index):
        """Returns the checkbox for a specific index
        """
        return self.cellWidget(index, 3).layout().itemAt(0).widget()

    def load_csv_file(self, path):
        """Load a lesson-csv-file and update the table with it's data
        """

        self.setSortingEnabled(False)
        self.write_lock = True

        with open(path, 'r', encoding='utf-8') as f:
            next(f)
            for line in f:
                matrikelnr, group_name, attendance, comment = line.strip().split(';')
                adhoc, *comment = comment.split()
                adhoc = adhoc.strip('%')
                if adhoc == '0':
                    adhoc = ''
                comment = ' '.join(comment)

                indices = [idx for idx in range(self.rowCount())
                           if self.item(idx, 1).text() == matrikelnr]
                if len(indices) == 1:
                    idx = indices[0]
                else:
                    idx = self.rowCount()

                    new_student = self.group_infos.get_student(matrikelnr)
                    if new_student:
                        self.add_row_to_table(new_student)
                    else:
                        self.add_row_to_table(Student('', matrikelnr, '', group_name))

                self.item(idx, 1).setText(matrikelnr)
                self.item(idx, 2).setText(group_name)
                self.get_checkbox(idx).setCheckState(QtCore.Qt.Checked if attendance == 'an' else
                                                     QtCore.Qt.Unchecked)
                self.item(idx, 4).setText(adhoc)
                self.item(idx, 5).setText(comment)

        self.resizeColumnsToContents()
        self.setSortingEnabled(True)
        self.sortByColumn(0, QtCore.Qt.AscendingOrder)
        self.write_lock = False
        self.current_data = self.get_data()
        self.show_last_history()

    def set_group_infos(self, group_infos):
        self.group_infos = group_infos

    def new_student(self, matrikelnr):
        self.write_lock = True
        self.setSortingEnabled(False)

        student = self.group_infos.get_student(matrikelnr)
        self.add_row_to_table(student)
        text = '{} hinzugefügt'.format(student.name)
        self.add_new_history((matrikelnr, text, 1, None, student))

        self.setSortingEnabled(True)
        self.write_lock = False

    def export_csv(self):
        """Write the opened table to a csv-file
        """
        if self.write_lock:
            return

        if not self.history_lock:
            self.get_changes()

        path = self.get_csv_path()

        order = dict()
        with open(path, 'r', encoding='utf-8') as f:
            next(f)
            for idx, line in enumerate(f):
                matrikelnr = line.split(';')[0]
                order[matrikelnr] = idx

        with io.open(path, 'w', encoding='utf-8', newline='') as f:
            f.write('MatrNr;Gruppe;Kontrolle;Kommentar\n')
            data = self.get_data()
            data.sort(key=lambda t: order.get(t[0], 999))
            for d in data:
                f.write('{};{};{};{}% {}\n'.format(*d))

        self.show_last_history()

    def get_changes(self):
        data = self.get_data()
        if len(data) == len(self.current_data):
            for new, current in zip(data, self.current_data):
                if new != current:
                    student = self.group_infos.get_student(new[0])
                    student_name = student.name if student.name else student.matrikelnr
                    if new[2] == 'an' != current[2]:
                        text = '{} ist anwesend'.format(student_name)
                        self.add_new_history((new[0], text, 2, 'ab', 'an'))
                    if new[2] == 'ab' != current[2]:
                        text = '{} ist nicht anwesend'.format(student_name)
                        self.add_new_history((new[0], text, 2, 'an', 'ab'))
                    if new[3] != current[3]:
                        text = '{} erreicht {} bei der Adhoc-Aufgabe'.format(student_name, new[3])
                        self.add_new_history((new[0], text, 3, current[3], new[3]))
                    if new[4] != current[4]:
                        text = '{}: {}'.format(student_name, new[4])
                        self.add_new_history((new[0], text, 4, current[4], new[4]))

        self.current_data = data

    def add_new_history(self, history):
        self.history.append(history)
        self.history_foreward = []
        self.write_console(history[1])
        self.show_last_history()

    def undo_history(self, reverse=False):
        self.history_lock = True
        last_history = None
        if not reverse:
            if len(self.history):
                last_history = self.history.pop()
                new_history = (last_history[0], last_history[1], last_history[2], last_history[4], last_history[3])
                self.history_foreward.append(new_history)
                self.write_console('Rückgängig: {}'.format(last_history[1]))
        else:
            if len(self.history_foreward):
                last_history = self.history_foreward.pop()
                new_history = (last_history[0], last_history[1], last_history[2], last_history[4], last_history[3])
                self.history.append(new_history)
                self.write_console('Wiederherstellen: {}'.format(last_history[1]))

        if last_history is None:
            return

        self.setSortingEnabled(False)

        index = -1
        for i in range(self.rowCount()):
            if self.item(i, 1).text() == last_history[0]:
                index = i
                break
        if index >= 0:
            if last_history[2] == 1:
                if not last_history[3]:
                    self.removeRow(index)
                else:
                    self.add_row_to_table(last_history[3])
            if last_history[2] == 2:
                self.get_checkbox(index).setCheckState(QtCore.Qt.Checked if last_history[3] == 'an' else
                                                       QtCore.Qt.Unchecked)
            if last_history[2] in [3, 4]:
                self.item(index, last_history[2] + 1).setText(last_history[3])

        self.setSortingEnabled(True)
        self.current_data = self.get_data()

        self.show_last_history()
        self.history_lock = False

    def set_action_undo(self, action_undo):
        self.action_undo = action_undo

    def set_action_redo(self, action_redo):
        self.action_redo = action_redo

    def show_last_history(self):
        if self.history:
            message = self.history[-1][1]
            self.action_undo.setEnabled(True)
            self.action_undo.setText('Zurück ({})'.format(message))
        else:
            self.action_undo.setText('Zurück')
            self.action_undo.setEnabled(False)

        if self.history_foreward:
            message = self.history_foreward[-1][1]
            self.action_redo.setEnabled(True)
            self.action_redo.setText('Vor ({})'.format(message))
        else:
            self.action_redo.setText('Vor')
            self.action_redo.setEnabled(False)

    def get_data(self):
        data = []
        for idx in range(self.rowCount()):
            if self.item(idx, 1).text():
                data.append((
                    self.item(idx, 1).text(),
                    self.item(idx, 2).text() or '0',
                    'an' if self.get_checkbox(idx).isChecked() else 'ab',
                    self.item(idx, 4).text() or '0',
                    self.item(idx, 5).text()
                ))
        return sorted(data)

    def find_index(self, identification):
        """Find the index of a student in the table
        """
        indices = [i for i in range(self.rowCount())
                   if identification.lower() in self.item(i, 0).text().lower() or
                   identification == self.item(i, 1).text()]
        return indices[0] if len(indices) == 1 else indices
