# File: Solarpanel.py
# Author: Unubileg
# ID: 523127
# Email: 523127@learning.eynesbury.edu.au
# Description: Solarpanel class
# This is my own work as defined by the Academic Integrity Policy

from component.Component import Component

class Solarpanel(Component):
    '''
    Represents a solar panel component with voltage, current, and price.
    Unubileg
    '''

    def __init__(self, voltage: float, current: float, price: float):
        super().__init__("Solar Panel", price)
        self.__voltage = voltage
        self.__current = current

    @property
    def voltage(self) -> float:
        return self.__voltage

    @property
    def current(self) -> float:
        return self.__current

    def showDetails(self) -> str:
        return self.toString()

    def duplicate(self) -> "Solarpanel":
        return Solarpanel(self.voltage, self.current, self.price)

    @classmethod
    def fromString(cls, data: str) -> "Solarpanel":
        parts = data.split(",")
        return cls(float(parts[0]), float(parts[1]), float(parts[2]))

    def toCSV(self) -> str:
        return f"{self.voltage},{self.current},{self.price}"

    def toString(self) -> str:
        return f"{self.voltage}V {self.current}mA Solar Panel ${self.price}"

    def isEquals(self, other: "Component") -> bool:
        return isinstance(other, Solarpanel) and self.voltage == other.voltage and self.current == other.current
