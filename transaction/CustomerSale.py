from typing import Dict
from component.Component import Component

class CustomerSale:
    def __init__(self, customerName: str) -> None:
        self.customerName = customerName
        self.saleTotal: float = 0.0
        self.isComplete: bool = False
        self._items: Dict[Component, int] = {}  # {Component: quantity}

    def addItem(self, component: Component, quantity: int) -> None:
        self._items[component] = self._items.get(component, 0) + quantity

    def removeItem(self, component: Component) -> None:
        if component in self._items:
            del self._items[component]

    def calculateSalesTotal(self) -> float:
        return sum(getattr(c, "price", 0.0) * q for c, q in self._items.items())

    def completeOrder(self) -> None:
        self.isComplete = True

    def cancelOrder(self) -> None:
        self.isComplete = False

    def getCustomerName(self) -> str:
        return self.customerName

    def setCustomerName(self, name: str) -> None:
        self.customerName = name

    def __str__(self) -> str:
        header = " ".join(["Sale to:", self.customerName])
        lines = []
        for c, q in self._items.items():
            amount = getattr(c, "price", 0.0) * q
            line = " ".join([c.name, "x", str(q) + ":", "$" + format(amount, ".2f")])
            lines.append(line)
        total = " ".join(["Total:", "$" + format(self.calculateSalesTotal(), ".2f")])
        return "\n".join([header] + lines + [total])