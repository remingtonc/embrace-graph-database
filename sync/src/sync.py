#!/usr/bin/env python
import logging
from paho.mqtt.client import Client

client = None

def on_connect(client, userdata, flags, rc):
    logging.info('Connected with result code %d.', rc)
    client.subscribe('sensors')

def on_message(client, userdata, msg):
    logging.debug('%s %s', msg.topic, msg.payload)

def main():
    client = Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect('mqtt_broker', 1883, 60)
    client.loop_forever()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()
