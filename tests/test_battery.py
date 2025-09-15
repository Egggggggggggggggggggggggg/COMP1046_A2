import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from component.Battery import Battery

b1 = Battery("AA", 1.50, 9.0)
print(b1.showDetails())
print(b1.toCSV())

csv_str = "Battery,AA,1.50,9.0"
b2 = b1.fromString(csv_str)
print(b2.showDetails())

print(b1.isEqual(b2))
b3 = b1.duplicate()
print(b3.showDetails())
