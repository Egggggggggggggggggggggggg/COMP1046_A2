from Component import Component

class Light(Component):
    def __init__(self, name: str, price: float, colour: str = "", voltage: float = 0.0) -> None:
        super().__init__(name, price)
        self.colour = colour
        self.voltage = voltage

    def calculateWasted(self) -> float:
        return 0.0
