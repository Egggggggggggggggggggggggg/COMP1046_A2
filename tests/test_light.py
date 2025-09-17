import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from component.Light import Light

def test_light():
    print("\n=== Light ===")
    l1 = Light("LED", 2.0, "blue", 3.3, 0.2)
    print("Details:", l1.showDetails())
    print("CSV:", l1.toCSV())
    l2 = l1.duplicate()
    print("Duplicate Equal:", l1.isEqual(l2))

if __name__ == "__main__":
    test_light()
