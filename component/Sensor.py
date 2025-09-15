from component.Component import Component

class Sensor(Component):
    def __init__(self, sensor_type: str, voltage: float, price: float) -> None:
        super().__init__("Sensor", price)
        self.__sensor_type = sensor_type
        self.__voltage = voltage

    @property
    def sensor_type(self) -> str:
        return self.__sensor_type

    @property
    def voltage(self) -> float:
        return self.__voltage

    def showDetails(self) -> str:
        return self.toString()

    def duplicate(self) -> "Sensor":
        return Sensor(self.sensor_type, self.voltage, self.price)

    @classmethod
    def fromString(cls, data: str) -> "Sensor":
        parts = data.split(",")
        return cls(parts[0], float(parts[1]), float(parts[2]))

    def toCSV(self) -> str:
        return self.sensor_type + "," + str(self.voltage) + "," + str(self.price)

    def toString(self) -> str:
        return str(self.voltage) + "V " + self.sensor_type.capitalize() + " Sensor $" + str(self.price)
