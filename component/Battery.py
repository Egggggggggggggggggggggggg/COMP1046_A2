from component.Component import Component

class Battery(Component):
    def __init__(self, name: str, price: float, voltage: float) -> None:
        super().__init__(name, price)
        self._voltage = float(voltage)

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        if not value:
            raise ValueError("Battery name cannot be empty")
        self._name = value

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float) -> None:
        if value < 0:
            raise ValueError("Battery price cannot be negative")
        self._price = float(value)

    @property
    def voltage(self) -> float:
        return self._voltage

    @voltage.setter
    def voltage(self, value: float) -> None:
        if value <= 0:
            raise ValueError("Battery voltage must be positive")
        self._voltage = float(value)

    def showDetails(self) -> str:
        return "Battery(" + self.name + ", $" + format(self.price, ".2f") + ", " + format(self.voltage, ".2f") + "V)"

    def toCSV(self) -> str:
        return "Battery," + self.name + "," + format(self.price, ".2f") + "," + format(self.voltage, ".2f")

    @classmethod
    def fromString(cls, s: str) -> "Battery":
        parts = s.strip().split(",")
        if len(parts) != 4 or parts[0] != "Battery":
            raise ValueError("Invalid Battery string: " + s)
        return cls(parts[1], float(parts[2]), float(parts[3]))

    def duplicate(self) -> "Battery":
        return Battery(self.name, self.price, self.voltage)

    def isEqual(self, other: "Battery") -> bool:
        return isinstance(other, Battery) and \
               self.name == other.name and \
               self.price == other.price and \
               self.voltage == other.voltage
