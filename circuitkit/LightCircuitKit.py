from circuitkit.CircuitKit import CircuitKit

class LightCircuitKit(CircuitKit):
    def __init__(self, name="LightCircuitKit"):
        super().__init__(name)
        self.__battery_count = 0
        self.__light_count = 0
        self.__switch_count = 0

    def check_has_battery(self):
        return self.__battery_count > 0

    def check_has_light(self):
        return self.__light_count > 0

    def check_has_switch(self):
        return self.__switch_count > 0

    def get_unique_colour_count(self):
        return 0  # placeholder

    def is_complete(self):
        return self.check_has_battery() and self.check_has_light() and self.check_has_switch()