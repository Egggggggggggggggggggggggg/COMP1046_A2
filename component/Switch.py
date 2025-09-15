from component.Component import Component

class Switch(Component):
    def __init__(self, switch_type: str, voltage: float, price: float) -> None:
        super().__init__("Switch", price)
        self.__switch_type = switch_type
        self.__voltage = voltage

    @property
    def switch_type(self) -> str:
        return self.__switch_type

    @property
    def voltage(self) -> float:
        return self.__voltage

    def showDetails(self) -> str:
        return self.toString()

    def duplicate(self) -> "Switch":
        return Switch(self.switch_type, self.voltage, self.price)

    @classmethod
    def fromString(cls, data: str) -> "Switch":
        parts = data.split(",")
        return cls(parts[0], float(parts[1]), float(parts[2]))

    def toCSV(self) -> str:
        return self.switch_type + "," + str(self.voltage) + "," + str(self.price)

    def toString(self) -> str:
        return str(self.voltage) + "V " + self.switch_type.capitalize() + " Switch $" + str(self.price)

    def isEquals(self, other: "Component") -> bool:
        return isinstance(other, Switch) and self.switch_type == other.switch_type and self.voltage == other.voltage