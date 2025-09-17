import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from component.Wire import Wire

def test_wire():
    print("\n=== Wire ===")
    w1 = Wire("Copper", 0.5, 100, "red")
    print("Details:", w1.showDetails())
    print("CSV:", w1.toCSV())
    w2 = Wire.fromString("Wire,Copper,0.50,100.00,red")
    print("FromString:", w2.showDetails())
    print("Duplicate Equal:", w1.isEqual(w1.duplicate()))

if __name__ == "__main__":
    test_wire()
