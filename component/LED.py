from component.Component import Component

class LED(Component):
    def __init__(self, colour: str, voltage: float, current: float, price: float) -> None:
        super().__init__("LED Light", price)
        self.__colour = colour
        self.__voltage = voltage
        self.__current = current

    @property
    def colour(self) -> str:
        return self.__colour

    @property
    def voltage(self) -> float:
        return self.__voltage

    @property
    def current(self) -> float:
        return self.__current

    def showDetails(self) -> str:
        return self.toString()

    def duplicate(self) -> "LED":
        return LED(self.colour, self.voltage, self.current, self.price)

    @classmethod
    def fromString(cls, data: str) -> "LED":
        parts = data.split(",")
        return cls(parts[0], float(parts[1]), float(parts[2]), float(parts[3]))

    def toCSV(self) -> str:
        return self.colour + "," + str(self.voltage) + "," + str(self.current) + "," + str(self.price)

    def toString(self) -> str:
        return str(self.voltage) + "V " + str(self.current) + "mA " + self.colour.capitalize() + " LED Light $" + str(self.price)

    def isEquals(self, other: "Component") -> bool:
        return (
            isinstance(other, LED)
            and self.colour == other.colour
            and self.voltage == other.voltage
            and self.current == other.current
        )