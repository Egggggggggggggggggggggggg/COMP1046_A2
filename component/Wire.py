from component.Component import Component

class Wire(Component):
    def __init__(self, name: str, price: float, length: float, colour: str) -> None:
        super().__init__(name, price)
        self.length = float(length)
        self.colour = colour

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

    def fromString(self, s: str) -> "Wire":
        parts = [p.strip() for p in s.split(",")]
        if len(parts) == 5 and parts[0] == "Wire":
            self.name = parts[1]
            self.price = float(parts[2])
            self.length = float(parts[3])
            self.colour = parts[4]
        elif len(parts) == 4:
            self.name = parts[0]
            self.price = float(parts[1])
            self.length = float(parts[2])
            self.colour = parts[3]
        else:
            raise ValueError("Invalid Wire string: " + s)
        return self

    def duplicate(self) -> "Wire":
        return Wire(self.name, self.price, self.length, self.colour)

    def isEqual(self, other: "Wire") -> bool:
        return isinstance(other, Wire) and \
               self.name == other.name and \
               self.price == other.price and \
               self.length == other.length and \
               self.colour == other.colour
