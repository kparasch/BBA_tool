from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton, QListWidget, QListWidgetItem, QAbstractItemView, QProgressBar
from PyQt6.QtWidgets import QHBoxLayout
from general import select_all
import json

class SectorCellBPMList(QWidget):

    row = 0
    column = 0
    rowSpan = 3
    columnSpan = 3

    min_width = 0.16
    min_height = 0.18

    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout_args = [self.rowSpan, self.columnSpan]
        #self.layout_args = [self.row, self.column, self.rowSpan, self.columnSpan]

        self.bpm_conf = json.load(open('petra4_bpm_conf.json','r'))
        self.sectors = list(self.bpm_conf.keys())


        # lists
        self.sectorList = QListWidget(parent=self)
        self.sectorList.insertItems(0, self.sectors)

        self.cellList = QListWidget(parent=self)

        self.bpmList = QListWidget(parent=self)

        self.layout = QGridLayout(self)
        self.layout.addWidget(self.sectorList, 0, 0)
        self.layout.addWidget(self.cellList, 0, 1)
        self.layout.addWidget(self.bpmList, 0, 2)

        self.sectorList.itemSelectionChanged.connect(self.update_cell_list)
        self.cellList.itemSelectionChanged.connect(self.update_bpm_list)
        
        for thisList in self.sectorList, self.cellList, self.bpmList:
            thisList.setMinimumSize(int(self.min_width*parent.width()), int(self.min_height*parent.height()))
            thisList.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)

        # buttons
        self.button_selall_sectors = QPushButton('Select all', parent=self) 
        self.layout.addWidget(self.button_selall_sectors, 1, 0)
        self.button_selall_sectors.clicked.connect(lambda : select_all(self.sectorList))

        self.button_selall_cells = QPushButton('Select all', parent=self)
        self.layout.addWidget(self.button_selall_cells, 1, 1)
        self.button_selall_cells.clicked.connect(lambda : select_all(self.cellList))

        self.button_selall_bpms = QPushButton('Select all', parent=self)
        self.layout.addWidget(self.button_selall_bpms, 1, 2)
        self.button_selall_bpms.clicked.connect(lambda : select_all(self.bpmList))


    def update_cell_list(self):
        # cellList.clear()
        for i in range(self.cellList.count()-1, -1, -1):
            self.cellList.takeItem(i)
    
        row = 0
        for item in self.sectorList.selectedItems():
            sector = item.text()
            for cell in self.bpm_conf[sector].keys():
                self.cellList.insertItem(row, f'{sector}/{cell}')
                row += 1

    def update_bpm_list(self):
        self.bpmList.clear()

        my_items = [] 
        for item in self.cellList.selectedItems():
            itemtext = item.text()
            se, ce = itemtext.split('/')
            for bpm in self.bpm_conf[se][ce].keys():
                my_items.append(f"{itemtext}/{bpm}")
        self.bpmList.insertItems(0, my_items)
