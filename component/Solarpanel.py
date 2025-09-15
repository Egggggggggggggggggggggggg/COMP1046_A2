from component.PowerSupply import PowerSupply
from component.Component import Component

class Solarpanel(PowerSupply):
    def __init__(self, voltage: float, current: float, price: float) -> None:
        super().__init__("Solar Panel", voltage, price)
        self.__current = current

    @property
    def current(self) -> float:
        return self.__current

    def duplicate(self) -> "Solarpanel":
        return Solarpanel(self.voltage, self.current, self.price)

    @classmethod
    def fromString(cls, data: str) -> "Solarpanel":
        parts = data.split(",")
        return cls(float(parts[0]), float(parts[1]), float(parts[2]))

    def toCSV(self) -> str:
        return str(self.voltage) + "," + str(self.current) + "," + str(self.price)

    def toString(self) -> str:
        return str(self.voltage) + "V " + str(self.current) + "mA Solar Panel $" + str(self.price)

    def isEquals(self, other: "Component") -> bool:
        return isinstance(other, Solarpanel) and self.voltage == other.voltage and self.current == other.current