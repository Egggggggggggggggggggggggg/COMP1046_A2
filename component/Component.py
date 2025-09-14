class Component:
    def __init__(self, name: str, price: float) -> None:
        self.name = name
        self.price = price

    def showDetails(self) -> str:
        return f"{self.__class__.__name__}({self.name}, ${self.price:.2f})"

    def toCSV(self) -> str:
        return ""

    def fromString(self, s: str) -> "Component":
        return self

    def duplicate(self) -> "Component":
        return self

    def isEqual(self, other: "Component") -> bool:
        return isinstance(other, Component) and self.name == other.name
