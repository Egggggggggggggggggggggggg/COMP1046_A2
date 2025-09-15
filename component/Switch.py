from component.InputComponent import InputComponent
from component.Component import Component

class Switch(InputComponent):
    def __init__(self, switch_type: str, voltage: float, price: float) -> None:
        super().__init__("Switch", voltage, price)
        self.__switch_type = switch_type

    @property
    def switch_type(self) -> str:
        return self.__switch_type

    def duplicate(self) -> "Switch":
        return Switch(self.switch_type, self.voltage, self.price)

    @classmethod
    def from_string(cls, data: str) -> "Switch":
        parts = data.split(",")
        return cls(parts[0], float(parts[1]), float(parts[2]))

    def to_csv(self) -> str:
        return self.switch_type + "," + str(self.voltage) + "," + str(self.price)

    def to_string(self) -> str:
        return str(self.voltage) + "V " + self.switch_type + " Switch $" + str(self.price)

    def is_equals(self, other: "Component") -> bool:
        return isinstance(other, Switch) and self.switch_type == other.switch_type and self.voltage == other.voltage