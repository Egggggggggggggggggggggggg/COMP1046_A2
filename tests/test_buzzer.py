import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from component.Buzzer import Buzzer

def test_buzzer():
    print("\n=== Buzzer ===")
    bz1 = Buzzer(5.0, 0.1, 2000, 90, 4.0)
    print("Details:", bz1.showDetails())
    print("CSV:", bz1.toCSV())
    bz2 = Buzzer.fromString("5,0.1,2000,90,4")
    print("FromString:", bz2.showDetails())
    print("Duplicate Equal:", bz1.isEqual(bz1.duplicate()))

if __name__ == "__main__":
    test_buzzer()
