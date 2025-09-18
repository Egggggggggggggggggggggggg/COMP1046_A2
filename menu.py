import os
import csv
import json
import sys
from typing import Callable, Optional, List, Tuple
from circuitkit.CircuitKit import CircuitKit


class SelectorMenu:
    def __init__(self, title: str, options: List[Tuple[str, Optional[Callable[[], None]]]], prompt: str = "Please enter a number: ") -> None:
        self._title = title
        self._options = options
        self._prompt = prompt

    def _input_select(self) -> Optional[Callable[[], None]]:
        sel = input(self._prompt).strip()
        idx = int(sel) - 1
        if idx < 0 or idx >= len(self._options):
            raise ValueError("Wrong input, must be a number between 1 and " + str(len(self._options)))
        _, fn = self._options[idx]
        return fn

    def run(self) -> bool:
        print(self._title)
        for i, (name, _) in enumerate(self._options, 1):
            print(str(i) + ". " + name)
        try:
            fn = self._input_select()
            if fn is None:
                return False
            fn()
            return True
        except ValueError as e:
            print(str(e))
            return True
        except Exception as e:
            print("Error: " + str(e))
            return True


class UI:
    def __init__(self, app) -> None:
        self.app = app

    def _input_int(self, prompt: str, min_val: Optional[int] = None, max_val: Optional[int] = None) -> int:
        s = input(prompt).strip()
        v = int(s)
        if min_val is not None and v < min_val:
            raise ValueError("Value must be at least " + str(min_val))
        if max_val is not None and v > max_val:
            raise ValueError("Value must be at most " + str(max_val))
        return v

    def _input_float(self, prompt: str, min_val: Optional[float] = None, max_val: Optional[float] = None) -> float:
        s = input(prompt).strip()
        v = float(s)
        if min_val is not None and v < min_val:
            raise ValueError("Value must be at least " + str(min_val))
        if max_val is not None and v > max_val:
            raise ValueError("Value must be at most " + str(max_val))
        return v

    def _to_float(self, s: str) -> float:
        try:
            return float(s)
        except Exception:
            return 0.0

    def _now_string(self) -> str:
        import datetime
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _extract_price_string(self, frag: str) -> str:
        parts = [c.strip() for c in frag.split(",")]
        if len(parts) == 0:
            return "0.00"
        return parts[-1]

    def _fmt(self, s: str) -> str:
        try:
            v = float(s)
            return str(round(v, 1))
        except Exception:
            return s

    def _to_title(self, s: str) -> str:
        if s is None or s == "":
            return ""
        lowers = set(["with", "and", "or", "of", "the", "a", "an", "x"])
        t = s.strip()
        if t.lower() in lowers:
            return t.lower()
        return t[0:1].upper() + t[1:].lower()

    def _component_row_to_pretty_title(self, frag: str) -> str:
        try:
            cols = [c.strip() for c in frag.split(",")]
            ctype = cols[0]
            if ctype == "Wire" and len(cols) >= 3:
                return cols[1] + "mm Wire"
            if ctype == "Battery" and len(cols) >= 4:
                return cols[2] + "V " + cols[1] + " Battery"
            if ctype == "Solar Panel" and len(cols) >= 4:
                return cols[1] + "V " + cols[2] + "mA Solar Panel"
            if ctype == "Light Globe" and len(cols) >= 5:
                colour = cols[1]
                volt = cols[2]
                curr = cols[3]
                return volt + "V " + self._fmt(curr) + "mA " + self._to_title(colour) + " Light Globe"
            if ctype == "LED Light" and len(cols) >= 5:
                colour = cols[1]
                volt = cols[2]
                curr = cols[3]
                return volt + "V " + self._fmt(curr) + "mA " + self._to_title(colour) + " LED Light"
            if ctype == "Switch" and len(cols) >= 3:
                return cols[2] + "V " + self._to_title(cols[1]) + " Switch"
            if ctype == "Sensor" and len(cols) >= 3:
                return cols[2] + "V " + self._to_title(cols[1]) + " Sensor"
            if ctype == "Buzzer" and len(cols) >= 6:
                freq = cols[1]
                spl = cols[2]
                volt = cols[3]
                curr = cols[4]
                return volt + "V " + self._fmt(curr) + "mA " + self._fmt(freq) + "Hz " + spl + "dB Buzzer"
            return ctype
        except Exception:
            return frag

    def _price_from_frag(self, frag: str) -> float:
        parts = [c.strip() for c in frag.split(",")]
        if len(parts) == 0:
            return 0.0
        try:
            return float(parts[-1])
        except Exception:
            return 0.0

    def _summarize_transactions(self) -> List[Tuple[str, str, float]]:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(base_dir, "data", "transactions.csv")
        summaries: List[Tuple[str, str, float]] = []
        totals_map = {}
        order_keys: List[Tuple[str, str]] = []

        try:
            with open(path, "r", encoding="utf-8", newline="") as f:
                reader = csv.reader(f)
                for row in reader:
                    if row is None or len(row) == 0:
                        continue
                    try:
                        op_type = row[0].strip()
                        ts = row[1].strip()
                        qty = int(str(row[2]).strip())
                    except Exception:
                        continue

                    amount = 0.0
                    if len(row) >= 4 and row[3].strip() == "KIT":
                        try:
                            items_json = row[5]
                            items = json.loads(items_json)
                            unit_sum = 0.0
                            for it in items:
                                iq = int(it.get("qty", 0))
                                frag = str(it.get("row", ""))
                                unit_sum = unit_sum + (iq * self._price_from_frag(frag))
                            amount = unit_sum * qty
                        except Exception:
                            amount = 0.0
                    else:
                        try:
                            unit_price = float(row[-1])
                            amount = qty * unit_price
                        except Exception:
                            amount = 0.0

                    key = (op_type, ts)
                    if key not in totals_map:
                        totals_map[key] = 0.0
                        order_keys.append(key)
                    totals_map[key] = totals_map[key] + amount
        except FileNotFoundError:
            return []

        for key in order_keys:
            op_type, ts = key
            total = totals_map.get(key, 0.0)
            summaries.append((op_type, ts, total))
        return summaries


    def _component_row_to_caps_title(self, frag: str) -> str:
        return self._component_row_to_pretty_title(frag).upper()

    def _infer_circuit_base_name(self, items: List[Tuple[int, str]]) -> str:
        has_light_globe = False
        has_led_light = False
        has_sensor = False
        for q, frag in items:
            head = frag.split(",")[0].strip()
            if head == "Light Globe":
                has_light_globe = True
            elif head == "LED Light":
                has_led_light = True
            elif head == "Sensor":
                has_sensor = True
        if has_sensor and (has_light_globe or has_led_light):
            return "Sensor Circuit"
        if has_sensor:
            return "Sensor Circuit"
        if has_light_globe:
            return "Light Circuit"
        if has_led_light:
            return "Light Circuit"
        return "Circuit"

    def home(self) -> None:
        SelectorMenu("HOME MENU", [
            ("COMPONENTS", self.components_menu),
            ("CIRCUIT KITS", self.circuits_menu),
            ("PURCHASE ORDERS", self.purchase_orders_menu),
            ("CUSTOMER SALES", self.customer_sales_menu),
            ("TRANSACTION HISTORY", self.transactions_menu),
            ("CLOSE", self.close_app),
        ]).run()
        self.home()

    def components_menu(self) -> None:
        again = SelectorMenu("COMPONENT MENU", [
            ("NEW COMPONENT", self.new_component_menu),
            ("VIEW COMPONENTS", self.view_components),
            ("BACK", None),
        ]).run()
        if again:
            self.components_menu()

    def new_component_menu(self) -> None:
        again = SelectorMenu("NEW COMPONENT MENU", [
            ("WIRE", self.create_wire),
            ("BATTERY", self.create_battery),
            ("SOLAR PANEL", self.create_solar_panel),
            ("LIGHT GLOBE", self.create_light_globe),
            ("LED LIGHT", self.create_led_light),
            ("SWITCH", self.create_switch),
            ("SENSOR", self.create_sensor),
            ("BUZZER", self.create_buzzer),
            ("BACK", None),
        ]).run()
        if again:
            self.new_component_menu()

    def view_components(self) -> None:
        comp_list = self.app.list_component_rows()
        options: List[Tuple[str, Optional[Callable[[], None]]]] = []
        for qty, frag in comp_list:
            title = self._component_row_to_caps_title(frag)
            price = self._extract_price_string(frag)
            label = title + " $" + price + " X " + str(qty)
            options.append((label, (lambda f=frag: self._component_actions(f))))
        options.append(("BACK", None))
        again = SelectorMenu("ALL COMPONENTS", options).run()
        if again:
            self.view_components()

    def _component_actions(self, frag: str) -> None:
        title = self._component_row_to_pretty_title(frag)
        price = self._extract_price_string(frag)
        def buy() -> None:
            print("Buying " + title + " $" + price)
            n = self._input_int("Please enter number of " + title + " $" + price + ": ", 1, None)
            self.app.buy_component(frag, n)
            print("Bought " + self._component_row_to_caps_title(frag) + " $" + price + " X " + str(n))
            print("Completing Purchase Order " + self._now_string())
        def sell() -> None:
            print("Selling " + title + " $" + price)
            n = self._input_int("Please enter number of " + title + " $" + price + ": ", 1, None)
            ok = self.app.sell_component(frag, n)
            if ok:
                print("Sold " + title + " $" + price + " X " + str(n))
                print("Completing Customer Sale " + self._now_string())
            else:
                print("Not enough stock to sell.")
        SelectorMenu(title + " $" + price, [
            ("BUY", buy),
            ("SELL", sell),
            ("BACK", None),
        ]).run()

    def circuits_menu(self) -> None:
        again = SelectorMenu("CIRCUIT KIT MENU", [
            ("NEW CIRCUIT KIT", self.new_circuit_menu),
            ("VIEW CIRCUIT KITS", self.view_circuit_kits),
            ("BACK", None),
        ]).run()
        if again:
            self.circuits_menu()

    def new_circuit_menu(self) -> None:
        again = SelectorMenu("NEW CIRCUIT KIT MENU", [
            ("PACK FROM COMPONENTS", self._pack_from_components),
            ("BACK", None),
        ]).run()
        if again:
            self.new_circuit_menu()

    def _pack_from_components(self) -> None:
        comp_list = self.app.list_component_rows()
        if len(comp_list) == 0:
            print("No components available.")
            return
        chosen: List[Tuple[int, str]] = []
        done = {"v": False}
        while not done["v"]:
            options: List[Tuple[str, Optional[Callable[[], None]]]] = []
            for stock_qty, frag in comp_list:
                title = self._component_row_to_pretty_title(frag)
                price = self._extract_price_string(frag)
                label = title + " $" + price + " x " + str(stock_qty)
                def make_add(stock_qty_i: int, f: str, t: str, p: str) -> Callable[[], None]:
                    def _inner() -> None:
                        already = 0
                        for qx, fx in chosen:
                            if fx == f:
                                already = already + qx
                        remain = stock_qty_i - already
                        print("Selecting " + t + " $" + p)
                        want = self._input_int("Please enter number of " + t + "s: ", 1, None)
                        if want > remain:
                            print("Not enough in stock.")
                            return
                        chosen.append((want, f))
                        print("Added " + str(want) + " x " + t)
                    return _inner
                options.append((label, make_add(stock_qty, frag, title, price)))
            def set_done() -> None:
                done["v"] = True
            options.append(("DONE", set_done))
            SelectorMenu("PACK FROM COMPONENTS", options).run()
        if len(chosen) == 0:
            print("No items selected.")
            return
        piece_count = 0
        total_price = 0.0
        items_for_model: List[Tuple[int, str]] = []
        for q, frag in chosen:
            piece_count = piece_count + q
            unit_price = self._to_float(self._extract_price_string(frag))
            total_price = total_price + (unit_price * q)
            items_for_model.append((q, frag))
        base_name = self._infer_circuit_base_name(items_for_model)
        display_name = str(piece_count) + " Piece " + base_name
        kit = CircuitKit(display_name, total_price, items_for_model)
        if not self.app.can_pack(kit, 1):
            print("Not enough components to pack.")
            return
        print("Adding " + kit.heading_pretty())
        self.app.perform_pack(kit, 1)

    def view_circuit_kits(self) -> None:
        kits = self.app.list_circuit_objects()
        options: List[Tuple[str, Optional[Callable[[], None]]]] = []
        for qty, kit in kits:
            label = kit.heading_caps() + " X " + str(qty)
            options.append((label, (lambda k=kit: self._circuit_actions(k))))
        options.append(("BACK", None))
        again = SelectorMenu("ALL CIRCUIT KITS", options).run()
        if again:
            self.view_circuit_kits()

    def _circuit_actions(self, kit: CircuitKit) -> None:
        title = kit.heading_pretty()
        def sell() -> None:
            print("Selling " + title)
            n = self._input_int("Please enter number of " + title + ": ", 1, None)
            ok = self.app.sell_circuit(kit.name, n)
            if ok:
                print("Sold " + title + " X " + str(n))
                print("Completing Customer Sale " + self._now_string())
            else:
                print("Not enough stock to sell.")
        def pack_more() -> None:
            print("Packing " + title)
            n = self._input_int("Please enter number of " + title + ": ", 1, None)
            if not self.app.can_pack(kit, n):
                print("Not enough components to pack the requested number.")
                return
            self.app.perform_pack(kit, n)
            print("Packed " + title + " X " + str(n))
        def unpack() -> None:
            print("Unpacking " + title)
            n = self._input_int("Please enter number of " + title + ": ", 1, None)
            if not self.app.can_unpack(kit.name, n):
                print("Not enough kits to unpack.")
                return
            self.app.perform_unpack(kit.name, n)
            print("Unpacked " + title + " X " + str(n))
        def buy() -> None:
            print("Buying " + title)
            n = self._input_int("Please enter number of " + title + ": ", 1, None)
            ok = self.app.buy_circuit(kit.name, n)
            if ok:
                print("Bought " + title + " X " + str(n))
                print("Completing Purchase Order " + self._now_string())
            else:
                print("Kit not found.")
        SelectorMenu(title, [
            ("SELL", sell),
            ("PACK", pack_more),
            ("UNPACK", unpack),
            ("BUY", buy),
            ("BACK", None),
        ]).run()

    def purchase_orders_menu(self) -> None:
        def add_item() -> None:
            comp = self.app.list_component_rows()
            kits = self.app.list_circuit_objects()
            options: List[Tuple[str, Optional[Callable[[], None]]]] = []
            for qty, frag in comp:
                title = self._component_row_to_caps_title(frag)
                price = self._extract_price_string(frag)
                label = title + " $" + price
                def make_buy(f: str, p: str, t: str) -> Callable[[], None]:
                    def _inner() -> None:
                        q = self._input_int("Quantity: ", 1, None)
                        self.app.buy_component(f, q)
                        print("Adding " + str(q) + " x " + t + " $" + p)
                    return _inner
                options.append((label, make_buy(frag, price, title)))
            for qty, kit in kits:
                label = kit.heading_caps()
                def make_buy_kit(k: CircuitKit) -> Callable[[], None]:
                    def _inner() -> None:
                        q = self._input_int("Quantity: ", 1, None)
                        ok = self.app.buy_circuit(k.name, q)
                        if ok:
                            print("Adding " + str(q) + " x " + k.heading_caps())
                        else:
                            print("Kit not found.")
                    return _inner
                options.append((label, make_buy_kit(kit)))
            options.append(("BACK", None))
            SelectorMenu("PURCHASE ORDER", options).run()
        again = SelectorMenu("PURCHASE ORDER", [
            ("Add Item from Catalogue to Order", add_item),
            ("BACK (CANCEL ORDER)", None),
        ]).run()
        if again:
            self.purchase_orders_menu()

    def customer_sales_menu(self) -> None:
        def add_item() -> None:
            comp = self.app.list_component_rows()
            kits = self.app.list_circuit_objects()
            options: List[Tuple[str, Optional[Callable[[], None]]]] = []
            for qty, frag in comp:
                title = self._component_row_to_caps_title(frag)
                price = self._extract_price_string(frag)
                label = title + " $" + price + " X " + str(qty)
                def make_sell(f: str, have: int, pretty: str) -> Callable[[], None]:
                    def _inner() -> None:
                        q = self._input_int("Quantity: ", 1, None)
                        if q > have:
                            print("Not enough stock.")
                            return
                        ok = self.app.sell_component(f, q)
                        if ok:
                            print("Adding " + str(q) + " x " + pretty)
                        else:
                            print("Not enough stock.")
                    return _inner
                options.append((label, make_sell(frag, qty, title)))
            for qty, kit in kits:
                label = kit.heading_caps() + " X " + str(qty)
                def make_sell_kit(k: CircuitKit, have: int) -> Callable[[], None]:
                    def _inner() -> None:
                        q = self._input_int("Quantity: ", 1, None)
                        if q > have:
                            print("Not enough stock.")
                            return
                        ok = self.app.sell_circuit(k.name, q)
                        if ok:
                            print("Adding " + str(q) + " x " + k.heading_caps())
                        else:
                            print("Not enough stock.")
                    return _inner
                options.append((label, make_sell_kit(kit, qty)))
            options.append(("BACK", None))
            SelectorMenu("CUSTOMER SALE INVENTORY", options).run()
        again = SelectorMenu("CUSTOMER SALE", [
            ("Add Item from Inventory to Sale", add_item),
            ("BACK (CANCEL ORDER)", None),
        ]).run()
        if again:
            self.customer_sales_menu()

    def transactions_menu(self) -> None:
        lines = self._summarize_transactions()
        print("TRANSACTION HISTORY")
        if len(lines) == 0:
            print("No transactions yet.")
        else:
            i = 1
            for op_type, ts, total in lines:
                print(str(i) + ". " + op_type + " " + ts + ", total $" + format(total, ".2f"))
                i = i + 1

        again = SelectorMenu(
            "TRANSACTION HISTORY",
            [
                ("SORT", self.sort_transactions_menu),
                ("BACK", None),
            ],
            prompt="Select Option Number: "
        ).run()
        if again:
            self.transactions_menu()

    def sort_transactions_menu(self) -> None:
        again = SelectorMenu(
            "SORT OPTIONS",
            [
                ("Sort by date (ascending)", lambda: None),
                ("Sort by date (descending)", lambda: None),
                ("Sort by wholesale price (ascending)", lambda: None),
                ("Sort by wholesale price (descending)", lambda: None),
                ("Sort by retail price (ascending)", lambda: None),
                ("Sort by retail price (descending)", lambda: None),
                ("BACK (CANCEL SORTING)", None),
            ],
            prompt="Select option number: "
        ).run()
        if again:
            self.sort_transactions_menu()

    def close_app(self) -> None:
        print("Saving and Closing")
        self.app.save_components()
        self.app.save_circuits()
        sys.exit(0)

    def create_wire(self) -> None:
        print("NEW WIRE")
        length_mm = self._input_float("Please enter length (mm): ", 0.001, None)
        price = self._input_float("Please enter price: ", 0.0, None)
        qty = self._input_int("Please enter number of Wires: ", 1, None)
        frag = "Wire," + str(int(round(length_mm))) + "," + format(price, ".2f")
        self.app.buy_component(frag, qty)
        print("Added " + str(int(round(length_mm))) + "mm Wire $" + format(price, ".2f") + " X " + str(qty))

    def create_battery(self) -> None:
        print("NEW BATTERY")
        print("Battery sizes are AA or AAA or C or D or E")
        size = input("Please enter battery size: ").strip().upper()
        valid = {"AA": [1.2, 1.5], "AAA": [1.2, 1.5], "C": [1.2, 1.5], "D": [1.5], "E": [9.0]}
        while size not in valid:
            print("Invalid size. Valid: AA, AAA, C, D, E")
            size = input("Please enter battery size: ").strip().upper()
        print("AA, AAA and C batteries are either 1.2 Volts or 1.5 Volts")
        print("D batteries are 1.5 Volts")
        print("E batteries are 9.0 Volts")
        voltage = self._input_float("Please enter a voltage that matches the battery size: ", 0.0, None)
        allowed = [round(v, 2) for v in valid[size]]
        while round(voltage, 2) not in allowed:
            print("Voltage does not match the selected size. Allowed: " + ", ".join([str(v) for v in valid[size]]))
            voltage = self._input_float("Please enter a voltage that matches the battery size: ", 0.0, None)
        price = self._input_float("Please enter price: ", 0.0, None)
        qty = self._input_int("Please enter number of Batteries: ", 1, None)
        frag = "Battery," + size + "," + format(voltage, ".1f") + "," + format(price, ".2f")
        self.app.buy_component(frag, qty)
        print("Added " + format(voltage, ".1f") + "V " + size + " Battery $" + format(price, ".2f") + " X " + str(qty))

    def create_solar_panel(self) -> None:
        print("NEW SOLAR PANEL")
        print("Voltage is usually between 1 and 12")
        voltage = self._input_float("Please enter voltage (V): ", 0.0001, None)
        print("Current is usually between 100 and 1000 milliAmps")
        current_mA = self._input_float("Please enter current (mA): ", 0.0001, None)
        price = self._input_float("Please enter price: ", 0.0, None)
        qty = self._input_int("Please enter number of Solar Panels: ", 1, None)
        frag = "Solar Panel," + format(voltage, ".1f") + "," + format(current_mA, ".1f") + "," + format(price, ".2f")
        self.app.buy_component(frag, qty)
        print("Added " + format(voltage, ".1f") + "V " + format(current_mA, ".1f") + "mA Solar Panel $" + format(price, ".2f") + " X " + str(qty))

    def create_light_globe(self) -> None:
        print("NEW LIGHT GLOBE")
        print("Light Globe Colours:")
        print("warm, neutral, cool")
        allowed = {"warm", "neutral", "cool"}
        colour = input("Please enter light globe colour: ").strip().lower()
        while colour not in allowed:
            print("Invalid colour. Valid: warm, neutral, cool")
            colour = input("Please enter light globe colour: ").strip().lower()
        print("Voltage is usually between 1 and 12")
        voltage = self._input_float("Please enter voltage (V): ", 0.0001, None)
        print("Current is usually between 100 and 1000 milliAmps")
        current_mA = self._input_float("Please enter current (mA): ", 0.0001, None)
        price = self._input_float("Please enter price: ", 0.0, None)
        qty = self._input_int("Please enter number of Light Globes: ", 1, None)
        frag = "Light Globe," + colour + "," + format(voltage, ".1f") + "," + format(current_mA, ".1f") + "," + format(price, ".2f")
        self.app.buy_component(frag, qty)
        label = self._to_title(colour)
        print("Added " + format(voltage, ".1f") + "V " + format(current_mA, ".1f") + "mA " + label + " Light Globe $" + format(price, ".2f") + " X " + str(qty))

    def create_led_light(self) -> None:
        print("NEW LED LIGHT")
        print("LED Light Colours:")
        print("white, red, green, blue, yellow, orange, pink, aqua, violet")
        allowed = {"white","red","green","blue","yellow","orange","pink","aqua","violet"}
        colour = input("Please enter LED light colour: ").strip().lower()
        while colour not in allowed:
            print("Invalid colour. Valid: white, red, green, blue, yellow, orange, pink, aqua, violet")
            colour = input("Please enter LED light colour: ").strip().lower()
        print("Voltage is usually between 1 and 12")
        voltage = self._input_float("Please enter voltage (V): ", 0.0001, None)
        print("Current is usually between 100 and 1000 milliAmps")
        current_mA = self._input_float("Please enter current (mA): ", 0.0001, None)
        price = self._input_float("Please enter price: ", 0.0, None)
        qty = self._input_int("Please enter number of LED Lights: ", 1, None)
        frag = "LED Light," + colour + "," + format(voltage, ".1f") + "," + format(current_mA, ".1f") + "," + format(price, ".2f")
        self.app.buy_component(frag, qty)
        label = self._to_title(colour)
        print("Added " + format(voltage, ".1f") + "V " + format(current_mA, ".1f") + "mA " + label + " LED Light $" + format(price, ".2f") + " X " + str(qty))

    def create_switch(self) -> None:
        print("NEW SWITCH")
        print("Switch types:")
        print("push, slide, rocker, toggle")
        allowed = {"push","slide","rocker","toggle"}
        swtype = input("Please enter switch type: ").strip().lower()
        while swtype not in allowed:
            print("Invalid type. Valid: push, slide, rocker, toggle")
            swtype = input("Please enter switch type: ").strip().lower()
        print("Voltage is usually between 1 and 12")
        voltage = self._input_float("Please enter voltage (V): ", 0.0001, None)
        price = self._input_float("Please enter price: ", 0.0, None)
        qty = self._input_int("Please enter number of Switches: ", 1, None)
        frag = "Switch," + swtype + "," + format(voltage, ".1f") + "," + format(price, ".2f")
        self.app.buy_component(frag, qty)
        print("Added " + format(voltage, ".1f") + "V " + self._to_title(swtype) + " Switch $" + format(price, ".2f") + " X " + str(qty))

    def create_sensor(self) -> None:
        print("NEW SENSOR")
        print("Sensor types:")
        print("light, motion, infrared, sound, touch, dust, temperature, humidity")
        allowed = {"light","motion","infrared","sound","touch","dust","temperature","humidity"}
        stype = input("Please enter sensor type: ").strip().lower()
        while stype not in allowed:
            print("Invalid type. Valid: light, motion, infrared, sound, touch, dust, temperature, humidity")
            stype = input("Please enter sensor type: ").strip().lower()
        print("Voltage is usually between 1 and 12")
        voltage = self._input_float("Please enter voltage (V): ", 0.0001, None)
        price = self._input_float("Please enter price: ", 0.0, None)
        qty = self._input_int("Please enter number of Sensors: ", 1, None)
        frag = "Sensor," + stype + "," + format(voltage, ".1f") + "," + format(price, ".2f")
        self.app.buy_component(frag, qty)
        print("Added " + format(voltage, ".1f") + "V " + self._to_title(stype) + " Sensor $" + format(price, ".2f") + " X " + str(qty))

    def create_buzzer(self) -> None:
        print("NEW BUZZER")
        freq = self._input_float("Please enter frequency (Hz): ", 0.0001, None)
        spl  = self._input_float("Please enter sound pressure (dB): ", 0.0001, None)
        print("Voltage is usually between 1 and 12")
        voltage = self._input_float("Please enter voltage (V): ", 0.0001, None)
        print("Current is usually between 100 and 1000 milliAmps")
        current_mA = self._input_float("Please enter current (mA): ", 0.0001, None)
        price = self._input_float("Please enter price: ", 0.0, None)
        qty = self._input_int("Please enter number of Buzzers: ", 1, None)
        frag = "Buzzer," + format(freq, ".1f") + "," + format(spl, ".1f") + "," + format(voltage, ".1f") + "," + format(current_mA, ".1f") + "," + format(price, ".2f")
        self.app.buy_component(frag, qty)
        print("Added " + format(voltage, ".1f") + "V " + format(current_mA, ".1f") + "mA " + format(freq, ".1f") + "Hz " + str(int(round(spl))) + "dB Buzzer $" + format(price, ".2f") + " X " + str(qty))


class Menu:
    def __init__(self, app) -> None:
        self.app = app

    def run(self) -> None:
        UI(self.app).home()
