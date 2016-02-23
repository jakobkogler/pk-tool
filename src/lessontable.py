from PyQt5.QtWidgets import QTableWidget


class LessonTable(QTableWidget):
    def __init__(self, widget):
        super().__init__(widget)
