from Component import Component

class Solarpanel(Component):
    def __init__(self, name: str, price: float, voltage: float = 0.0, current: float = 0.0) -> None:
        super().__init__(name, price)
        self.voltage = voltage
        self.current = current
