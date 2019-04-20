#!/usr/bin/env python
import logging
import signal
from simulator import Simulator

def main():
    logging.basicConfig(level=logging.DEBUG)
    logging.warning('Beginning simulation.')
    simulator = Simulator('mqtt_broker', time_scale=0.03)
    signal.signal(signal.SIGINT, simulator.stop_nodes)
    signal.signal(signal.SIGTERM, simulator.stop_nodes)
    simulator.activate_nodes()
    simulator.await_nodes()
    logging.warning('Simulation has ended.')

if __name__ == '__main__':
    main()
