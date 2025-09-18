# File: Battery.py
# Author: Unubileg
# ID: 523127
# Email: 523127@learning.eynesbury.edu.au
# Description: Battery class
# This is my own work as defined by the Academic Integrity Policy

from component.Component import Component

class Battery(Component):
    '''
    Represents a battery component with name, price, and voltage.
    Inherits from Component.
    Unubileg
    '''

    def __init__(self, name: str, price: float, voltage: float):
        '''
        Initializes the Battery with name, price, and voltage.
        Unubileg
        '''
        super().__init__(name, price)
        self._voltage = float(voltage)

    @property
    def name(self) -> str:
        '''Returns the name of the battery. Unubileg'''
        return self._name

    @name.setter
    def name(self, value: str):
        if not value:
            raise ValueError("Battery name cannot be empty")
        self._name = value

    @property
    def price(self) -> float:
        '''Returns the price of the battery. Unubileg'''
        return self._price

    @price.setter
    def price(self, value: float):
        if value < 0:
            raise ValueError("Battery price cannot be negative")
        self._price = float(value)

    @property
    def voltage(self) -> float:
        '''Returns the voltage of the battery. Unubileg'''
        return self._voltage

    @voltage.setter
    def voltage(self, value: float):
        if value <= 0:
            raise ValueError("Battery voltage must be positive")
        self._voltage = float(value)

    def showDetails(self) -> str:
        return f"Battery({self.name}, ${self.price:.2f}, {self.voltage:.2f}V)"

    def toCSV(self) -> str:
        return f"Battery,{self.name},{self.price:.2f},{self.voltage:.2f}"

    @classmethod
    def fromString(cls, s: str) -> "Battery":
        parts = s.strip().split(",")
        if len(parts) != 4 or parts[0] != "Battery":
            raise ValueError("Invalid Battery string: " + s)
        return cls(parts[1], float(parts[2]), float(parts[3]))

    def duplicate(self) -> "Battery":
        return Battery(self.name, self.price, self.voltage)

    def isEqual(self, other: "Battery") -> bool:
        return isinstance(other, Battery) and \
               self.name == other.name and \
               self.price == other.price and \
               self.voltage == other.voltage
