from component.Component import Component

class Wire(Component):
    def __init__(self, name: str, price: float, length: float) -> None:
        super().__init__(name, price)
        self.length = length

    def showDetails(self) -> str:
        return "Wire(" + self.name + ", $" + format(self.price, ".2f") + ", " + str(self.length) + "cm)"

    def toCSV(self) -> str:
        return "Wire," + self.name + "," + format(self.price, ".2f") + "," + str(self.length)

    def fromString(self, s: str) -> "Wire":
        parts = s.strip().split(",")
        if len(parts) != 4 or parts[0] != "Wire":
            raise ValueError("Invalid Wire string: " + s)
        return Wire(parts[1], float(parts[2]), float(parts[3]))

    def duplicate(self) -> "Wire":
        return Wire(self.name, self.price, self.length)

    def isEqual(self, other: "Wire") -> bool:
        return isinstance(other, Wire) and \
               self.name == other.name and \
               self.price == other.price and \
               self.length == other.length
