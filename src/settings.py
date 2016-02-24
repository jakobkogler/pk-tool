from PyQt5.QtCore import QSettings


class Settings:
    """
    Enables easy reading and writing of settings-information
    """

    def __init__(self):
        """
        Connect to the settings-file.
        """
        self.settings = QSettings('settings.ini', QSettings.IniFormat)
        self.key_defaults = {'repo-path': ('Path/pk_repo', ''),
                                'use-git': ('Git/use_git', 'False'),
                                'username': ('Personal/username', '')}

    @property
    def repo_path(self):
        """
        Returns the path to the pk-repo
        """
        return self.__get_value('repo-path')

    @repo_path.setter
    def repo_path(self, repo_path):
        """
        Sets the path to the pk-repo
        """
        self.__set_value('repo-path', repo_path)

    @property
    def use_git(self):
        """
        Returns a boolean, which tells if git-interactions are enabled.
        """
        return self.__get_value('use-git') == 'True'

    @use_git.setter
    def use_git(self, use_git):
        """
        Enables or disables the git-interactions
        """
        self.__set_value('use-git', 'True' if use_git else 'False')

    @property
    def username(self):
        """
        Returns the username of the tutor
        """
        return self.__get_value('username')

    @username.setter
    def username(self, username):
        """
        Sets the username of the tutor
        """
        self.__set_value('username', username)

    def __get_value(self, short_key):
        """
        Gets a value from the settings-file
        """
        key, default = self.key_defaults[short_key]
        return self.settings.value(key, default)

    def __set_value(self, short_key, value):
        """
        Sets a value in the settings file
        """
        key, _ = self.key_defaults[short_key]
        self.settings.setValue(key, value)
