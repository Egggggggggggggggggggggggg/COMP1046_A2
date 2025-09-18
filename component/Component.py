# File: Component.py
# Author: Unubileg
# ID: 523127
# Email: 523127@learning.eynesbury.edu.au
# Description: Component.py
# This is my own work as defined by the Academic Integrity Policy

class Component:
    '''
    Represents a generic component with a name and a price.
    Unubileg
    '''

    def __init__(self, name: str, price: float):
        '''
        Initializes the component with a name and price.

        Parameters:
        name (str): The name of the component.
        price (float): The price of the component.
        Unubileg
        '''
        self._name = None
        self._price = None
        self.name = name
        self.price = price

    @property
    def name(self) -> str:
        '''
        Returns the name of the component.
        Unubileg
        '''
        return self._name

    @name.setter
    def name(self, value: str):
        '''
        Sets the name of the component. Raises an error if empty.

        Parameters:
        value (str): The name to set.
        Unubileg
        '''
        if not value:
            raise ValueError("Component name cannot be empty")
        self._name = value

    @property
    def price(self) -> float:
        '''
        Returns the price of the component.
        Unubileg
        '''
        return self._price

    @price.setter
    def price(self, value: float):
        '''
        Sets the price of the component. Must be a non-negative number.

        Parameters:
        value (float): The price to set.
        Unubileg
        '''
        try:
            v = float(value)
        except Exception:
            raise ValueError("Component price must be a number")
        if v < 0:
            raise ValueError("Component price cannot be negative")
        self._price = v

    def showDetails(self) -> str:
        '''
        Returns a formatted string with the component's details.
        Unubileg
        '''
        cls = self.__class__.__name__
        price_str = "$" + format(self.price, ".2f")
        return "".join([cls, "(", self.name, ", ", price_str, ")"])

    def toCSV(self) -> str:
        '''
        Returns the component's data in CSV format.
        Unubileg
        '''
        return ",".join([self.__class__.__name__, self.name, format(self.price, ".2f")])

    def fromString(self, s: str) -> "Component":
        '''
        Parses a component from a string and updates the current object.

        Parameters:
        s (str): A string in the format "ClassName,Name,Price" or "Name,Price".
        Unubileg
        '''
        parts = [p.strip() for p in s.split(",")]
        if len(parts) == 3:
            self.name = parts[1]
            self.price = float(parts[2])
        elif len(parts) == 2:
            self.name = parts[0]
            self.price = float(parts[1])
        else:
            raise ValueError("Invalid Component string: " + s)
        return self

    def duplicate(self) -> "Component":
        '''
        Returns a new Component object with the same data.
        Unubileg
        '''
        return Component(self.name, self.price)

    def isEqual(self, other: "Component") -> bool:
        '''
        Checks if another component is equal to this one.

        Parameters:
        other (Component): The component to compare.
        Unubileg
        '''
        return isinstance(other, Component) and \
               (self.__class__ is other.__class__) and \
               (self.name == other.name) and \
               (self.price == other.price)

    def __str__(self) -> str:
        '''
        Returns the string representation of the component.
        Unubileg
        '''
        return self.showDetails()
