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

    def calculateWasted(self) -> float:
        return 0.0
