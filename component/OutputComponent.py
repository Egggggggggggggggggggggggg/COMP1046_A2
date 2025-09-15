from component.Component import Component
from abc import ABC

class OutputComponent(Component, ABC):
    def __init__(self, name: str, voltage: float, price: float) -> None:
        super().__init__(name, price)
        self.__voltage = voltage

    @property
    def voltage(self) -> float:
        return self.__voltage