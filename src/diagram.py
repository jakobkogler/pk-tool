from PyQt5.QtWidgets import QDialog, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import re


class DiagramDialog(QDialog):
    def __init__(self, parent=None, files=None):
        super(DiagramDialog, self).__init__(parent)

        self.files = files

        # a figure instance to plot on
        self.figure = plt.figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        if isinstance(self.files, dict):
            self.comparison()
        else:
            self.plot()

    def plot(self):
        data, labels = self.parse_files(self.files)

        # create an axis
        plt.figure()

        ax = self.figure.add_subplot(111)

        # discards the old graph
        ax.hold(False)

        # plot data
        #ax.plot(data, '*-')

        plt.bar(range(len(data)), data, align='center')
        plt.xticks(range(len(labels)), labels, size='small')


        ax.set_title('Anwesende Studenten pro Übung')

        ax.set_xlabel('Übungen')
        ax.set_ylabel('Anwesende Studenten')


        # refresh canvas
        self.canvas.draw()

    def comparison(self):
        all_data = []
        all_labels = set()

        for group_name, files in self.files.items():
            data, labels = self.parse_files(files)
            all_data.append((group_name, dict(zip(labels, data))))
            all_labels |= set(labels)

        all_labels = list(sorted(all_labels, key=lambda x: int(x[2:]) if x.startswith('ue') else -1))

        ax = self.figure.add_subplot(111)

        # discards the old graph
        ax.hold(False)

        extracted = []
        for group_name, d in all_data:
            tmp = [range(len(all_labels)), [d.get(key, 0) for key in all_labels]]
            #plt.plot(tmp[0], tmp[1], label=group_name)
            extracted += tmp
            #ax.plot(tmp[0], tmp[1], label=group_name)

        plt.plot(*extracted)
        plt.xticks(range(len(all_labels)), all_labels, size='small')


        ax.set_title('Anwesende Studenten pro Übung pro Gruppe')

        ax.set_xlabel('Übungen')
        ax.set_ylabel('Anwesende Studenten')

        plt.legend()

        self.canvas.draw()

    def parse_files(self, files):
        parsed = []
        for file in files:
            pattern = re.compile(r'ue\d+')
            match = pattern.search(file)
            name = match.group(0) if match else ''
            name[:2]
            number = int(name[2:]) if name else -1
            with open(file, 'r', encoding='utf-8') as f:
                count = sum(';an;' in line for line in f)
            parsed.append((number, name, count))
        data = []
        labels = []
        for number, name, count in sorted(parsed):
            data.append(count)
            labels.append(name)

        return data, labels
