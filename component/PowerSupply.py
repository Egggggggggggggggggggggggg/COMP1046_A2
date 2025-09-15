#Academic Integrity Statement
#Author: Pratik Sapkota
#Student ID: 522498
#Email: 522498@learning.eynesbury.edu.au
#Description: PowerSupply class definition
#This is my own work as defined by the Academic Integrity Policy.

from component.Component import Component
from abc import ABC

class PowerSupply(Component, ABC):
    def __init__(self, name: str, voltage: float, price: float) -> None:
        super().__init__(name, price)
        self.__voltage = voltage

    @property
    def voltage(self) -> float:
        return self.__voltage