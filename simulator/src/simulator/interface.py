import random

class Interface:

    def __init__(self, network, radio_power=5):
        self.network = network
        # Attributes of the interface
        self.radio_power = radio_power
    
    def forward_data(self, data):
        self.network.send_data(data)
