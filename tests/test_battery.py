# Academic Integrity Statment
# Filename: test_battery.py
# Author: Botao Huang
# Student ID: 521560
# Email: 521560@learning.eynesbury.edu.au
# Date: 17 SEP 2025
# Description: Test code for Battery class
# This is my own work as defined by the Academic Integrity Policy


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
