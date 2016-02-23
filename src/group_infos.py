import re
from src.group import Group
from collections import namedtuple


Student = namedtuple('Student', 'name matrikelnr email group_name')


class GroupInfos:
    def __init__(self, repo_path=''):
        self.repo_path = repo_path
        self.groups = dict()

        self.__read_group_infos()
        self.__read_student_lists()

    def tutor_names(self):
        """Returns a list of the names of all tutors"""
        groups = [[group.tutor1, group.tutor2, group.substitute1, group.substitute2] for group in self.groups.values()]
        names = set(name for group in groups for name in group)
        names.add('')
        return sorted(names)

    def get_group_info(self, group_name):
        """Returns the info for a specific group"""
        if group_name not in self.groups:
            self.groups[group_name] = Group(group_name)
        return self.groups[group_name]

    def get_involved_groups(self, tutor_name):
        """Returns a list of names of all groups a tutor is involved in"""
        return [name for name, info in self.groups.items() if tutor_name in [info.tutor1, info.tutor2]]

    def get_group_names(self, allowed_types=None):
        if allowed_types:
            return [name for name, group in self.groups.items() if group.group_type in allowed_types]
        else:
            return [name for name in self.groups]

    @staticmethod
    def __split_file_into_parts(self, filename, regex):
        file_parts = []

        try:
            with open(filename, 'r', encoding='utf-8') as file:
                for line in file:
                    if regex.search(line):
                        file_parts.append([])
                    if file_parts:
                        file_parts[-1].append(line)
        except IOError:
            pass

        return file_parts

    def __read_group_infos(self):
        """Parses the file "GRUPPEN.txt" and stores the data for all student groups.
        This includes group, instructor and tutor names. """

        path = self.repo_path + '/GRUPPEN.txt'
        name_regex = re.compile(r'\[((mo|di|mi|do|fr)\d{2}\w)\]')
        name_simple_regex = re.compile(r'\[.*\]')

        for part in self.__split_file_into_parts(path, name_simple_regex):
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

            self.groups[group_name] = Group(name=group_name,
                                            instructor=info.get('leiter', ''),
                                            tutor1=info.get('tutor1', ''),
                                            tutor2=info.get('tutor2', ''),
                                            substitute1=info.get('ersatz1', ''),
                                            substitute2=info.get('ersatz2', ''))

    def __read_student_lists(self):
        """Reads the files 'groups_fortgeschritten.txt' und 'groups_normal.txt',
        and extracts all groups and student data."""

        path_template = self.repo_path + '/Anwesenheiten/Anmeldung/groups_{group_type}.txt'
        group_name_regex = re.compile('(mo|di|mi|do|fr)\d{2}\w')
        student_regex = re.compile('\s+[+✔]\s+(\D+)\s(\d+)\s(.*)\s?')

        for group_type in ['fortgeschritten', 'normal']:
            path = path_template.format(group_type=group_type)
            for part in self.__split_file_into_parts(path, group_name_regex):
                group_name = group_name_regex.search(part[0]).group(0)
                group = self.get_group_info(group_name)
                group.group_type = group_type

                for line in part[1:]:
                    match = student_regex.search(line)
                    if match:
                        group.add_student(Student(*([match.group(i) for i in range(1, 4)] + [group_name])))
