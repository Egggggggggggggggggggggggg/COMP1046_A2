from typing import List
from component.Component import Component

class Circuit:
    def __init__(self, name: str, price: float = 0.0) -> None:
        self.name = name
        self.price = price
        self.components: List[Component] = []

    def addComponent(self, component: Component) -> None:
        self.components.append(component)

    def removeComponent(self, component: Component) -> None:
        if component in self.components:
            self.components.remove(component)

    def getComponentCount(self) -> int:
        return len(self.components)

    def isEqual(self, other: "Circuit") -> bool:
        return isinstance(other, Circuit) and self.name == other.name
