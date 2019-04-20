import uuid
import time
import random
import threading
import math
import logging


FIVE_MINUTES=60*5

class Node(threading.Thread):

    def __init__(self, node_id=None, latitude=0, longitude=0, min_data_interval=FIVE_MINUTES, time_scale=1, **thread_args):
        self.node_id = node_id or uuid.uuid1()
        self.latitude = latitude
        self.longitude = longitude
        self.time_scale = time_scale
        self.min_data_interval = min_data_interval
        self.interface = None
        self._stop_event = threading.Event()
        self.sensors = self.create_sensors()
        super().__init__(target=self.run, **thread_args)

    def create_sensors(self):
        return {
            'battery': 100,
            'temperature': random.randint(-50, 120),
            'air_quality': random.randint(1, 100)
        }

    def stop(self):
        logging.info('%s received stop signal.', self.node_id)
        self._stop_event.set()
    
    def stopped(self):
        self._stop_event.is_set()
    
    def await_stop(self, timeout):
        self._stop_event.wait(timeout)

    def run(self):
        while not self.stopped():
            self.await_irq(self.min_data_interval)

    def await_irq(self, timeout=0):
        if timeout == 0:
            timeout = self.min_data_interval
        random_irq_time = random.randint(1, int(self.min_data_interval * self.time_scale))
        self.await_stop(
            timeout if timeout < random_irq_time else random_irq_time
        )
        data = self.get_sensor_data()
        self.send_data(data)
    
    def get_instantaneous_sensor_data(self):
        self.sensors['battery'] -= 0.1
        self.sensors['temperature'] += random.random() * random.randrange(-1, 1)
        self.sensors['air_quality'] += random.random() * random.randrange(-1, 1)
        return self.sensors
    
    def get_fixed_sensor_data(self):
        return {
            'latitude': self.latitude,
            'longitude': self.longitude,
            'id': self.node_id
        }

    def get_sensor_data(self):
        return {**self.get_fixed_sensor_data(), **self.get_instantaneous_sensor_data()}

    def set_interface(self, interface):
        self.interface = interface

    def send_data(self, data):
        if not self.interface:
            logging.error('No interface to send data from!')
        else:
            self.interface.forward_data(data)
