from collections import namedtuple
import re


GroupInfo = namedtuple('GroupInfo', 'instructor, tutor1, tutor2, substitute1, substitute2')


class GroupInfos:
    """Reads and stores meta-data for all student groups.
    This includes names, instructor and tutor names. """

    def __init__(self, path):
        self.groups = dict()

        with open(path, 'r', encoding='utf-8') as file:
            # split file into parts
            file_parts = []
            name_simple_regex = re.compile(r'\[.*\]')

            for line in file:
                if (name_simple_regex.search(line)):
                    file_parts.append([])
                if file_parts:
                    file_parts[-1].append(line)

            # parse parts into group infos
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
                        if line.startswith(title):
                            info[title] = line.split('=')[-1].strip()

                self.groups[group_name] = GroupInfo(instructor=info.get('leiter', ''),
                                                    tutor1=info.get('tutor1', ''),
                                                    tutor2=info.get('tutor2', ''),
                                                    substitute1=info.get('ersatz1', ''),
                                                    substitute2=info.get('ersatz2', ''))

    def get_group_infos(self):
        return self.groups

    def tutor_names(self):
        extracted = [[group.tutor1, group.tutor2, group.substitue1, group.substitue2] for group in self.groups.values()]
        names = set(name for group in extracted for name in group)
        names.add('')
        return sorted(names)
