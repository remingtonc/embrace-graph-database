import operator
import math
import json
import logging
import random
from geopy.distance import distance
from .interface import Interface
from paho.mqtt.client import Client

class Network:

    def __init__(self, mqtt_broker_address, mqtt_port=1883, mqtt_timeout=60):
        self.nodes = []
        self.node_graph = self.__compute_node_graph()
        self.mqtt_client = Client()
        self.mqtt_client.on_connect = self.__mqtt_on_connect
        self.mqtt_client.on_message = self.__mqtt_on_message
        self.mqtt_client.connect(mqtt_broker_address, mqtt_port, mqtt_timeout)

    def __compute_node_graph(self):
        node_graph = {}
        for node in self.nodes:
            adjacent_nodes = self.__compute_adjacent_nodes(node)
            for _node in adjacent_nodes:
                node_pair = (node.node_id, _node.node_id)
                if node_pair in node_graph.keys():
                    continue
                edge = {
                    'distance': self.__compute_node_distance(node, _node),
                    'radio_power': node.interface.radio_power
                }
                node_graph[node_pair] = edge
        return node_graph

    def __compute_node_distance(self, first_node, second_node):
        return distance(
            (first_node.latitude, first_node.longitude),
            (second_node.latitude, second_node.longitude)
        ).miles

    def __compute_adjacent_nodes(self, node):
        adjacent_nodes = []
        for _node in self.nodes:
            if node.node_id == _node.node_id:
                continue
            if node.interface.radio_power < self.__compute_node_distance(node, _node):
                continue
            adjacent_nodes.append(_node)
        return adjacent_nodes

    def add_node(self, node):
        interface = Interface(self, random.randint(1, 5))
        node.set_interface(interface)
        self.nodes.append(node)
        self.node_graph = self.__compute_node_graph()

    def get_serializable_graph(self):
        node_graph = []
        for node_pair, edge in self.node_graph.items():
            from_node, to_node = node_pair
            connection = {
                'from_node': from_node,
                'to_node': to_node,
                'edge': edge
            }
            node_graph.append(connection)
        return node_graph

    def send_topology(self):
        self.publish_mqtt('topology', json.dumps(self.get_serializable_graph()), retain=True)

    def send_data(self, data):
        self.publish_mqtt('sensors', json.dumps(data))

    def publish_mqtt(self, sub_topic, message, base_topic='embrace', retain=False):
        topic_name = '{base_topic}/{sub_topic}'.format(base_topic=base_topic, sub_topic=sub_topic)
        self.mqtt_client.publish(topic_name, message, retain=retain)

    def __mqtt_on_connect(self, client, userdata, flags, rc):
        logging.warn('Connected to MQTT broker with result code %d.', rc)

    def __mqtt_on_message(self, client, userdata, msg):
        logging.debug('%s %s', msg.topic, msg.payload)
