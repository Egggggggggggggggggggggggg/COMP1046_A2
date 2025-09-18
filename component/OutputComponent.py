# File: OutputComponent.py
# Author: Unubileg
# ID: 523127
# Email: 523127@learning.eynesbury.edu.au
# Description: abstract OutputComponent class
# This is my own work as defined by the Academic Integrity Policy

from component.Component import Component
from abc import ABC

class OutputComponent(Component, ABC):
    '''
    Abstract base class for output components with a voltage attribute.
    Unubileg
    '''

    def __init__(self, name: str, voltage: float, price: float):
        super().__init__(name, price)
        self.__voltage = voltage

    @property
    def voltage(self) -> float:
        return self.__voltage
