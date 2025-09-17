import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from component.Sensor import Sensor

def test_sensor():
    print("\n=== Sensor ===")
    s1 = Sensor("Temperature", 5.0, 3.5)
    print("Details:", s1.showDetails())
    print("CSV:", s1.toCSV())
    s2 = Sensor.fromString("Temperature,5.0,3.5")
    print("FromString:", s2.showDetails())
    print("Duplicate Equal:", s1.isEqual(s1.duplicate()))

if __name__ == "__main__":
    test_sensor()
