# Academic Integrity Statment
# Filename: test_solarpanel.py
# Author: Botao Huang
# Student ID: 521560
# Email: 521560@learning.eynesbury.edu.au
# Date: 17 SEP 2025
# Description: Test code for Solarpanel class
# This is my own work as defined by the Academic Integrity Policy


import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from component.Solarpanel import Solarpanel

def test_solarpanel():
    print("\n=== Solarpanel ===")
    sp1 = Solarpanel(12.0, 200, 25.0)
    print("Details:", sp1.showDetails())
    print("CSV:", sp1.toCSV())
    sp2 = Solarpanel.fromString("12,200,25")
    print("FromString:", sp2.showDetails())
    print("Duplicate Equal:", sp1.isEqual(sp1.duplicate()))

if __name__ == "__main__":
    test_solarpanel()
