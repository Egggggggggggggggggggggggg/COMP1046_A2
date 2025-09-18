# Academic Integrity Statment
# Filename: test_buzzer.py
# Author: Botao Huang
# Student ID: 521560
# Email: 521560@learning.eynesbury.edu.au
# Date: 17 SEP 2025
# Description: Test code for Buzzer class
# This is my own work as defined by the Academic Integrity Policy


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
