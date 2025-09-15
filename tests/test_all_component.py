import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from component.Battery import Battery
from component.Wire import Wire


def test_battery():
    print("=== Test Battery ===")
    b1 = Battery("AA", 1.50, 9.0)
    print("Show:", b1.showDetails())
    print("CSV :", b1.toCSV())

    csv_str = "Battery,AA,1.50,9.00"
    b2 = Battery.fromString(csv_str)
    print("FromString:", b2.showDetails())

    b3 = b1.duplicate()
    print("Duplicate Equal:", b1.isEqual(b3))

    try:
        b1.price = -10
    except ValueError as e:
        print("Expected error:", e)


def test_wire():
    print("\n=== Test Wire ===")
    w1 = Wire("CopperWire", 0.50, 100.0, "red")
    print("Show:", w1.showDetails())
    print("CSV :", w1.toCSV())

    csv_str = "Wire,CopperWire,0.50,100.00,red"
    w2 = Wire.fromString(csv_str)
    print("FromString:", w2.showDetails())

    w3 = w1.duplicate()
    print("Duplicate Equal:", w1.isEqual(w3))

    try:
        w1.length = 0
    except ValueError as e:
        print("Expected error:", e)


if __name__ == "__main__":
    test_battery()
    test_wire()
