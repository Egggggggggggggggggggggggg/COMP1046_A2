from abc import ABC, abstractmethod

class Component(ABC):
    def __init__(self, name: str, price: float) -> None:
        self.name = name
        self.price = price

    @abstractmethod
    def showDetails(self) -> str:
        return ""

    def toCSV(self) -> str:
        return ""

    def toString(self) -> str:
        return self.__class__.__name__ + f"({self.name}, {self.price})"

    def fromString(self, s: str) -> "Component":
        return self

    def clone(self) -> "Component":
        return self

    def isEqual(self, other: "Component") -> bool:
        return isinstance(other, Component) and self.name == other.name

    def parseCSV(self, raw: str) -> "Component":
        return self
