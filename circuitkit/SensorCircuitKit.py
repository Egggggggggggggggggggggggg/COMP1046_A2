#Academic Integrity Statement
#Author: Pratik Sapkota
#Student ID: 522498
#Email: 522498@learning.eynesbury.edu.au
#Description: SensorCircuitKit class definition
#This is my own work as defined by the Academic Integrity Policy.

from circuitkit.CircuitKit import CircuitKit

class SensorCircuitKit(CircuitKit):
    def __init__(self, name="SensorCircuitKit"):
        super().__init__(name)

    def get_power_supply_type(self):
        return "Battery"  # placeholder

    def get_sensor_type(self):
        return "Generic"  # placeholder

    def get_light_info(self):
        return "No lights"  # placeholder

    def is_complete(self):
        return True  # placeholder