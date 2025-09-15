from component.Component import Component

class Wire(Component):
    def __init__(self, length: float, price: float) -> None:
        super().__init__("Wire", price)
        self.__length = length

    @property
    def length(self) -> float:
        return self.__length

    def duplicate(self) -> "Wire":
        return Wire(self.length, self.price)

    @classmethod
    def from_string(cls, data: str) -> "Wire":
        parts = data.split(",")
        return cls(float(parts[0]), float(parts[1]))

    def to_csv(self) -> str:
        return str(self.length) + "," + str(self.price)

    def to_string(self) -> str:
        return str(self.length) + "mm Wire $" + str(self.price)

    def is_equals(self, other: "Component") -> bool:
        return isinstance(other, Wire) and self.length == other.length
