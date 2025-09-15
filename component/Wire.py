from component.Component import Component

class Wire(Component):
    def __init__(self, name: str, price: float, length: float = 0.0) -> None:
        super().__init__(name, price)
        self.length = length
