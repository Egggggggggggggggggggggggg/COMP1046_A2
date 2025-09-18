# Academic Integrity Statment
# Filename: test_switch.py
# Author: Botao Huang
# Student ID: 521560
# Email: 521560@learning.eynesbury.edu.au
# Date: 17 SEP 2025
# Description: Test code for Switch class
# This is my own work as defined by the Academic Integrity Policy


import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from component.Switch import Switch

def test_switch():
    print("\n=== Switch ===")
    sw1 = Switch("toggle", 220, 4.5)
    print("Details:", sw1.showDetails())
    print("CSV:", sw1.toCSV())
    sw2 = Switch.fromString("toggle,220,4.5")
    print("FromString:", sw2.showDetails())
    print("Duplicate Equal:", sw1.isEqual(sw1.duplicate()))

if __name__ == "__main__":
    test_switch()
