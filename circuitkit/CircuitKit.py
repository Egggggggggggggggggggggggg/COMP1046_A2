# File: circuitkit/CircuitKit.py
# Author: Your Name
# ID: Your Student ID
# Email: your.email@learning.eynesbury.edu.au
# Description: CircuitKit class for grouping components into a kit (model only).
# This is my own work as defined by the Academic Integrity Policy

from typing import List, Tuple


class CircuitKit:
    '''
    Object model for a circuit kit.

    Attributes:
    name (str): Kit display name, e.g., "Light Circuit", "Sensor Circuit".
    price (float): Optional overall price (not stored in CSV; computed in UI when needed).
    items (List[Tuple[int, str]]): A list of (qty, component_row_without_stock_qty).
                                   component_row_without_stock_qty is like "Battery,AA,1.5,3.1".
    Your Name
    '''

    def __init__(self, name: str, price: float, items: List[Tuple[int, str]]) -> None:
        '''
        Initialize kit with name, optional price, and items.

        Parameters:
        name (str): Kit name.
        price (float): A computed value; not persisted to components.csv.
        items (List[Tuple[int,str]]): Each item is (qty, component_fragment_without_qty)
        Your Name
        '''
        self.name = name
        self.price = float(price) if price is not None else 0.0
        self.items: List[Tuple[int, str]] = []
        for q, frag in items:
            self.items.append((int(q), str(frag).strip()))

    # ---------------- Heading helpers for UI ----------------

    def heading_caps(self) -> str:
        '''
        Uppercase heading for list displays.
        Your Name
        '''
        return self.name.upper()

    def heading_pretty(self) -> str:
        '''
        Pretty heading for detail displays.
        Your Name
        '''
        return self.name

    # ---------------- CSV helpers (flat, no JSON) ----------------

    def items_as_flat_tokens(self) -> List[str]:
        '''
        Convert items to a flat list of tokens for CSV / transactions:
        [ item_qty, item_type, ...item_fields..., item_qty, item_type, ... ]
        Your Name
        '''
        out: List[str] = []
        for qty, frag in self.items:
            parts = [c.strip() for c in frag.split(",")]
            out.append(str(int(qty)))
            out.extend(parts)
        return out

    @staticmethod
    def from_components_csv_row(row: List[str]) -> Tuple[int, "CircuitKit"]:
        '''
        Parse one components.csv row (kit inventory row) into (qty, CircuitKit).

        Format:
          qty, kit_name, item_qty, item_type, ...fields..., item_qty, item_type, ...fields...
        Your Name
        '''
        if row is None or len(row) < 2:
            raise ValueError("Invalid components.csv row")

        try:
            qty = int(str(row[0]).strip())
        except Exception:
            qty = 0

        kit_name = row[1].strip()

        # item parsing requires knowing how many columns each type has
        arity = {
            "Wire": 3,
            "Battery": 4,
            "Solar Panel": 4,
            "Light Globe": 5,
            "LED Light": 5,
            "Switch": 4,
            "Sensor": 4,
            "Buzzer": 6,
        }

        items: List[Tuple[int, str]] = []
        i = 2
        while i < len(row):
            try:
                item_qty = int(str(row[i]).strip())
            except Exception:
                break
            i = i + 1
            if i >= len(row):
                break
            item_type = row[i].strip()
            i = i + 1
            ncols = arity.get(item_type, 0)
            if ncols <= 0 or i + ncols - 1 >= len(row):
                break
            fields = [item_type] + [c.strip() for c in row[i:i + ncols]]
            i = i + ncols
            frag = ",".join(fields)
            items.append((item_qty, frag))

        kit = CircuitKit(kit_name, 0.0, items)
        return qty, kit

    def to_components_csv_row(self, qty: int) -> List[str]:
        '''
        Build a components.csv row (kit inventory row) for this kit.
        Format:
          [qty, name, item_qty, item_type, ...fields..., item_qty, item_type, ...]
        Your Name
        '''
        row = [str(int(qty)), self.name]
        row.extend(self.items_as_flat_tokens())
        return row
