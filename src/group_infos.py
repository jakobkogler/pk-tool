from collections import namedtuple
import re


GroupInfo = namedtuple('GroupInfo', 'instructor, tutor1, tutor2, substitute1, substitute2')


class GroupInfos:
    """Parses the file "GRUPPEN.txt" and stores the data for all student groups.
    This includes group, instructor and tutor names. """

    def __init__(self, path='', repo_path=''):
        if repo_path:
            path = repo_path + '/GRUPPEN.txt'

        # split file into parts
        file_parts = []

        try:
            with open(path, 'r', encoding='utf-8') as file:
                name_simple_regex = re.compile(r'\[.*\]')

                for line in file:
                    if (name_simple_regex.search(line)):
                        file_parts.append([])
                    if file_parts:
                        file_parts[-1].append(line)
        except IOError:
            pass

        # parse parts into group infos
        self.groups = dict()
        name_regex = re.compile(r'\[((mo|di|mi|do|fr)\d{2}\w)\]')

        for part in file_parts:
            match = name_regex.search(part[0])
            if match:
                group_name = match.group(1)
            else:
                continue

            info = dict()
            for line in part[1:]:
                for title in 'leiter tutor1 tutor2 ersatz1 ersatz2'.split():
                    if line.startswith(title) and '=' in line:
                        info[title] = line.split('=')[-1].strip()

            self.groups[group_name] = GroupInfo(instructor=info.get('leiter', ''),
                                                tutor1=info.get('tutor1', ''),
                                                tutor2=info.get('tutor2', ''),
                                                substitute1=info.get('ersatz1', ''),
                                                substitute2=info.get('ersatz2', ''))

    def tutor_names(self):
        groups = [[group.tutor1, group.tutor2, group.substitute1, group.substitute2] for group in self.groups.values()]
        names = set(name for group in groups for name in group)
        names.add('')
        return sorted(names)

    def get_group(self, group_name):
        return self.groups.get(group_name, GroupInfo(instructor='', tutor1='', tutor2='',
                                                     substitute1='', substitute2=''))

    def get_involved_groups(self, tutor_name):
        return [name for name, info in self.groups.items() if tutor_name in [info.tutor1, info.tutor2]]
