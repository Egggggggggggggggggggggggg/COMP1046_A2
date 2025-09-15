from component.Component import Component

class Battery(Component):
    def __init__(self, name: str, price: float, voltage: float) -> None:
        super().__init__(name, price)
        self.voltage = voltage

    def showDetails(self) -> str:
        return "Battery(" + self.name + ", $" + format(self.price, ".2f") + ", " + str(self.voltage) + "V)"

    def toCSV(self) -> str:
        return "Battery," + self.name + "," + format(self.price, ".2f") + "," + str(self.voltage)

    def fromString(self, s: str) -> "Battery":
        parts = s.strip().split(",")
        if len(parts) != 4 or parts[0] != "Battery":
            raise ValueError("Invalid Battery string: " + s)
        return Battery(parts[1], float(parts[2]), float(parts[3]))

    def duplicate(self) -> "Battery":
        return Battery(self.name, self.price, self.voltage)

    def isEqual(self, other: "Battery") -> bool:
        return isinstance(other, Battery) and \
               self.name == other.name and \
               self.price == other.price and \
               self.voltage == other.voltage
