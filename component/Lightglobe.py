from component.Light import Light

class Lightglobe(Light):
    def __init__(self, name: str, price: float, colour: str, voltage: float, current: float) -> None:
        super().__init__(name, price, colour, voltage, current)
        return None
    
    def showDetails(self) -> str:
        return "LightGlobe -> " + super().showDetails()
    
    def duplicate(self) -> "Lightglobe":
        return Lightglobe(self.name, self.price, self.colour, self.voltage, self.current)
    pass
