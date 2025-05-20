import sys
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, QPushButton, QListWidget, QListWidgetItem, QAbstractItemView, QProgressBar, QTableWidget, QSizePolicy
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtCore import pyqtSignal, QObject, QThread, QCoreApplication, QElapsedTimer
from colors import DESYCyan, DESYOrange, Dunkelblau, Gelb, Dunkelrot, Petrol, Grun, Olive

import time

import numpy as np

from sector_cell_bpm_list import SectorCellBPMList
from selected_bpm_list import SelectedBPMList
from general import remove_selected, transfer_selection
from bba_worker import get_bba_thread, BBAplot, BBA_worker

app = QApplication([])

window = QWidget()

total_width = 1000
total_height = 800
# window.setStyleSheet(f'background-color: {Dunkelblau};'
#                      f'color: {Olive};')
window.setWindowTitle("Beam Based Alignment")
window.setGeometry(100, 100, 1000, 800)

layout = QGridLayout(parent=window)
window.setLayout(layout)

SCB = SectorCellBPMList(parent=window)


selBPM = SelectedBPMList(parent=window)
selectedBPMs = selBPM.selectedBPMs

number_of_BPMs = QLabel('BPMs: 0', parent=window)

set_selbpm_num = lambda : number_of_BPMs.setText(f"BPMs: {selectedBPMs.count()}")

button4 = QPushButton('Send to plan', parent=window) 
send_to_plan = lambda : transfer_selection(SCB.bpmList, selectedBPMs)
button4.clicked.connect(send_to_plan)
button4.clicked.connect(set_selbpm_num)


button5 = QPushButton('Remove selected', parent=window) 
button5.clicked.connect(lambda :remove_selected(selectedBPMs))
button5.clicked.connect(set_selbpm_num)

button6 = QPushButton('Run all', parent=window) 
button6.setStyleSheet(f'background-color: {Grun}; color: black;')

button7 = QPushButton('Remove all', parent=window) 
button7.clicked.connect(selectedBPMs.clear)
button7.clicked.connect(set_selbpm_num)
#button7.setStyleSheet(f'background-color: {Dunkelrot}; color: black;')

plot_window = QWidget(parent=window)
plot_layout = QGridLayout(parent=plot_window)
plot_window.setLayout(plot_layout)



bba_plotH = BBAplot(window)
bba_plotV = BBAplot(window)


progress_bar = QProgressBar(parent=window)
progress_bar.setMinimum(0)
progress_bar.setMaximum(1)
progress_bar.setFormat('%v/%m')
#progress_bar.setFormat(f"Running {selectedBPMs.item(row).text()}")
progress_bar.setTextVisible(True)

results = QTableWidget(parent=window)
results.setColumnCount(2)
results.setRowCount(1)


bba_thread = get_bba_thread(progress_bar, selectedBPMs, results, bba_plotH, bba_plotV)

button6.clicked.connect(progress_bar.reset)
button6.clicked.connect(bba_thread.start)
button6.clicked.connect(lambda : print('BBA thread started'))

pbutton = QPushButton('Plot', parent=window)
pbutton.clicked.connect(bba_plotH.plot)
pbutton.clicked.connect(bba_plotV.plot)

sp = QSizePolicy.Policy.Expanding
for qq in [bba_plotH.canvas, bba_plotH.toolbar, bba_plotV.canvas, bba_plotV.toolbar]:
    qq.setSizePolicy(sp, sp)
plot_layout.addWidget(bba_plotH.canvas, 0, 0, 1, 1)
plot_layout.addWidget(bba_plotH.toolbar, 1, 0, 1, 1)
plot_layout.addWidget(bba_plotV.canvas, 0, 1, 1, 1)
plot_layout.addWidget(bba_plotV.toolbar, 1, 1, 1, 1)



connect_button = QPushButton('Disable')
connect_button.clicked.connect(lambda : selBPM.selectedBPMs.setDisabled(True))

run_thread_button = QPushButton('Empty')
#run_thread_button.clicked.connect(worker_thread.start)

## Master Layout

layout.addWidget(SCB, 0, 0, *SCB.layout_args)

for qq in [SCB, number_of_BPMs, button4, selectedBPMs, button5, button6, button7, results, plot_window, pbutton, connect_button, progress_bar]:
    qq.setSizePolicy(sp, sp)
for qq in [results]:
    qq.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

layout.addWidget(number_of_BPMs, 3, 0, 1, 1)
layout.addWidget(button4, 3, 4, 1, 1)

layout.addWidget(selectedBPMs, 4, 0, 1, 1)
layout.addWidget(button5, 5, 0, 1, 1)
layout.addWidget(button6, 7, 0, 1, 1)
layout.addWidget(button7, 6, 0, 1, 1)
layout.addWidget(results, 4, 1, 1, 1)
layout.addWidget(plot_window, 4, 2, 1, 3)

layout.addWidget(pbutton, 7, 1, 1, 1)
layout.addWidget(connect_button, 7, 2, 1, 1)
layout.addWidget(run_thread_button, 7, 3, 1, 1)

layout.addWidget(progress_bar, 8, 0, 1, 6)
window.show()
sys.exit(app.exec())