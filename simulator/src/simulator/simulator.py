import logging
import random
import signal
from .node import Node
from .interface import Interface
from .network import Network

class Simulator:

    def __init__(self, mqtt_broker_address, length=1000, width=1000, time_scale=1, max_nodes=30):
        self.length = length
        self.width = width
        self.time_scale = time_scale
        self.max_nodes = max_nodes
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
        for node_num in range(self.max_nodes):
            node_latitude = random.randint(0, self.length)
            node_longitude = random.randint(0, self.width)
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
