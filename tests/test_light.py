# Academic Integrity Statment
# Filename: test_light.py
# Author: Botao Huang
# Student ID: 521560
# Email: 521560@learning.eynesbury.edu.au
# Date: 17 SEP 2025
# Description: Test code for Light class
# This is my own work as defined by the Academic Integrity Policy


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
