from collections import namedtuple
import re


GroupInfo = namedtuple('GroupInfo', 'instructor, tutor1, tutor2')


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
            name_regex = re.compile(r'(mo|di|mi|do|fr)\d{2}\w')
            for part in file_parts:
                match = name_regex.search(line)
                if match:
                    group_name = match.group(0)
                else:
                    continue

                group = GroupInfo(instructor='', tutor1='', tutor2='')
                for line in part[1:]:
                    extract_name = lambda: line.split('=')[-1].strip()
                    if line.startswith('leiter'):
                        group.instructor = extract_name()
                    if line.startswith('tutor1'):
                        group.tutor1 = extract_name()
                    if line.startswith('tutor2'):
                        group.tutor2 = extract_name()

                self.groups[group_name] = group
