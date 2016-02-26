from PyQt5.QtWidgets import QMessageBox
import sys

try:
    import git
except ImportError:
    pass


class GitInteractions:
    """
    Handles all git interactions
    """

    def __init__(self, settings, action_commit_and_push):
        """
        Pass over parameters to instance, try to load git
        """
        self.settings = settings
        self.action_commit_and_push = action_commit_and_push
        self.repo = None

        if 'git' not in sys.modules:
            self.settings.use_git = False

    def pull_and_react(self):
        """
        Try git pull. If error, set use-git in settings to False and print error-message.
        """
        if self.settings.use_git:
            success = self.pull()
            if not success:
                self.settings.use_git = False
                QMessageBox.about(None, 'Fehler', 'Es gab einen Fehler beim Pullen des Git-Repos. \n'
                                  'Git-Interaktionen wurden für diese Session ausgeschaltet.')

            if self.settings.use_git:
                self.action_commit_and_push.setEnabled(True)
            else:
                self.action_commit_and_push.setDisabled(True)
        else:
            self.action_commit_and_push.setDisabled(True)

    def pull(self):
        """
        Try git pull. Return a boolean indicating success or failure.
        """
        pk_repo_path = self.settings.repo_path
        if pk_repo_path and self.settings.use_git:
            try:
                self.repo = git.Repo(pk_repo_path)
                o = self.repo.remotes.origin
                info = o.pull()[0]
                return not (info.flags & (git.FetchInfo.ERROR | git.FetchInfo.REJECTED))
            except:
                return False
        return False

    def commit_file(self, file, message):
        """
        Try commiting a file. Return a boolean indicating success or failure.
        """
        try:
            self.repo.head.reset(index=True, working_tree=False)
            self.repo.git.add(file)

            self.repo.index.commit(message)
            return True
        except:
            return False

    def push(self):
        """
        Try git push. Return a boolean indicating success or failure.
        """
        try:
            self.repo.git.push()
            return True
        except:
            return False

    def get_changed_or_untracked_files(self):
        """
        Returns a list of files, which have been modified or haven't been tracked yet.
        """
        self.repo.head.reset(index=True, working_tree=False)
        files = self.repo.untracked_files + [info.a_path for info in self.repo.index.diff(None)]
        return files
