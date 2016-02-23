from PyQt5.QtCore import QSettings


class Settings:
    def __init__(self):
        self.settings = QSettings('settings.ini', QSettings.IniFormat)
        self.key_defaults = {'repo-path': ('Path/pk_repo', ''),
                                'use-git': ('Git/use_git', 'False'),
                                'username': ('Personal/username', '')}

    def get_repo_path(self):
        return self.__get_value('repo-path')

    def set_repo_path(self, repo_path):
        self.__set_value('repo-path', repo_path)

    def get_use_git(self):
        return self.__get_value('use-git') == 'True'

    def set_use_git(self, use_git):
        self.__set_value('use-git', 'True' if use_git else 'False')

    def get_username(self):
        return self.__get_value('username')

    def set_username(self, username):
        self.__set_value('username', username)

    def __get_value(self, short_key):
        key, default = self.key_defaults[short_key]
        return self.settings.value(key, default)

    def __set_value(self, short_key, value):
        key, _ = self.key_defaults[short_key]
        self.settings.setValue(key, value)
