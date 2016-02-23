from PyQt5.QtCore import QSettings


class Settings:
    def __init__(self):
        self.settings = QSettings('settings.ini', QSettings.IniFormat)
        self.key_defaults = {'repo-path': ('Path/pk_repo', ''),
                                'use-git': ('Git/use_git', 'False'),
                                'username': ('Personal/username', '')}

    @property
    def repo_path(self):
        return self.__get_value('repo-path')

    @repo_path.setter
    def repo_path(self, repo_path):
        self.__set_value('repo-path', repo_path)

    @property
    def use_git(self):
        return self.__get_value('use-git') == 'True'

    @use_git.setter
    def use_git(self, use_git):
        self.__set_value('use-git', 'True' if use_git else 'False')

    @property
    def username(self):
        return self.__get_value('username')

    @username.setter
    def username(self, username):
        self.__set_value('username', username)

    def __get_value(self, short_key):
        key, default = self.key_defaults[short_key]
        return self.settings.value(key, default)

    def __set_value(self, short_key, value):
        key, _ = self.key_defaults[short_key]
        self.settings.setValue(key, value)
