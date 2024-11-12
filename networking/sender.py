import time
from data import Data
from networking import Network

network = Network(12000)

idx = 0    
while True:
    idx += 1
    msg = "Hello world! " + str(idx)
    data = Data(msg)
    network.send(data)
    print(str(idx))
    time.sleep(1)