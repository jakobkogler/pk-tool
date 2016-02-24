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

    def git_pull(self):
        """
        Try git pull. If error, set use-git in settings to False and print error-message.
        """
        pk_repo_path = self.settings.repo_path
        if pk_repo_path and self.settings.use_git:
            try:
                self.repo = git.Repo(pk_repo_path)
                o = self.repo.remotes.origin
                info = o.pull()[0]

                if info.flags & (git.FetchInfo.ERROR | git.FetchInfo.REJECTED):
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
