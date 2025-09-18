# Academic Integrity Statment
# Filename: test_wire.py
# Author: Botao Huang
# Student ID: 521560
# Email: 521560@learning.eynesbury.edu.au
# Date: 17 SEP 2025
# Description: Test code for Wire class
# This is my own work as defined by the Academic Integrity Policy


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
