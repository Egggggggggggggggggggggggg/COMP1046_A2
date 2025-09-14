from Component import Component

class Sensor(Component):
    def __init__(self, name: str, price: float, type: str = "") -> None:  # noqa: A003
        super().__init__(name, price)
        self.type = type
