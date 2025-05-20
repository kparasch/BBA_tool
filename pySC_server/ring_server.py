import socket
import numpy as np
import atexit
from send_receive import send_nparray, receive_nparray, receive_int, send_float
from init_sc import initSC, do_BBA

s = socket.socket()

SC = initSC()


HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 13131  # Port to listen on (non-privileged ports are > 1023)

bpm_data = np.array([1, 2, 3, 4, 5], dtype=np.float64)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("Socket successfully created")
    atexit.register(s.close)
    while True:
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
 #           while True:
            data = conn.recv(1024)
            signal = data.decode()
            print(signal, len(signal))
            if len(signal) > 2 and signal[:3] == 'BBA':
                print('Got BBA signal')
                conn.sendall(b'OK')
                bpm_index = receive_int(conn)
                print(f'Running BBA for BPM {bpm_index}')
                bps, orbits, offsets, offset_errors = do_BBA(SC, bpm_index)
                bps_H = bps[0]
                bps_V = bps[1]
                orbits_H = orbits[0]
                orbits_V = orbits[1]
                offset_H = offsets[0][0]
                offset_V = offsets[1][0]
                offseterr_H = offset_errors[0][0]
                offseterr_V = offset_errors[1][0]

                send_nparray(conn, bps_H)
                send_nparray(conn, orbits_H)
                send_float(conn, offset_H)
                send_float(conn, offseterr_H)
                send_nparray(conn, bps_V)
                send_nparray(conn, orbits_V)
                send_float(conn, offset_V)
                send_float(conn, offseterr_V)


            # print(f'Running BBA for BPM {data.decode()}')
            if not data:
                break
            send_nparray(conn, bpm_data)
            #conn.sendall('Got everything!'.encode())
            #conn.sendall(data)

