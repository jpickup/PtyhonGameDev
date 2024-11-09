import socket
import pickle
import struct
from data import Data

multicast_group = '224.1.1.1' 
multicast_port = 12000

receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
try:
    receiver_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
except AttributeError:
    pass
receiver_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)
receiver_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)

receiver_socket.bind((multicast_group, multicast_port))
host = socket.gethostbyname(socket.gethostname())
receiver_socket.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_IF, socket.inet_aton(host))
receiver_socket.setsockopt(socket.SOL_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton(multicast_group) + socket.inet_aton(host))

while True:
    message, address = receiver_socket.recvfrom(1024)
    data = pickle.loads(message)
    print("Message from " + str(address))
    print(data.toString())
