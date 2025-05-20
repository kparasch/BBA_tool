from PyQt6.QtCore import pyqtSignal, QObject, QThread, QCoreApplication, QElapsedTimer, pyqtSlot
from PyQt6.QtWidgets import QTableWidgetItem

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar

from pySC_client import RingClient

class BBA_measurement(QObject):
    done = pyqtSignal(int)
    plot = pyqtSignal()

    def __init__(self, progress, bba_plotH, bba_plotV):
        super().__init__()
        self.done.connect(progress.setValue)
        self.bba_plotH = bba_plotH
        self.bba_plotV = bba_plotV
        # self.plot.connect(bba_plotH.plot)
        # self.plot.connect(bba_plotV.plot)
    
    def request(self, bpm_name, number):
        self.name = bpm_name
        self.number = number
        # self.wait(100)
        self.done.emit(self.number+1)
        self.plot.emit()
    
    def wait(self, ms):
        timer = QElapsedTimer()
        timer.start()
        while timer.elapsed() < ms:
            QCoreApplication.processEvents()

class BBA_worker(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, progress_bar, selectedBPMs, results, bba_plotH, bba_plotV):
        super().__init__()
        self.progress_bar = progress_bar
        self.selectedBPMs = selectedBPMs
        self.results = results
        self.bba_plotH = bba_plotH
        self.bba_plotV = bba_plotV
        self.ring_client = RingClient(13131)
        print('BBA worker initialized')

    @pyqtSlot()
    def run_all(self):
        self.selectedBPMs.setEnabled(False)
        print('Starting measurement!!')
        n_bpms = self.selectedBPMs.count()

        self.results.setRowCount(n_bpms)
        for row in range(n_bpms):
            self.results.setItem(row, 0, QTableWidgetItem(self.selectedBPMs.item(row).text()))
            self.results.setItem(row, 1, QTableWidgetItem('          '))
            self.results.setItem(row, 2, QTableWidgetItem('          '))

        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(n_bpms)
        measurement = BBA_measurement(self.progress_bar, self.bba_plotH, self.bba_plotV)
    
        for row in range(n_bpms):
            print('Doing BBA for BPM', row)
            bpm = self.selectedBPMs.item(row).text()
            bpm_index = row ### fake
            self.ring_client.bba(bpm_index, measurement, self.results)
            measurement.done.emit(row + 1)
            measurement.wait(10)
        self.finished.emit()
        self.selectedBPMs.setEnabled(True)

def get_bba_thread(progress_bar, selectedBPMs, results, bba_plotH, bba_plotV):
    """
    Create a BBA worker thread.
    """
    bba_thread = QThread()
    print('BBA thread initialized')
    worker = BBA_worker(progress_bar, selectedBPMs, results, bba_plotH, bba_plotV)
    worker.moveToThread(bba_thread)
    bba_thread.started.connect(worker.run_all)
    worker.finished.connect(bba_thread.quit)
    bba_thread.destroyed.connect(lambda : print('BBA thread destroyed'))
    worker.destroyed.connect(lambda : print('BBA worker destroyed'))
    bba_thread.worker = worker ### attach worker to thread so that it is not garbage collected
    return bba_thread

class BBAplot:
    def __init__(self, window):
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, window)

    def plot(self):
        ''' plot some random stuff '''
        # random data
        data1 = [np.random.random() for i in range(10)]
        data2 = [np.random.random() for i in range(10)]
        self.figure.clear()
        ax1 = self.figure.add_subplot(211)
        ax2 = self.figure.add_subplot(212)
        ax1.plot(data1, '*-')
        ax2.plot(data2, '*-')

        # refresh canvas
        self.canvas.draw()

    def plot_bba(self, bps, orbits):
        ''' plot BBA '''

        cols = ['r', 'b']
        self.figure.clear()
        ax1 = self.figure.add_subplot(211)
        ax2 = self.figure.add_subplot(212)
        ax1.plot(np.arange(5), np.zeros(5), '*-')
        for k1_step in range(orbits.shape[1]):
            for bpi in range(orbits.shape[2]):
                ax2.plot(bps[:,k1_step]*1e6, orbits[:, k1_step, bpi]*1e6, '.-', c=cols[k1_step], lw=0.5, alpha=0.3 )
        ax2.set_xlabel('BPM position [μm]')
        ax2.set_ylabel('Orbit modulation [μm]')

        # refresh canvas
        self.canvas.draw()