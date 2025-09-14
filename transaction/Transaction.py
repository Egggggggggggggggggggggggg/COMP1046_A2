from typing import List
from datetime import datetime
from component.Component import Component

class Transaction:
    def __init__(self, dateTime: "datetime" = None) -> None:
        self.items: List[Component] = []
        self.dateTime = dateTime or datetime.now()

    def addItem(self, component: Component) -> None:
        self.items.append(component)

    def removeItem(self, component: Component) -> None:
        if component in self.items:
            self.items.remove(component)

    def getTotalPrice(self) -> float:
        return sum(getattr(c, "price", 0.0) for c in self.items)

    def cancel(self) -> None:
        pass

    def confirm(self) -> None:
        pass

    def searchByDate(self, date: "datetime") -> list["Transaction"]:
        return []
