import time
from data import Data
from networking import Network

network = Network()
while True:
    if network.has_data():
        data = network.receive()
        if not(data is None) and data.isValid():
            print(data.toString())
    else:
        time.sleep(0.01)
