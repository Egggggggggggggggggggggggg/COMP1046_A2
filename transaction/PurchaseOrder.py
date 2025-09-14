from typing import Dict
from component.Component import Component

class PurchaseOrder:
    def __init__(self, supplierName: str, brandName: str) -> None:
        self.supplierName = supplierName
        self.brandName = brandName
        self.salesTotal: float = 0.0
        self.isPurchased: bool = False
        self._items: Dict[Component, int] = {}  # {Component: quantity}

    def addItem(self, item: Component, quantity: int) -> None:
        self._items[item] = self._items.get(item, 0) + quantity

    def removeItem(self, item: Component) -> None:
        if item in self._items:
            del self._items[item]

    def calculateSalesTotal(self) -> float:
        return sum(getattr(c, "price", 0.0) * q for c, q in self._items.items())

    def validateSingleBrand(self) -> bool:
        return True

    def completeOrder(self) -> None:
        self.isPurchased = True

    def cancelOrder(self) -> None:
        self.isPurchased = False

    def getSupplierName(self) -> str:
        return self.supplierName

    def setSupplierName(self, name: str) -> None:
        self.supplierName = name

    def __str__(self) -> str:
        header = " ".join(["Purchase Order →", self.supplierName, "(" + self.brandName + ")"])
        item_lines = []
        for c, q in self._items.items():
            line = " ".join([
                c.name, "x", str(q) + ":", "$" + format(getattr(c, "price", 0.0) * q, ".2f")
            ])
            item_lines.append(line)
        total = " ".join(["Total:", "$" + format(self.calculateSalesTotal(), ".2f")])
        return "\n".join([header] + item_lines + [total])
