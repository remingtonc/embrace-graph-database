import uuid
import time
import random


class Node:

    def __init__(self, _id=None, data_interval=60*5):
        self._id = _id or uuid.uuid1()
        self.fixed_sensor_data = self.get_fixed_sensor_data()

    def run():
        while True:
            self.await_irq_or_timeout()

    def await_irq_or_timeout(self):
        random_irq_time = random.randint(1, 24*7*4)
        time.sleep(
            self.data_interval if self.data_interval < random_irq_time else random_irq_time
        )
    
    def get_instantaneous_sensor_data(self):
        return {
            'battery': 5.5,
            'temperature': 70,
            'air_quality': 80
        }
    
    def get_fixed_sensor_data(self):
        return {
            'latitude': 0,
            'longitude': 0,
            'id': self._id
        }
    
    def send_data(self):
        # mqtt publish
        pass
