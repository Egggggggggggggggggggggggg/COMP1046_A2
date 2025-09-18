# File: PurchaseOrder.py
# Author: Unubileg
# ID: 523127
# Email: 523127@learning.eynesbury.edu.au
# Description: PurchaseOrder class 
# This is my own work as defined by the Academic Integrity Policy

from typing import Dict
from component.Component import Component

class PurchaseOrder:
    '''
    Represents a purchase order with supplier, brand, and items with quantities.
    Unubileg
    '''

    def __init__(self, supplierName: str, brandName: str):
        self.supplierName = supplierName
        self.brandName = brandName
        self.salesTotal: float = 0.0
        self.isPurchased: bool = False
        self._items: Dict[Component, int] = {}

    def addItem(self, item: Component, quantity: int):
        self._items[item] = self._items.get(item, 0) + quantity

    def removeItem(self, item: Component):
        if item in self._items:
            del self._items[item]

    def calculateSalesTotal(self) -> float:
        return sum(getattr(c, "price", 0.0) * q for c, q in self._items.items())

    def validateSingleBrand(self) -> bool:
        return True  # placeholder

    def completeOrder(self):
        self.isPurchased = True

    def cancelOrder(self):
        self.isPurchased = False

    def getSupplierName(self) -> str:
        return self.supplierName

    def setSupplierName(self, name: str):
        self.supplierName = name

    def __str__(self) -> str:
        header = f"Purchase Order → {self.supplierName} ({self.brandName})"
        item_lines = []
        for c, q in self._items.items():
            line = f"{c.name} x {q}: ${c.price * q:.2f}"
            item_lines.append(line)
        total = f"Total: ${self.calculateSalesTotal():.2f}"
        return "\n".join([header] + item_lines + [total])
