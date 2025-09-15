from component.Component import Component

class Wire(Component):
<<<<<<< HEAD
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
=======
    def __init__(self, length: float, price: float) -> None:
        super().__init__("Wire", price)
        self.__length = length

    @property
    def length(self) -> float:
        return self.__length

    def duplicate(self) -> "Wire":
        return Wire(self.length, self.price)

    @classmethod
    def from_string(cls, data: str) -> "Wire":
        parts = data.split(",")
        return cls(float(parts[0]), float(parts[1]))

    def to_csv(self) -> str:
        return str(self.length) + "," + str(self.price)

    def to_string(self) -> str:
        return str(self.length) + "mm Wire $" + str(self.price)

    def is_equals(self, other: "Component") -> bool:
        return isinstance(other, Wire) and self.length == other.length
>>>>>>> 469e8e68d6b8f34a1a911cad2c9ccff187ffa0e2
