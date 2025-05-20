import socket
import atexit
from pySC_server.send_receive import send_int, receive_nparray, receive_float

from PyQt6.QtWidgets import QTableWidgetItem
import time

class RingClient:
    def __init__(self, port):
        self.port = port
        #atexit.register(self.close)

    def bba(self, bpm=0, measurement=None, results=None):
        self.socket = socket.socket()
        self.socket.connect(('localhost', self.port))
        #message = 'Hi ring!'
        message = 'BBA'
        self.socket.sendall(message.encode()) #signal for bba
        ok = self.socket.recv(2)
        send_int(self.socket, bpm) 
        #self.socket.sendall(bpm.encode())
        try:
            bpm_pos_H = receive_nparray(self.socket)
            orbits_H = receive_nparray(self.socket)
            offset_H = receive_float(self.socket)
            offseterr_H = receive_float(self.socket)
            bpm_pos_V = receive_nparray(self.socket)
            orbits_V = receive_nparray(self.socket)
            offset_V = receive_float(self.socket)
            offseterr_V = receive_float(self.socket)
            print(f'BBA for BPM {bpm}:')
            print(f'\t H: {1e6*offset_H:.1f} +- {1e6*offseterr_H:.1f}')
            print(f'\t V: {1e6*offset_V:.1f} +- {1e6*offseterr_V:.1f}')
            self.socket.close()

            if measurement is not None:
                measurement.bba_plotH.plot_bba(bpm_pos_H, orbits_H)
                measurement.bba_plotV.plot_bba(bpm_pos_V, orbits_V)
                measurement.wait(10)

            if results is not None:
                results.setRowCount(bpm+1)
                results.setItem(bpm, 0, QTableWidgetItem(f'{1e6*offset_H:.1f} +- {1e6*offseterr_H:.1f} μm'))
                results.setItem(bpm, 1, QTableWidgetItem(f'{1e6*offset_V:.1f} +- {1e6*offseterr_V:.1f} μm'))
        except Exception as e:
            print(f'Error during BBA: {e}')
            self.socket.close()
            return

    def close(self):
        self.socket.close()
        print('Socket closed.')