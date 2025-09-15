from component.Light import Light

class Lightglobe(Light):
    def __init__(self, name: str, price: float, colour: str, voltage: float, current: float) -> None:
        super().__init__(name, price, colour, voltage, current)
        return None
    pass
