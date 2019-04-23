import logging
import random
import signal
from .node import Node
from .interface import Interface
from .network import Network

class Simulator:

    def __init__(self, mqtt_broker_address, latitude_range=(37.413, 37.417), longitude_range=(-122.080, -122.068), time_scale=1, num_nodes=10):
        self.latitude_range = latitude_range
        self.longitude_range = longitude_range
        self.time_scale = time_scale
        self.num_nodes = num_nodes
        self.mqtt_broker_address = mqtt_broker_address
        self.nodes = []
        self.network = None
        self.setup_nodes()
        self.setup_network()
    
    def activate_nodes(self):
        for node in self.nodes:
            logging.warning('Starting %s', node.node_id)
            node.start()
    
    def await_nodes(self):
        for node in self.nodes:
            node.join()
            logging.info('%s stopped', node.node_id)
    
    def stop_nodes(self):
        for node in self.nodes:
            logging.warning('Stopping %s', node.node_id)
            node.stop()
    
    def setup_nodes(self):
        for node_num in range(self.num_nodes):
            node_latitude = random.uniform(*self.latitude_range)
            node_longitude = random.uniform(*self.longitude_range)
            node_id = 'node-{node_num}'.format(node_num=node_num)
            self.nodes.append(
                Node(
                    node_id=node_id,
                    latitude=node_latitude,
                    longitude=node_longitude,
                    time_scale=self.time_scale
                )
            )
    
    def setup_network(self):
        if not self.nodes:
            raise Exception('Nodes not yet set up!')
        self.network = Network(self.mqtt_broker_address)
        for node in self.nodes:
            self.network.add_node(node)
        self.network.send_topology()
