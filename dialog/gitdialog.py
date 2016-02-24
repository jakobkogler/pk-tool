import re
from PyQt5.QtWidgets import QDialog, QMessageBox
from ui.git_interactions import Ui_GitDialog
from src.git_interactions import GitInteractions


class GitDialog(QDialog, Ui_GitDialog):
    """
    Dialog to add and commit files to the pk-repo.
    """

    def __init__(self, git_interactions: GitInteractions):
        """
        Initialize everything. Show modified files.
        """
        QDialog.__init__(self)
        self.setupUi(self)

        self.git_interactions = git_interactions

        self.list_widget.clear()
        self.list_widget.addItems(self.git_interactions.get_changed_or_untracked_files())
        self.list_widget.selectAll()

        self.button_box.accepted.connect(self.commit_and_push)

    def commit_and_push(self):
        """
        Commit every marked file with a separate commit.
        Push at the end.
        Print error-message if an error occurred.
        """
        success = self.git_interactions.pull()
        if success:
            files = [item.text() for item in self.list_widget.selectedItems()]
            for file in files:
                pattern = re.compile('(\w\w\d\d\w)_ue')
                matches = pattern.search(file)
                group_name = ''
                if matches:
                    group_name = matches.group(1)
                message = self.commit_message_line_edit.text().format(group_name=group_name)

                success = self.git_interactions.commit_file(file, message)
                if not success:
                    break
            else:
                success = self.git_interactions.push()
        if success:
            QMessageBox.about(self, 'Erfolgreich', 'Dateien erfolgreich committet.')
        elif self.list_widget.selectedItems():
            QMessageBox.about(self, 'Fehler', 'Es gab einen Fehler beim Committen der neuen Dateien. \n'
                              'Bitte kontrollieren Sie das Git-Repository manuell.')

