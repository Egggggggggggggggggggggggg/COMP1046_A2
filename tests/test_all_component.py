import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from component.Component import Component
from component.Battery import Battery
from component.Wire import Wire
from component.Light import Light
from component.Sensor import Sensor
from component.Switch import Switch
from component.Solarpanel import Solarpanel
from component.Buzzer import Buzzer
from component.PowerSupply import PowerSupply


def test_battery():
    print("\n=== Battery ===")
    b1 = Battery("AA", 1.50, 9.0)
    print("Details:", b1.showDetails())
    print("CSV:", b1.toCSV())
    b2 = Battery.fromString("Battery,AA,1.50,9.00")
    print("FromString:", b2.showDetails())
    print("Duplicate Equal:", b1.isEqual(b1.duplicate()))


def test_wire():
    print("\n=== Wire ===")
    w1 = Wire("Copper", 0.5, 100, "red")
    print("Details:", w1.showDetails())
    print("CSV:", w1.toCSV())
    w2 = Wire.fromString("Wire,Copper,0.50,100.00,red")
    print("FromString:", w2.showDetails())
    print("Duplicate Equal:", w1.isEqual(w1.duplicate()))


def test_light():
    print("\n=== Light ===")
    l1 = Light("LED", 2.0, "blue", 3.3, 0.2)
    print("Details:", l1.showDetails())
    print("CSV:", l1.toCSV())
    l2 = l1.duplicate()
    print("Duplicate Equal:", l1.isEqual(l2))


def test_sensor():
    print("\n=== Sensor ===")
    s1 = Sensor("Temperature", 5.0, 3.5)
    print("Details:", s1.showDetails())
    print("CSV:", s1.toCSV())
    s2 = Sensor.fromString("Temperature,5.0,3.5")
    print("FromString:", s2.showDetails())
    print("Duplicate Equal:", s1.isEqual(s1.duplicate()))


def test_switch():
    print("\n=== Switch ===")
    sw1 = Switch("toggle", 220, 4.5)
    print("Details:", sw1.showDetails())
    print("CSV:", sw1.toCSV())
    sw2 = Switch.fromString("toggle,220,4.5")
    print("FromString:", sw2.showDetails())
    print("Duplicate Equal:", sw1.isEqual(sw1.duplicate()))


def test_solarpanel():
    print("\n=== Solarpanel ===")
    sp1 = Solarpanel(12.0, 200, 25.0)
    print("Details:", sp1.showDetails())
    print("CSV:", sp1.toCSV())
    sp2 = Solarpanel.fromString("12,200,25")
    print("FromString:", sp2.showDetails())
    print("Duplicate Equal:", sp1.isEqual(sp1.duplicate()))


def test_buzzer():
    print("\n=== Buzzer ===")
    bz1 = Buzzer(5.0, 0.1, 2000, 90, 4.0)
    print("Details:", bz1.showDetails())
    print("CSV:", bz1.toCSV())
    bz2 = Buzzer.fromString("5,0.1,2000,90,4")
    print("FromString:", bz2.showDetails())
    print("Duplicate Equal:", bz1.isEqual(bz1.duplicate()))


if __name__ == "__main__":
    test_battery()
    test_wire()
    test_light()
    test_sensor()
    test_switch()
    test_solarpanel()
    test_buzzer()
