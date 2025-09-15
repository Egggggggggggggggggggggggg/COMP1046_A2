# Academic Integrity Statment
# Filename: Wire.py
# Author: Botao Huang
# Student ID: 521560
# Email: 521560@learning.eynesbury.edu.au
# Date: 15 SEP 2025
# Description: Wire class
# This is my own work as defined by the Academic Integrity Policy

from component.Component import Component

class Wire(Component):
    def __init__(self, name: str, price: float, length: float, colour: str) -> None:
        super().__init__(name, price)
        self._length = float(length)
        self._colour = colour
        
    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        if not value:
            raise ValueError("Wire name cannot be empty")
        self._name = value

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float) -> None:
        if value < 0:
            raise ValueError("Wire price cannot be negative")
        self._price = float(value)

    @property
    def length(self) -> float:
        return self._length

    @length.setter
    def length(self, value: float) -> None:
        if value <= 0:
            raise ValueError("Wire length must be positive")
        self._length = float(value)

    @property
    def colour(self) -> str:
        return self._colour

    @colour.setter
    def colour(self, value: str) -> None:
        if not value:
            raise ValueError("Wire colour cannot be empty")
        self._colour = value

    def showDetails(self) -> str:
        base = super().showDetails()[:-1]
        return base + ", " + format(self.length, ".2f") + "cm, " + self.colour + ")"

    def toCSV(self) -> str:
        return ",".join([
            "Wire",
            self.name,
            format(self.price, ".2f"),
            format(self.length, ".2f"),
            self.colour
        ])

    @classmethod
    def fromString(cls, s: str) -> "Wire":
        parts = [p.strip() for p in s.split(",")]
        if len(parts) == 5 and parts[0] == "Wire":
            return cls(parts[1], float(parts[2]), float(parts[3]), parts[4])
        elif len(parts) == 4:
            return cls(parts[0], float(parts[1]), float(parts[2]), parts[3])
        else:
            raise ValueError("Invalid Wire string: " + s)

    def duplicate(self) -> "Wire":
        return Wire(self.name, self.price, self.length, self.colour)

    def isEqual(self, other: "Wire") -> bool:
        return isinstance(other, Wire) and \
               self.name == other.name and \
               self.price == other.price and \
               self.length == other.length and \
               self.colour == other.colour
