from typing import List, Iterable, Tuple
import csv
import os
from datetime import datetime
from component.factory import csv_to_component, component_to_csv_row
from component.Component import Component


class App:
    def __init__(self,
                 data_dir: str = "data",
                 circuitKit_csv: str = "circuitKit.csv",
                 components_csv: str = "components.csv",
                 transactions_csv: str = "transactions.csv") -> None:
        os.makedirs(data_dir or ".", exist_ok=True)

        self._circuitKit_path = os.path.join(data_dir, circuitKit_csv)
        self._components_path = os.path.join(data_dir, components_csv)
        self._transactions_path = os.path.join(data_dir, transactions_csv)


        self._circuitKit: List[List[str]] = []
        self._components: List[List[str]] = []
        self._transactions: List[List[str]] = []

        self.load()


    def list_circuitKit(self) -> List[List[str]]:
        return list(self._circuitKit)

    def list_components(self) -> List[List[str]]:
        return list(self._components)

    def list_transactions(self) -> List[List[str]]:
        return list(self._transactions)


    def add_circuitkit_row(self, row: Iterable[str]) -> None:
        self._circuitKit.append([str(x) for x in row])
        self.save()

    def add_component_row(self, row: Iterable[str]) -> None:
        self._components.append([str(x) for x in row])
        self.save()

    def add_transaction_row(self, row: Iterable[str]) -> None:
        self._transactions.append([str(x) for x in row])
        self.save()


    def _read_csv(self, path: str) -> List[List[str]]:
        rows: List[List[str]] = []
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8", newline="") as f:
                for fields in csv.reader(f):
                    if not fields:
                        continue
                    rows.append([field.strip() for field in fields])
        return rows

    def _write_csv(self, path: str, rows: Iterable[Iterable[str]]) -> None:
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "w", encoding="utf-8", newline="") as f:
            w = csv.writer(f)
            for r in rows:
                w.writerow(list(r))


    def load(self) -> None:
        self._circuitKit = self._read_csv(self._circuitKit_path)
        self._components = self._read_csv(self._components_path)
        self._transactions = self._read_csv(self._transactions_path)

    def save(self) -> None:
        self._write_csv(self._circuitKit_path, self._circuitKit)
        self._write_csv(self._components_path, self._components)
        self._write_csv(self._transactions_path, self._transactions)


    def list_circuitKit_objects(self) -> List[Tuple[int, Component]]:
        objs: List[Tuple[int, Component]] = []
        for row in self._circuitKit:
            if len(row) < 3:
                continue
            qty = int(row[0])
            kind = row[1]
            fields = row[2:]
            comp = csv_to_component(kind, fields)
            objs.append((qty, comp))
        return objs

    def add_circuitkit_object(self, qty: int, comp: Component) -> None:
        row = component_to_csv_row(qty, comp)
        self.add_circuitkit_row(row)

    def get_circuitkit_row(self, index: int) -> List[str]:
        return list(self._circuitKit[index])

    def set_circuitkit_qty(self, index: int, new_qty: int) -> None:
        if new_qty < 0:
            raise ValueError("Quantity cannot be negative")
        self._circuitKit[index][0] = str(int(new_qty))
        self.save()

    def change_circuitkit_qty(self, index: int, delta: int) -> int:
        cur = int(self._circuitKit[index][0])
        new_qty = cur + int(delta)
        if new_qty < 0:
            raise ValueError("Not enough stock to sell")
        self._circuitKit[index][0] = str(new_qty)
        self.save()
        return new_qty

    def add_component_transaction(self, kind: str, row: List[str], qty: int, when: str = None) -> None:
        ts = when or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        detail = [str(int(qty))] + row[1:]
        self.add_transaction_row([kind, ts] + detail)


if __name__ == "__main__":
    from menu import UI
    ui = UI(App())
    ui.home()
