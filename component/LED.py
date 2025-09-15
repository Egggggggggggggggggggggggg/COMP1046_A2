from component.Light import Light
from component.Component import Component

class LED(Light):
    def __init__(self, colour: str, voltage: float, current: float, price: float) -> None:
        super().__init__("LED Light", colour, voltage, current, price)

    def duplicate(self) -> "LED":
        return LED(self.colour, self.voltage, self.current, self.price)

    @classmethod
    def from_string(cls, data: str) -> "LED":
        parts = data.split(",")
        return cls(parts[0], float(parts[1]), float(parts[2]), float(parts[3]))

    def to_csv(self) -> str:
        return self.colour + "," + str(self.voltage) + "," + str(self.current) + "," + str(self.price)

    def to_string(self) -> str:
        return str(self.voltage) + "V " + str(self.current) + "mA " + self.colour.capitalize() + " LED Light $" + str(self.price)

    def is_equals(self, other: "Component") -> bool:
        return isinstance(other, LED) and self.colour == other.colour and self.voltage == other.voltage and self.current == other.current