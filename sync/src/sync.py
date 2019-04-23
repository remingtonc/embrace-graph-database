#!/usr/bin/env python
import logging
import json
import socket
import time
import datetime
from urllib.parse import urlparse
from paho.mqtt.client import Client as MQTTClient
from influxdb import InfluxDBClient
from arango import ArangoClient
import geohash2

mqtt_client = None
influxdb_client = None
topology_graph = None
topology_node_references = {}

def await_netloc(host, port, interval=3):
    """Await a certain URL to be open.
    url expects a port parameter in url string.
    Adapted from:
    http://code.activestate.com/recipes/576655-wait-for-network-service-to-appear/
    """
    sock = socket.socket()
    sock.settimeout(1)
    connected = False
    while not connected:
        try:
            sock.connect((host, port))
        except Exception:
            time.sleep(interval)
        else:
            sock.close()
            connected = True

def mqtt_on_connect(client, userdata, flags, rc):
    logging.info('Connected with result code %d.', rc)
    client.subscribe('embrace/#')

def mqtt_on_message_sensor(client, userdata, msg):
    sensor_data = json.loads(msg.payload)
    required_fields = {'battery', 'temperature', 'air_quality', 'radio_power'}
    required_tags = {'id'}
    geohash = geohash2.encode(sensor_data['latitude'], sensor_data['longitude'])
    influx_datapoints = []
    for field in required_fields:
        influx_datapoint = {
            'measurement': field,
            'tags': {
                **{tag: sensor_data[tag] for tag in required_tags},
                'geohash': geohash
            },
            'time': int(sensor_data['time']),
            'fields': {'value': sensor_data[field]}
        }
        influx_datapoints.append(influx_datapoint)
    influxdb_client.write_points(influx_datapoints, time_precision='s')
    if not sensor_data['id'] in topology_node_references.keys():
        logging.error('%s not yet in topology!', sensor_data['id'])
    else:
        topology_graph.update_vertex(
            {
                '_id': topology_node_references[sensor_data['id']]['_id'],
                'coordinate': [sensor_data['latitude'], sensor_data['longitude']],
                'geohash': geohash,
                **{field: sensor_data[field] for field in required_fields}
            }
        )

def mqtt_on_message_topology(client, userdata, msg):
    logging.warning('Received new topology!')
    global topology_node_references
    topology_data = json.loads(msg.payload)
    for connection in topology_data:
        first_node = connection['first_node']
        second_node = connection['second_node']
        edge = connection['edge']
        if first_node not in topology_node_references.keys():
            topology_node_references[first_node] = topology_graph.insert_vertex(
                'Nodes', {'_key': first_node}
            )
        if second_node not in topology_node_references.keys():
            topology_node_references[second_node] = topology_graph.insert_vertex(
                'Nodes', {'_key': second_node}
            )
        topology_graph.link(
            'Connections',
            topology_node_references[first_node]['_id'],
            topology_node_references[second_node]['_id'],
            data=edge
        )

def ensure_influxdb(host, port, username='devnet', password='create', database='embrace'):
    await_netloc(host, port)
    connected = False
    influxdb_client = None
    while not connected:
        try:
            influxdb_client = InfluxDBClient(host, username=username, password=password, database=database)
        except:
            time.sleep(3)
        else:
            connected = True
    try:
        influxdb_client.drop_database(database)
    except:
        pass
    influxdb_client.create_database(database)
    return influxdb_client

def ensure_arangodb(host, port, username='root', password='devnet', database='embrace'):
    await_netloc(host, port)
    connected = False
    arangodb_client = None
    while not connected:
        try:
            arangodb_client = ArangoClient(host=host)
        except:
            time.sleep(3)
        else:
            connected = True
    connected = False
    sys_db = arangodb_client.db('_system', username=username, password=password)
    while not connected:
        try:
            if sys_db.has_database(database):
                sys_db.delete_database(database)
        except:
            time.sleep(3)
        else:
            connected = True
    sys_db.create_database(database)
    topology_db = arangodb_client.db(database, username=username, password=password)
    topology = None
    if not topology_db.has_graph('Topology'):
        topology = topology_db.create_graph('Topology')
    else:
        topology = topology_db.graph('Topology')
    nodes = None
    if not topology.has_vertex_collection('Nodes'):
        nodes = topology.create_vertex_collection('Nodes')
    else:
        nodes = topology.vertex_collection('Nodes')
    #nodes.add_geo_index('coordinate')
    if not topology.has_edge_definition('Connections'):
        topology.create_edge_definition(
            edge_collection='Connections',
            from_vertex_collections=['Nodes'],
            to_vertex_collections=['Nodes']
        )
    return topology

def ensure_mqtt(host):
    mqtt_client = MQTTClient()
    mqtt_client.on_connect = mqtt_on_connect
    mqtt_client.message_callback_add('embrace/sensors', mqtt_on_message_sensor)
    mqtt_client.message_callback_add('embrace/topology', mqtt_on_message_topology)
    mqtt_client.connect(host, 1883, 60)
    return mqtt_client

def main(mqtt_host='mqtt_broker', influxdb_host='tsdb', arangodb_host='graphdb'):
    global influxdb_client
    global topology_graph
    global mqtt_client
    logging.info('Setting up InfluxDB...')
    influxdb_client = ensure_influxdb(influxdb_host, 8086)
    logging.info('Setting up ArangoDB...')
    topology_graph = ensure_arangodb(arangodb_host, 8529)
    logging.info('Setting up Mosquito/MQTT...')
    mqtt_client = ensure_mqtt(mqtt_host)
    mqtt_client.loop_forever()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    main()
