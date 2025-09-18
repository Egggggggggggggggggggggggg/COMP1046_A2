# File: Lightglobe.py
# Author: Unubileg
# ID: 523127
# Email: 523127@learning.eynesbury.edu.au
# Description: Lightglobe class
# This is my own work as defined by the Academic Integrity Policy

from component.Light import Light

class Lightglobe(Light):
    '''
    Represents a Lightglobe, extending the Light class.
    Unubileg
    '''

    def __init__(self, name: str, price: float, colour: str, voltage: float, current: float):
        super().__init__(name, price, colour, voltage, current)

    def showDetails(self) -> str:
        return "LightGlobe -> " + super().showDetails()

    def duplicate(self) -> "Lightglobe":
        return Lightglobe(self.name, self.price, self.colour, self.voltage, self.current)
