import socket
import pickle
from select import select

class Network():
    def __init__(self, port = 55000, group = '255.255.255.255'):
        self.multicast_port = port
        self.multicast_group = group 
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 1))  # connect() for UDP doesn't send packets
        self.local_ip = s.getsockname()[0]
        print(self.local_ip)
        self.sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sender_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sender_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sender_socket.settimeout(1.0)
        self.sender_socket.bind((self.local_ip, self.multicast_port))
        #self.receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        #self.receiver_socket.bind(('', self.multicast_port))
        self.receiver_socket = self.sender_socket
        
    def send(self, data):
        self.sender_socket.sendto(pickle.dumps(data), (self.multicast_group, self.multicast_port))

    def receive(self):
        message, address = self.receiver_socket.recvfrom(1024)
        if message is None:
            return None
        else:
            return pickle.loads(message)

    def has_data(self, timeout=0.001):
        ready = select([self.receiver_socket], [], [], timeout)
        return ready[0]

