import time
import socket
from data import Data
import pickle
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(1.0)

while True:
    msg = input("Please enter the message:\n")
    addr = ("127.0.0.1", 12000)
    data = Data(msg)

    start = time.time()
    client_socket.sendto(pickle.dumps(data), addr)