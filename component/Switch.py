from Component import Component

class Switch(Component):
    def __init__(self, name: str, price: float, type: str = "") -> None:  # noqa: A003
        super().__init__(name, price)
        self.type = type
