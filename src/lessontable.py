import io
from PyQt5 import QtCore
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QWidget, QCheckBox, QHBoxLayout
from src.group import Group
from src.group_infos import Student
from src.history import History


class LessonTable(QTableWidget):
    """
    Extent the QTableWidget, so that it can maintain the date in the table.
    This includes filling the table with data using the name of a group and a corresponding csv-file,
    recording every change in a history, and exporting the data back to a csv-file.

    Usage infos: after creating the table the method connect has to be called!
    """

    def __init__(self, widget):
        """
        Initialize locks and history data. Connect signals and slots.
        """
        super().__init__(widget)

        self.react_lock = False
        self.history = History()
        self.group_infos = None
        self.action_redo = None
        self.action_undo = None
        self.get_csv_path = None
        self.group = None
        self.write_console = None
        self.test_file = False

        self.cellChanged.connect(self.react_to_change)

    def connect(self, group_infos, action_undo, action_redo, get_csv_path, write_console):
        """
        Connect infos and important actions from the mainwindow with the table.
        """
        self.group_infos = group_infos
        self.action_undo = action_undo
        self.action_redo = action_redo
        self.get_csv_path = get_csv_path
        self.write_console = write_console

    def react_to_change(self):
        """
        React if there are no locks by writing the changes to history and by exporting the data to the csv-file.
        Change the count of the attendance column.
        """
        if not self.react_lock:
            self.history.record_changes(self.get_current_data())
            self.export_csv()

            count = sum(self.get_checkbox(index).isChecked() for index in range(self.rowCount()))
            attendance = 'Anwesend {}/{}'.format(count, self.rowCount())
            self.setHorizontalHeaderItem(3, QTableWidgetItem(attendance))

            self.history.adjust_undo_redo()

    def setup_table(self, group: Group):
        """
        Clear the table and history, refill the table with column names, and students default data.
        """
        self.react_lock = True

        self.clear()
        self.setRowCount(0)

        self.group = group
        labels = 'Name;Matrikelnr.;Gruppe;Anwesend 00/00;Adhoc;Kommentar'.split(';')
        self.setColumnCount(len(labels))
        self.setSortingEnabled(False)
        self.setHorizontalHeaderLabels(labels)

        for student in group.students:
            self.add_row_to_table(student)

        self.history = History(self.action_undo, self.action_redo, self.write_console, self.group_infos)

    def add_row_to_table(self, student: Student):
        """
        Adds a new row to the table and fills this row with item-widgets filled with the student's data.
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
        chk_bx.stateChanged.connect(self.react_to_change)
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

    def get_checkbox(self, index):
        """
        Returns the checkbox for a specific index
        """
        return self.cellWidget(index, 3).layout().itemAt(0).widget()

    def load_csv_file(self, path, test_file=False):
        """
        Load a lesson-csv-file and update the table with it's data
        """
        self.setSortingEnabled(False)
        self.react_lock = True

        self.test_file = test_file

        try:
            with open(path, 'r', encoding='utf-8') as file:
                next(file)  # skip header
                for line in file:
                    matrikelnr, group_name, attendance, comment = line.strip().split(';')
                    if not test_file:
                        adhoc, *comment = comment.split()
                        adhoc = adhoc.strip('%')
                        if adhoc == '0':
                            adhoc = ''
                        comment = ' '.join(comment)
                    else:
                        adhoc = ''

                    idx = self.index_of_student(matrikelnr)
                    if idx < 0:
                        idx = self.rowCount()
                        new_student = self.group_infos.get_student(matrikelnr)
                        if test_file:
                            new_student = Student(new_student.name, new_student.matrikelnr, new_student.email,
                                                  self.group.name)

                        self.add_row_to_table(new_student)

                    self.item(idx, 1).setText(matrikelnr)
                    self.item(idx, 2).setText(group_name)
                    self.get_checkbox(idx).setCheckState(QtCore.Qt.Checked if attendance == 'an' else
                                                         QtCore.Qt.Unchecked)
                    self.item(idx, 4).setText(adhoc)
                    self.item(idx, 5).setText(comment)
        except FileNotFoundError:
            pass

        self.resizeColumnsToContents()
        self.setSortingEnabled(True)
        self.sortByColumn(0, QtCore.Qt.AscendingOrder)
        self.react_lock = False
        self.history.current_data = self.get_current_data()
        self.history.adjust_undo_redo()

    def new_student(self, matrikelnr):
        """
        Adds a new row for a new student to the table.
        """
        self.react_lock = True
        self.setSortingEnabled(False)

        student = self.group_infos.get_student(matrikelnr)
        if self.test_file:
            student = Student(student.name, student.matrikelnr, student.email, self.group.name)

        self.add_row_to_table(student)
        text = '{} hinzugefügt'.format(student.name)
        self.history.add_change((matrikelnr, text, 1, None, student))

        self.setSortingEnabled(True)
        self.react_lock = False

    def export_csv(self):
        """
        Write the opened table to a csv-file
        """
        path = self.get_csv_path()

        # read file so it can keep the order of the lines
        order = dict()
        with open(path, 'r', encoding='utf-8') as f:
            next(f)
            for idx, line in enumerate(f):
                matrikelnr = line.split(';')[0]
                order[matrikelnr] = idx

        with io.open(path, 'w', encoding='utf-8', newline='') as f:
            f.write('MatrNr;Gruppe;Kontrolle;Kommentar\n')
            data = self.get_current_data()
            data.sort(key=lambda t: order.get(t[0], 999))
            for d in data:
                if self.test_file:
                    f.write('{};{};{};{}\n'.format(d[0], d[1], d[2], d[4]))
                else:
                    f.write('{};{};{};{}% {}\n'.format(*d))

    def index_of_student(self, identification):
        """
        Find the index of a student in the table. Identification can be a part of his name or the matrikel-nummer.
        Returns -1, if no student is found, or -2 if multiple students are found.
        """
        indices = [i for i in range(self.rowCount())
                   if identification.lower() in self.item(i, 0).text().lower() or
                   identification == self.item(i, 1).text()]
        if len(indices) == 1:
            return indices[0]
        if indices:
            return -2
        else:
            return -1

    def get_current_data(self):
        """
        Reads all data from the table and returns a list of it
        """
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

    def undo_history(self, reverse=False):
        """
        Undos/redos the last history.
        """
        self.react_lock = True
        self.setSortingEnabled(False)

        last_history = self.history.undo_history(reverse=reverse)
        if last_history:
            index = self.index_of_student(last_history[0])
            if index >= 0:
                if last_history[2] == 1:
                    if not last_history[3]:
                        self.removeRow(index)

                if last_history[2] == 2:
                    self.get_checkbox(index).setCheckState(QtCore.Qt.Checked if last_history[3] == 'an' else
                                                           QtCore.Qt.Unchecked)
                if last_history[2] in [3, 4]:
                    self.item(index, last_history[2] + 1).setText(last_history[3])
            else:
                if last_history[2] == 1 and last_history[3]:
                    self.add_row_to_table(last_history[3])

            self.history.current_data = self.get_current_data()
            self.history.adjust_undo_redo()

        self.setSortingEnabled(True)
        self.react_lock = False
        self.export_csv()
