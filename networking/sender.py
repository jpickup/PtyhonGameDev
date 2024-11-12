import time
import socket
from data import Data
import pickle
multicast_group = '255.255.255.255' 
multicast_port = 55000
MULTICAST_TTL = 32
sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)#, socket.IPPROTO_UDP)
#sender_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)
sender_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sender_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

sender_socket.settimeout(1.0)
addr = (multicast_group, multicast_port)

idx = 0    
while True:
    idx += 1
    msg = "Hello world! " + str(idx)
    data = Data(msg)

    start = time.time()
    sender_socket.sendto(pickle.dumps(data), addr)
    print(str(idx))
    time.sleep(1)