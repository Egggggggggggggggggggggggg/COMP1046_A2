import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from component.Battery import Battery

def test_battery():
    print("\n=== Battery ===")
    b1 = Battery("AA", 1.50, 9.0)
    print("Details:", b1.showDetails())
    print("CSV:", b1.toCSV())
    b2 = Battery.fromString("Battery,AA,1.50,9.00")
    print("FromString:", b2.showDetails())
    print("Duplicate Equal:", b1.isEqual(b1.duplicate()))

if __name__ == "__main__":
    test_battery()
