class Component:
    def __init__(self, name: str, price: float) -> None:
        self._name = None
        self._price = None
        self.name = name
        self.price = price

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        if not value:
            raise ValueError("Component name cannot be empty")
        self._name = value

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float) -> None:
        try:
            v = float(value)
        except Exception:
            raise ValueError("Component price must be a number")
        if v < 0:
            raise ValueError("Component price cannot be negative")
        self._price = v

    def showDetails(self) -> str:
        cls = self.__class__.__name__
        price_str = "$" + format(self.price, ".2f")
        return "".join([cls, "(", self.name, ", ", price_str, ")"])

    def toCSV(self) -> str:
        return ",".join([self.__class__.__name__, self.name, format(self.price, ".2f")])

    def fromString(self, s: str) -> "Component":
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
        return Component(self.name, self.price)

    def isEqual(self, other: "Component") -> bool:
        return isinstance(other, Component) and \
               (self.__class__ is other.__class__) and \
               (self.name == other.name) and \
               (self.price == other.price)


    def __str__(self) -> str:
        return self.showDetails()
