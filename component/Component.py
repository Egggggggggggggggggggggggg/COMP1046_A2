from component.Component import Component

class Battery(Component):
    def __init__(self, size: str, voltage: float, price: float) -> None:
        super().__init__("Battery", price)
        self.__size = size
        self.__voltage = voltage

    @property
    def size(self) -> str:
        return self.__size

    @property
    def voltage(self) -> float:
        return self.__voltage

    def showDetails(self) -> str:
        return self.toString()

    def duplicate(self) -> "Battery":
        return Battery(self.size, self.voltage, self.price)

    @classmethod
    def fromString(cls, data: str) -> "Battery":
        parts = data.split(",")
        return cls(parts[0], float(parts[1]), float(parts[2]))

    def toCSV(self) -> str:
        return self.size + "," + str(self.voltage) + "," + str(self.price)

    def toString(self) -> str:
        return str(self.voltage) + "V " + self.size + " Battery $" + str(self.price)

    def isEquals(self, other: "Component") -> bool:
        return isinstance(other, Battery) and self.size == other.size and self.voltage == other.voltage