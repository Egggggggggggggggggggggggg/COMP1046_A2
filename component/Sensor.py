from component.InputComponent import InputComponent
from component.Component import Component

class Sensor(InputComponent):
    def __init__(self, sensor_type: str, voltage: float, price: float) -> None:
        super().__init__("Sensor", voltage, price)
        self.__sensor_type = sensor_type

    @property
    def sensor_type(self) -> str:
        return self.__sensor_type

    def duplicate(self) -> "Sensor":
        return Sensor(self.sensor_type, self.voltage, self.price)

    @classmethod
    def from_string(cls, data: str) -> "Sensor":
        parts = data.split(",")
        return cls(parts[0], float(parts[1]), float(parts[2]))

    def to_csv(self) -> str:
        return self.sensor_type + "," + str(self.voltage) + "," + str(self.price)

    def to_string(self) -> str:
        return str(self.voltage) + "V " + self.sensor_type + " Sensor $" + str(self.price)

    def is_equals(self, other: "Component") -> bool:
        return isinstance(other, Sensor) and self.sensor_type == other.sensor_type and self.voltage == other.voltage