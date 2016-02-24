import re
from PyQt5.QtWidgets import QDialog, QMessageBox
from ui.git_interactions import Ui_GitDialog

try:
    from git import Repo, FetchInfo
except ImportError:
    pass


class GitDialog(QDialog, Ui_GitDialog):
    """
    Dialog to add and commit files to the pk-repo.
    """

    def __init__(self, repo):
        """
        Initialize everything. Show modified files.
        """
        QDialog.__init__(self)
        self.setupUi(self)

        self.repo = repo

        self.list_widget.clear()
        self.list_widget.addItems(self.get_changed_or_untracked_files())
        self.list_widget.selectAll()

        self.button_box.accepted.connect(self.commit_and_push)

    def commit_and_push(self):
        """
        Commit every marked file with a separate commit.
        Push at the end.
        Print error-message if an error occurred.
        """
        error = False

        o = self.repo.remotes.origin
        info = o.pull()[0]
        if info.flags & (FetchInfo.ERROR | FetchInfo.REJECTED):
            error = True
        else:
            try:
                files = [item.text() for item in self.list_widget.selectedItems()]
                for file in files:
                    self.repo.head.reset(index=True, working_tree=False)
                    self.repo.git.add(file)

                    pattern = re.compile('(\w\w\d\d\w)_ue')
                    matches = pattern.search(file)
                    group_name = ''
                    if matches:
                        group_name = matches.group(1)
                    message = self.commit_message_line_edit.text().format(group_name=group_name)

                    self.repo.index.commit(message)
                self.repo.git.push()

            except:
                error = True

        if error:
            QMessageBox.about(self, 'Fehler', 'Es gab einen Fehler beim Committen der neuen Dateien. \n'
                              'Bitte kontrollieren Sie das Git-Repository manuell.')
        else:
            if self.list_widget.selectedItems():
                QMessageBox.about(self, 'Erfolgreich', 'Dateien erfolgreich committet.')

    def get_changed_or_untracked_files(self):
        """
        Returns a list of files, which have been modified or haven't been tracked yet.
        """
        self.repo.head.reset(index=True, working_tree=False)
        files = self.repo.untracked_files + [info.a_path for info in self.repo.index.diff(None)]
        return files
