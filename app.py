import os
import csv
from datetime import datetime
from typing import List, Tuple, Dict, Any
from circuitkit.CircuitKit import CircuitKit
from menu import Menu


class App:
    def __init__(self) -> None:
        self.__base_dir = os.path.dirname(os.path.abspath(__file__))
        self.__data_dir = os.path.join(self.__base_dir, "data")
        self.__components_path = os.path.join(self.__data_dir, "circuitKit.csv")
        self.__circuits_path = os.path.join(self.__data_dir, "circuits.csv")
        self.__transactions_path = os.path.join(self.__data_dir, "transactions.csv")
        self.__components: Dict[str, int] = {}
        self.__circuits: Dict[str, Dict[str, Any]] = {}
        self.__ensure_files()
        self.__load_components()
        self.__load_circuits()
        Menu(self).run()

    def __ensure_files(self) -> None:
        if not os.path.exists(self.__data_dir):
            os.makedirs(self.__data_dir, exist_ok=True)
        if not os.path.exists(self.__components_path):
            with open(self.__components_path, "w", newline="", encoding="utf-8"):
                pass
        if not os.path.exists(self.__circuits_path):
            with open(self.__circuits_path, "w", newline="", encoding="utf-8"):
                pass
        if not os.path.exists(self.__transactions_path):
            with open(self.__transactions_path, "w", newline="", encoding="utf-8"):
                pass

    def __load_components(self) -> None:
        self.__components.clear()
        with open(self.__components_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line == "":
                    continue
                first_comma = line.find(",")
                if first_comma == -1:
                    continue
                qty_s = line[:first_comma].strip()
                frag = line[first_comma + 1:].strip()
                try:
                    qty = int(qty_s)
                except Exception:
                    qty = 0
                self.__components[frag] = self.__components.get(frag, 0) + qty

    def save_components(self) -> None:
        with open(self.__components_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            for frag, qty in self.__components.items():
                writer.writerow([qty, frag])

    def list_component_rows(self) -> List[Tuple[int, str]]:
        items = []
        for frag, qty in self.__components.items():
            items.append((qty, frag))
        items.sort(key=lambda x: (x[1], x[0]))
        return items

    def change_component_qty(self, row_without_qty: str, delta: int) -> None:
        cur = self.__components.get(row_without_qty, 0)
        newv = cur + delta
        if newv > 0:
            self.__components[row_without_qty] = newv
        else:
            if row_without_qty in self.__components:
                del self.__components[row_without_qty]

    def __load_circuits(self) -> None:
        self.__circuits.clear()
        with open(self.__circuits_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                if row is None or len(row) == 0:
                    continue
                if len(row) < 4:
                    continue
                qty_s = row[0].strip()
                name = row[1].strip()
                price_s = row[2].strip()
                items_json = row[3].strip()
                try:
                    qty = int(qty_s)
                except Exception:
                    qty = 0
                try:
                    price = float(price_s)
                except Exception:
                    price = 0.0
                self.__circuits[name] = {"qty": qty, "price": price, "items_json": items_json}

    def save_circuits(self) -> None:
        with open(self.__circuits_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            for name, data in self.__circuits.items():
                writer.writerow([data["qty"], name, data["price"], data["items_json"]])

    def list_circuit_objects(self) -> List[Tuple[int, CircuitKit]]:
        out: List[Tuple[int, CircuitKit]] = []
        for name, data in self.__circuits.items():
            items = CircuitKit.items_from_json(data["items_json"])
            kit = CircuitKit(name, float(data["price"]), items)
            out.append((int(data["qty"]), kit))
        out.sort(key=lambda x: x[1].name)
        return out

    def add_circuit_object(self, kit: CircuitKit, qty: int) -> None:
        if kit.name in self.__circuits:
            self.__circuits[kit.name]["qty"] = self.__circuits[kit.name]["qty"] + qty
            self.__circuits[kit.name]["price"] = kit.price
            self.__circuits[kit.name]["items_json"] = kit.items_to_json()
        else:
            self.__circuits[kit.name] = {"qty": qty, "price": kit.price, "items_json": kit.items_to_json()}

    def change_circuit_qty(self, kit_name: str, delta: int) -> bool:
        if kit_name not in self.__circuits:
            return False
        cur = int(self.__circuits[kit_name]["qty"])
        newv = cur + delta
        if newv > 0:
            self.__circuits[kit_name]["qty"] = newv
        else:
            del self.__circuits[kit_name]
        return True

    def can_pack(self, kit: CircuitKit, count: int) -> bool:
        for (iqty, frag) in kit.items:
            needed = iqty * count
            avail = self.__components.get(frag, 0)
            if avail < needed:
                return False
        return True

    def perform_pack(self, kit: CircuitKit, count: int) -> None:
        for (iqty, frag) in kit.items:
            self.change_component_qty(frag, -iqty * count)
        self.add_circuit_object(kit, count)
        self.save_components()
        self.save_circuits()
        self.add_circuit_transaction("Pack", kit, count)

    def can_unpack(self, kit_name: str, count: int) -> bool:
        if kit_name not in self.__circuits:
            return False
        return int(self.__circuits[kit_name]["qty"]) >= count

    def perform_unpack(self, kit_name: str, count: int) -> None:
        if kit_name not in self.__circuits:
            return
        items = CircuitKit.items_from_json(self.__circuits[kit_name]["items_json"])
        price = float(self.__circuits[kit_name]["price"])
        kit = CircuitKit(kit_name, price, items)
        self.change_circuit_qty(kit_name, -count)
        for (iqty, frag) in items:
            self.change_component_qty(frag, iqty * count)
        self.save_components()
        self.save_circuits()
        self.add_circuit_transaction("Unpack", kit, count)

    def add_component_transaction(self, op_type: str, frag: str, qty: int) -> None:
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.__transactions_path, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            row = [op_type, " " + ts, qty]
            row.extend([c.strip() for c in frag.split(",")])
            writer.writerow(row)

    def add_circuit_transaction(self, op_type: str, kit: CircuitKit, qty: int) -> None:
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.__transactions_path, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            row = [op_type, " " + ts, qty, "KIT", kit.name, kit.items_to_json()]
            writer.writerow(row)

    def buy_component(self, frag: str, qty: int) -> None:
        self.change_component_qty(frag, qty)
        self.save_components()
        self.add_component_transaction("Purchase Order", frag, qty)

    def sell_component(self, frag: str, qty: int) -> bool:
        if self.__components.get(frag, 0) < qty:
            return False
        self.change_component_qty(frag, -qty)
        self.save_components()
        self.add_component_transaction("Customer Sale", frag, qty)
        return True

    def buy_circuit(self, kit_name: str, qty: int) -> bool:
        if kit_name not in self.__circuits:
            return False
        price = float(self.__circuits[kit_name]["price"])
        items = CircuitKit.items_from_json(self.__circuits[kit_name]["items_json"])
        kit = CircuitKit(kit_name, price, items)
        self.add_circuit_object(kit, qty)
        self.save_circuits()
        self.add_circuit_transaction("Purchase Order", kit, qty)
        return True

    def sell_circuit(self, kit_name: str, qty: int) -> bool:
        if kit_name not in self.__circuits:
            return False
        if int(self.__circuits[kit_name]["qty"]) < qty:
            return False
        price = float(self.__circuits[kit_name]["price"])
        items = CircuitKit.items_from_json(self.__circuits[kit_name]["items_json"])
        kit = CircuitKit(kit_name, price, items)
        self.change_circuit_qty(kit_name, -qty)
        self.save_circuits()
        self.add_circuit_transaction("Customer Sale", kit, qty)
        return True


if __name__ == "__main__":
    App()
