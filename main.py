import sys
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, QPushButton, QProgressBar, QTableWidget, QSizePolicy
from PyQt6.QtWidgets import QTableWidgetItem
from colors import DESYCyan, DESYOrange, Dunkelblau, Gelb, Dunkelrot, Petrol, Grun, Olive


from sector_cell_bpm_list import SectorCellBPMList
from selected_bpm_list import SelectedBPMList
from general import remove_selected, transfer_selection
from bba_worker import get_bba_thread, BBAplot

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

button_send_to_plan = QPushButton('Send to plan', parent=window) 
send_to_plan = lambda : transfer_selection(SCB.bpmList, selectedBPMs)
button_send_to_plan.clicked.connect(send_to_plan)
button_send_to_plan.clicked.connect(set_selbpm_num)


button5 = QPushButton('Remove selected', parent=window) 
button5.clicked.connect(lambda :remove_selected(selectedBPMs))
button5.clicked.connect(set_selbpm_num)

button6 = QPushButton('Run all', parent=window) 
button6.setStyleSheet(f'background-color: {Grun}; color: black;')

button7 = QPushButton('Remove all', parent=window) 
button7.clicked.connect(selectedBPMs.clear)
button7.clicked.connect(set_selbpm_num)
#button7.setStyleSheet(f'background-color: {Dunkelrot}; color: black;')



bba_plotH = BBAplot(window)
bba_plotV = BBAplot(window)


progress_bar = QProgressBar(parent=window)
progress_bar.setMinimum(0)
progress_bar.setMaximum(1)
progress_bar.setFormat('%v/%m')
#progress_bar.setFormat(f"Running {selectedBPMs.item(row).text()}")
progress_bar.setTextVisible(True)

results = QTableWidget(parent=window)
results.setMinimumWidth(430)
results.setMinimumHeight(300)
results.setColumnCount(3)
results.setHorizontalHeaderLabels(['Name', 'Horizontal [μm]', 'Vertical [μm]'])
results.setColumnWidth(0, 160)
results.setColumnWidth(1, 110)
results.setColumnWidth(2, 110)

# for size testing
# results.setRowCount(790)
# results.setItem(0, 0, QTableWidgetItem('SSS_SO/R/BPM_SOR_10'))
# results.setItem(0, 1, QTableWidgetItem('1000.0 ± 100.0'))
# results.setItem(0, 2, QTableWidgetItem('1000.0 ± 100.0'))

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


## Plots layout
plot_window = QWidget(parent=window)
plot_layout = QGridLayout(parent=plot_window)
plot_window.setLayout(plot_layout)

plot_layout.addWidget(bba_plotH.canvas, 0, 0, 1, 1)
plot_layout.addWidget(bba_plotH.toolbar, 1, 0, 1, 1)
plot_layout.addWidget(bba_plotV.canvas, 2, 0, 1, 1)
plot_layout.addWidget(bba_plotV.toolbar, 3, 0, 1, 1)



connect_button = QPushButton('Disable')
connect_button.clicked.connect(lambda : selBPM.selectedBPMs.setDisabled(True))

#run_thread_button = QPushButton('Empty')
#run_thread_button.clicked.connect(worker_thread.start)

## Master Layout

layout.addWidget(SCB, 0, 0, *SCB.layout_args)

for qq in [SCB, number_of_BPMs, button_send_to_plan, selectedBPMs, button5, button6, button7, results, plot_window, pbutton, connect_button, progress_bar]:
    qq.setSizePolicy(sp, sp)
for qq in [results]:
    qq.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

layout.addWidget(number_of_BPMs, 3, 0, 1, 1)
layout.addWidget(button_send_to_plan, 3, 2, 1, 1)

layout.addWidget(selectedBPMs, 4, 0, 1, 1)
layout.addWidget(button5, 5, 0, 1, 1)
layout.addWidget(button6, 7, 0, 1, 1)
layout.addWidget(button7, 6, 0, 1, 1)
layout.addWidget(results, 4, 1, 1, 2)
layout.addWidget(plot_window, 0, 3, 9, 1)

layout.addWidget(pbutton, 7, 1, 1, 1)
layout.addWidget(connect_button, 7, 2, 1, 1)
#layout.addWidget(run_thread_button, 7, 3, 1, 1)

layout.addWidget(progress_bar, 8, 0, 1, 3)
window.show()
sys.exit(app.exec())