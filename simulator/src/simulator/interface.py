
class Interface:

    def __init__(self, network, radio_power=5):
        self.radio_power = radio_power
        self.network = network
    
    def forward_data(self, data):
        self.network.send_data(data)
