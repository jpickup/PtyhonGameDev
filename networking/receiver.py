import socket
import pickle
from data import Data

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('', 12000))

while True:
    message, address = server_socket.recvfrom(1024)
    data = pickle.loads(message)
    print(data.toString())
