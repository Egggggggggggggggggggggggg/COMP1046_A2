from typing import List, Iterable
import csv
import os

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


if __name__ == "__main__":
    from menu import UI
    ui = UI(App())
    ui.home()
