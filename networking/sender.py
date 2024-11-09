import time
import socket
from data import Data
import pickle
multicast_group = '224.1.1.1' 
multicast_port = 12000
MULTICAST_TTL = 32
sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sender_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)
sender_socket.settimeout(1.0)
addr = (multicast_group, multicast_port)
    
while True:
    msg = "Hello world!"
    data = Data(msg)

    start = time.time()
    sender_socket.sendto(pickle.dumps(data), addr)
    time.sleep(1)