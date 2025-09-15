class Component:
    def __init__(self, name: str, price: float) -> None:
        self.name = name
        self.price = price

    def showDetails(self) -> str:
        cls = self.__class__.__name__
        price_str = "$" + format(self.price, ".2f")
        return "".join([cls, "(", self.name, ", ", price_str, ")"])

    def toCSV(self) -> str:
        return ",".join([self.__class__.__name__, self.name, format(self.price, ".2f")])

    def fromString(self, s: str) -> "Component":
        return self

    def duplicate(self) -> "Component":
        return (self.name, self.price)

    def isEqual(self, other: "Component") -> bool:
        return isinstance(other, Component) and self.name == other.name