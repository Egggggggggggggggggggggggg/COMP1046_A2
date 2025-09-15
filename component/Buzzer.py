from component.Component import Component

class Buzzer(Component):
    def __init__(self, voltage: float, current: float, frequency: float, sound_pressure: float, price: float) -> None:
        super().__init__("Buzzer", price)
        self.__voltage = voltage
        self.__current = current
        self.__frequency = frequency
        self.__sound_pressure = sound_pressure

    @property
    def voltage(self) -> float:
        return self.__voltage

    @property
    def current(self) -> float:
        return self.__current

    @property
    def frequency(self) -> float:
        return self.__frequency

    @property
    def sound_pressure(self) -> float:
        return self.__sound_pressure

    def calculate_wattage(self) -> float:
        return self.voltage * self.current

    def showDetails(self) -> str:
        return self.toString()

    def duplicate(self) -> "Buzzer":
        return Buzzer(self.voltage, self.current, self.frequency, self.sound_pressure, self.price)

    @classmethod
    def fromString(cls, data: str) -> "Buzzer":
        parts = data.split(",")
        return cls(float(parts[0]), float(parts[1]), float(parts[2]), float(parts[3]), float(parts[4]))

    def toCSV(self) -> str:
        return str(self.voltage) + "," + str(self.current) + "," + str(self.frequency) + "," + str(self.sound_pressure) + "," + str(self.price)

    def toString(self) -> str:
        return str(self.voltage) + "V " + str(self.current) + "mA " + str(self.frequency) + "Hz " + str(self.sound_pressure) + "dB Buzzer $" + str(self.price)

    def isEquals(self, other: "Component") -> bool:
        return isinstance(other, Buzzer) and self.voltage == other.voltage and self.current == other.current and self.frequency == other.frequency and self.sound_pressure == other.sound_pressure