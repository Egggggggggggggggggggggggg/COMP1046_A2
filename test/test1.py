import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from component.Light import Light

l = Light("LED1", 2.5, "red", 3.3, 0.2)

print(l.showDetails())

print(l.toCSV())

