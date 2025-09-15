

from component.OutputComponent import OutputComponent
from component.Component import Component

class Buzzer(OutputComponent):
    def __init__(self, frequency: float, sound_pressure: float, voltage: float, current: float, price: float) -> None:
        super().__init__("Buzzer", voltage, price)
        self.__frequency = frequency
        self.__sound_pressure = sound_pressure
        self.__current = current

    @property
    def frequency(self) -> float:
        return self.__frequency

    @property
    def sound_pressure(self) -> float:
        return self.__sound_pressure

    @property
    def current(self) -> float:
        return self.__current

    def duplicate(self) -> "Buzzer":
        return Buzzer(self.frequency, self.sound_pressure, self.voltage, self.current, self.price)

    @classmethod
    def from_string(cls, data: str) -> "Buzzer":
        parts = data.split(",")
        return cls(float(parts[0]), float(parts[1]), float(parts[2]), float(parts[3]), float(parts[4]))

    def to_csv(self) -> str:
        return str(self.frequency) + "," + str(self.sound_pressure) + "," + str(self.voltage) + "," + str(self.current) + "," + str(self.price)

    def to_string(self) -> str:
        return str(self.voltage) + "V " + str(self.current) + "mA " + str(self.frequency) + "Hz " + str(self.sound_pressure) + "dB Buzzer $" + str(self.price)

    def is_equals(self, other: "Component") -> bool:
        return (
            isinstance(other, Buzzer)
            and self.frequency == other.frequency
            and self.voltage == other.voltage
            and self.current == other.current
        )
