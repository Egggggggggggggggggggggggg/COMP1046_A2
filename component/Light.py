from Component import Component

class Light(Component):
    def __init__(self, name: str, price: float, colour: str = "", voltage: float = 0.0, current: float = 0.0) -> None:
        super().__init__(name, price)
        self.colour = colour
        self.current = float(current)
        self.voltage = float(voltage)

    def showDetails(self):
        head = super().showDetails()[:-1]
        volt = format(self.voltage, ".2f") + "V"
        curr = format(self.current, ".2f") + "A"
        return ", ".join([head, self.colour, volt, curr]) + ")"
    
    def toCSV(self) -> str:
        return ",".join(["Light", self.name, format(self.price, ".2f"), self.colour, format(self.voltage, ".2f"), format(self.current, ".2f")])

    def fromString(self, s: str) -> "Light":
        parts = [p.strip() for p in s.split(",")]
        if len(parts) == 6:
            self.name = parts[1]
            self.price = float(parts[2])
            self.colour = parts[3]
            self.voltage = float(parts[4])
            self.current = float(parts[5])
        elif len(parts) == 5:
            self.name = parts[0]
            self.price = float(parts[1])
            self.colour = parts[2]
            self.voltage = float(parts[3])
            self.current = float(parts[4])
        return self

    def duplicate(self) -> "Light":
        return Light(self.name, self.price, self.colour, self.voltage, self.current)

    def calculateWasted(self) -> float:
        #
        return 0.0

    def isEqual(self, other:"Light") -> bool:
        return isinstance(other, Light) and \
        self.name == other.name and \
        self.price == other.price and \
        self.colour == other.colour and \
        self.voltage == other.voltage and \
        self.current == other.current
    
    