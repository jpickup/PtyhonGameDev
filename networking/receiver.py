import socket
import pickle
import struct
from data import Data

multicast_port = 55000

receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
receiver_socket.bind(('', multicast_port))

while True:
    message, address = receiver_socket.recvfrom(1024)
    data = pickle.loads(message)
    print("Message from " + str(address))
    print(data.toString())
