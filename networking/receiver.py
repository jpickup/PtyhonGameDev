import pickle
from data import Data
from networking import Network

network = Network(12000)

while True:
    data = network.receive()
    print(data.toString())
