class History:
    """
    Records every change in the table and undo/redo this actions on command.
    """

    def __init__(self, action_undo=None, action_redo=None, write_console=None, group_infos=None):
        self.history = []
        self.history_foreward = []
        self.current_data = []
        self.action_undo = action_undo
        self.action_redo = action_redo
        self.write_console = write_console
        self.group_infos = group_infos

    def adjust_undo_redo(self):
        """
        Adjusts the undo and redo buttons (text and enabled) depending on the history
        """
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

    def add_change(self, change):
        """
        Stores a new change into the history.
        Deletes all forwards-history.
        Prints the changes to the console and adjusts undo/redo buttons
        """
        self.history.append(change)
        self.history_foreward = []
        self.write_console(change[1])
        self.adjust_undo_redo()

    def record_changes(self, new_data):
        """
        Figures out what changed in the table compared to the last saved data.
        Records it in the history.
        Doesn't work if you added a new student to the table.
        """
        if len(new_data) == len(self.current_data):
            for new, current in zip(new_data, self.current_data):
                if new != current:
                    student = self.group_infos.get_student(new[0])
                    student_name = student.name if student.name else student.matrikelnr
                    if new[2] == 'an' != current[2]:
                        text = '{} ist anwesend'.format(student_name)
                        self.add_change((new[0], text, 2, 'ab', 'an'))
                    if new[2] == 'ab' != current[2]:
                        text = '{} ist nicht anwesend'.format(student_name)
                        self.add_change((new[0], text, 2, 'an', 'ab'))
                    if new[3] != current[3]:
                        text = '{0} erreicht {1} bei der Adhoc-Aufgabe'.format(student_name, new[3])
                        self.add_change((new[0], text, 3, current[3], new[3]))
                    if new[4] != current[4]:
                        text = '{0}: {1}'.format(student_name, new[4])
                        self.add_change((new[0], text, 4, current[4], new[4]))

        self.current_data = new_data

    def undo_history(self, reverse=False):
        """
        Undos/redos the last history.
        """
        last_history = None
        if not reverse and self.history:
            last_history = self.history.pop()
            new_history = (last_history[0], last_history[1], last_history[2], last_history[4], last_history[3])
            self.history_foreward.append(new_history)
            self.write_console('Rückgängig: {}'.format(last_history[1]))
        elif reverse and self.history_foreward:
            last_history = self.history_foreward.pop()
            new_history = (last_history[0], last_history[1], last_history[2], last_history[4], last_history[3])
            self.history.append(new_history)
            self.write_console('Wiederherstellen: {}'.format(last_history[1]))

        return last_history
