
from PyQt6.QtWidgets import QWidget, QAbstractItemView, QGridLayout, QPushButton, QListWidget, QSizePolicy
from PyQt6.QtWidgets import QVBoxLayout


class SelectedBPMList:

    #row = 0
    #rowSpan = 1

    def __init__(self, parent=None):
        #super().__init__(parent)
        self.selectedBPMs = QListWidget(parent=parent)
        self.selectedBPMs.setMinimumSize(int(0.17*parent.width()), int(0.4*parent.height()))
        self.selectedBPMs.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.selectedBPMs.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.MinimumExpanding)