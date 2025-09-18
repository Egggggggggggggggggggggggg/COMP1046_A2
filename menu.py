from typing import Callable, Optional, List, Tuple, Any
from circuitkit.CircuitKit import CircuitKit


class Menu:
    '''
    Simple single-shot menu helper: prints a title and numbered options; runs selection.
    '''
    def __init__(self, title: str, options: List[tuple[str, Optional[Callable[[], None]]]], prompt: str = "Please enter a number: ") -> None:
        self._title = title
        self._options = options
        self._prompt = prompt

    def _input_select(self) -> Optional[Callable[[], None]]:
        print(self._title)
        for i, (name, _) in enumerate(self._options, 1):
            print(str(i) + ". " + name)
        sel = input(self._prompt).strip()
        try:
            idx = int(sel) - 1
        except Exception:
            print("Wrong input, must be a number.")
            return self._input_select()
        if idx < 0 or idx >= len(self._options):
            print("Wrong input, must be a number between 1 and " + str(len(self._options)))
            return self._input_select()
        name, fn = self._options[idx]
        print(name)
        return fn

    def run(self) -> None:
        fn = self._input_select()
        if fn is None:
            return
        try:
            fn()
        except SystemExit:
            raise
        except Exception as e:
            print("Error: " + str(e))


class UI:
    def __init__(self, app: Any) -> None:
        self.app = app

    def _input_int(self, prompt: str, min_val: Optional[int] = None, max_val: Optional[int] = None) -> int:
        s = input(prompt).strip()
        v = int(s)
        if min_val is not None and v < min_val:
            raise ValueError("Value must be at least " + str(min_val))
        if max_val is not None and v > max_val:
            raise ValueError("Value must be at most " + str(max_val))
        return v

    def _tc(self, s: str) -> str:
        if s is None or s == "":
            return ""
        return s[0:1].upper() + s[1:].lower()

    def _component_caps(self, frag: str) -> str:
        parts = [c.strip() for c in frag.split(",")]
        kind = parts[0] if len(parts) > 0 else ""
        def _f(x, n):
            try:
                return format(float(x), "." + str(n) + "f")
            except Exception:
                return x
        if kind == "Wire" and len(parts) >= 3:
            return _f(parts[1], 0) + "MM WIRE $" + _f(parts[2], 2)
        if kind == "Battery" and len(parts) >= 4:
            return _f(parts[2], 1) + "V " + parts[1].upper() + " BATTERY $" + _f(parts[3], 2)
        if kind == "Solar Panel" and len(parts) >= 4:
            try:
                ma = format(float(parts[2]) * 1000.0, ".1f")
            except Exception:
                ma = parts[2]
            return _f(parts[1], 1) + "V " + ma + "MA SOLAR PANEL $" + _f(parts[3], 2)
        if kind == "Light Globe" and len(parts) >= 5:
            return _f(parts[2], 1) + "V " + _f(parts[3], 1) + "MA " + parts[1].upper() + " LIGHT GLOBE $" + _f(parts[4], 2)
        if kind == "LED Light" and len(parts) >= 5:
            return _f(parts[2], 1) + "V " + _f(parts[3], 1) + "MA " + parts[1].upper() + " LED LIGHT $" + _f(parts[4], 2)
        if kind == "Switch" and len(parts) >= 4:
            return _f(parts[2], 1) + "V " + parts[1].upper() + " SWITCH $" + _f(parts[3], 2)
        if kind == "Sensor" and len(parts) >= 4:
            return _f(parts[2], 1) + "V " + parts[1].upper() + " SENSOR $" + _f(parts[3], 2)
        if kind == "Buzzer" and len(parts) >= 6:
            return _f(parts[3], 1) + "V " + _f(parts[4], 1) + "MA " + _f(parts[1], 1) + "HZ " + str(int(float(parts[2]))) + "DB BUZZER $" + _f(parts[5], 2)
        return frag.upper()

    def _component_pretty(self, frag: str) -> str:
        parts = [c.strip() for c in frag.split(",")]
        kind = parts[0] if len(parts) > 0 else ""
        def _f(x, n):
            try:
                return format(float(x), "." + str(n) + "f")
            except Exception:
                return x
        def _t(s):
            return self._tc(s)
        if kind == "Wire" and len(parts) >= 3:
            return _f(parts[1], 0) + "mm Wire $" + _f(parts[2], 2)
        if kind == "Battery" and len(parts) >= 4:
            return _f(parts[2], 1) + "V " + parts[1].upper() + " Battery $" + _f(parts[3], 2)
        if kind == "Solar Panel" and len(parts) >= 4:
            try:
                ma = format(float(parts[2]) * 1000.0, ".1f")
            except Exception:
                ma = parts[2]
            return _f(parts[1], 1) + "V " + ma + "mA Solar Panel $" + _f(parts[3], 2)
        if kind == "Light Globe" and len(parts) >= 5:
            return _f(parts[2], 1) + "V " + _f(parts[3], 1) + "mA " + _t(parts[1]) + " Light Globe $" + _f(parts[4], 2)
        if kind == "LED Light" and len(parts) >= 5:
            return _f(parts[2], 1) + "V " + _f(parts[3], 1) + "mA " + _t(parts[1]) + " LED Light $" + _f(parts[4], 2)
        if kind == "Switch" and len(parts) >= 4:
            return _f(parts[2], 1) + "V " + _t(parts[1]) + " Switch $" + _f(parts[3], 2)
        if kind == "Sensor" and len(parts) >= 4:
            return _f(parts[2], 1) + "V " + _t(parts[1]) + " Sensor $" + _f(parts[3], 2)
        if kind == "Buzzer" and len(parts) >= 6:
            return _f(parts[3], 1) + "V " + _f(parts[4], 1) + "mA " + _f(parts[1], 1) + "Hz " + str(int(float(parts[2]))) + "dB Buzzer $" + _f(parts[5], 2)
        return frag

    def _infer_kit_name(self, items: List[Tuple[int, str]]) -> str:
        has_globe = False
        has_led = False
        has_sensor = False
        for q, frag in items:
            t = frag.split(",")[0].strip()
            if t == "Light Globe":
                has_globe = True
            elif t == "LED Light":
                has_led = True
            elif t == "Sensor":
                has_sensor = True
        if has_sensor:
            return "Sensor Circuit"
        if has_globe or has_led:
            return "Light Circuit"
        return "Circuit"

    def home(self) -> None:
        Menu("HOME MENU", [
            ("COMPONENTS", self.components_menu),
            ("CIRCUIT KITS", self.circuits_menu),
            ("PURCHASE ORDERS", self.purchase_orders_menu),
            ("CUSTOMER SALES", self.customer_sales_menu),
            ("TRANSACTION HISTORY", self.transactions_menu),
            ("CLOSE", self.close_app),
        ]).run()
        self.home()

    def components_menu(self) -> None:
        Menu("COMPONENT MENU", [
            ("NEW COMPONENT", self.new_component_menu),
            ("VIEW COMPONENTS", self.view_components),
            ("BACK", None),
        ]).run()

    def new_component_menu(self) -> None:
        Menu("NEW COMPONENT MENU", [
            ("WIRE", lambda: print("NEW WIRE")),
            ("BATTERY", lambda: print("NEW BATTERY")),
            ("SOLAR PANEL", lambda: print("NEW SOLAR PANEL")),
            ("LIGHT GLOBE", lambda: print("NEW LIGHT GLOBE")),
            ("LED LIGHT", lambda: print("NEW LED LIGHT")),
            ("SWITCH", lambda: print("NEW SWITCH")),
            ("SENSOR", lambda: print("NEW SENSOR")),
            ("BUZZER", lambda: print("NEW BUZZER")),
            ("BACK", None),
        ]).run()

    def view_components(self) -> None:
        rows = self.app.list_component_rows()
        if not rows:
            print("ALL COMPONENTS")
            print("No components yet.")
            return
        options: List[Tuple[str, Optional[Callable[[], None]]]] = []
        for qty, frag in rows:
            label = self._component_caps(frag) + " X " + str(qty)
            options.append((label, (lambda f=frag: self._component_actions(f))))
        options.append(("BACK", None))
        Menu("ALL COMPONENTS", options).run()

    def _component_actions(self, frag: str) -> None:
        title = self._component_caps(frag)
        Menu(title, [
            ("BUY",  (lambda: self._buy_component(frag))),
            ("SELL", (lambda: self._sell_component(frag))),
            ("BACK", None),
        ]).run()
        self.view_components()

    def _buy_component(self, frag: str) -> None:
        pretty = self._component_pretty(frag)
        print("Buying " + pretty)
        qty = self._input_int("Please enter number of " + pretty + ": ", 1)
        self.app.buy_component(frag, qty)
        print("Bought " + self._component_caps(frag) + " X " + str(qty))
        print("Completing Purchase Order " + datetime_now())

    def _sell_component(self, frag: str) -> None:
        pretty = self._component_pretty(frag)
        print("Selling " + pretty)
        qty = self._input_int("Please enter number of " + pretty + ": ", 1)
        ok = self.app.sell_component(frag, qty)
        if ok:
            print("Sold " + pretty + " X " + str(qty))
            print("Completing Customer Sale " + datetime_now())
        else:
            print("Not enough stock.")

    def circuits_menu(self) -> None:
        Menu("CIRCUIT KIT MENU", [
            ("NEW CIRCUIT KIT", self.new_circuit_menu),
            ("VIEW CIRCUIT KITS", self.view_circuitkits),
            ("BACK", None),
        ]).run()

    def new_circuit_menu(self) -> None:
        comp_list = self.app.list_component_rows()
        if len(comp_list) == 0:
            print("NEW CIRCUIT KIT MENU")
            print("No components available.")
            return

        print("NEW CIRCUIT KIT MENU")
        chosen: List[Tuple[int, str]] = []
        picking = True
        while picking:
            index_map = {}
            for i, (qty, frag) in enumerate(comp_list, 1):
                print(str(i) + ". " + self._component_pretty(frag) + " X " + str(qty))
                index_map[i] = (qty, frag)
            print(str(len(comp_list) + 1) + ". DONE")
            sel = self._input_int("Please select the component index: ", 1, len(comp_list) + 1)
            if sel == len(comp_list) + 1:
                picking = False
                break
            have, frag = index_map[sel]
            want = self._input_int("Please enter number of " + self._component_pretty(frag) + ": ", 1)
            if want > have:
                print("Not enough in stock.")
                continue
            chosen.append((want, frag))
            print("Added " + str(want) + " x " + self._component_pretty(frag))

        if len(chosen) == 0:
            print("No items selected.")
            return

        base = self._infer_kit_name(chosen)
        name = input("Please enter kit name (default " + base + "): ").strip()
        if name == "":
            name = base

        total_price = 0.0
        for q, frag in chosen:
            try:
                unit = float(frag.split(",")[-1])
            except Exception:
                unit = 0.0
            total_price = total_price + (q * unit)

        kit = CircuitKit(name, total_price, chosen)
        count = self._input_int("Please enter number of " + kit.heading_pretty() + ": ", 1)
        if not self.app.can_pack(kit, count):
            print("Not enough components to pack the requested number.")
            return

        self.app.perform_pack(kit, count)
        print("Packed " + kit.heading_pretty() + " X " + str(count))

    def view_circuitkits(self) -> None:
        kits = self.app.list_circuit_objects()
        if len(kits) == 0:
            print("ALL CIRCUIT KITS")
            print("No circuit kits yet.")
            return
        options: List[Tuple[str, Optional[Callable[[], None]]]] = []
        for qty, kit in kits:
            options.append((kit.heading_caps() + " X " + str(qty), (lambda k=kit: self._kit_actions(k))))
        options.append(("BACK", None))
        Menu("ALL CIRCUIT KITS", options).run()

    def _kit_actions(self, kit: CircuitKit) -> None:
        Menu(kit.heading_pretty(), [
            ("SELL", (lambda: self._sell_kit(kit))),
            ("PACK", (lambda: self._pack_more(kit))),
            ("UNPACK", (lambda: self._unpack_kit(kit))),
            ("BUY", (lambda: self._buy_kit(kit))),
            ("BACK", None),
        ]).run()
        self.view_circuitkits()

    def _sell_kit(self, kit: CircuitKit) -> None:
        n = self._input_int("Please enter number of " + kit.heading_pretty() + ": ", 1)
        ok = self.app.sell_circuit(kit.name, n)
        if ok:
            print("Sold " + kit.heading_pretty() + " X " + str(n))
            print("Completing Customer Sale " + datetime_now())
        else:
            print("Not enough stock to sell.")

    def _pack_more(self, kit: CircuitKit) -> None:
        n = self._input_int("Please enter number of " + kit.heading_pretty() + ": ", 1)
        if not self.app.can_pack(kit, n):
            print("Not enough components to pack the requested number.")
            return
        self.app.perform_pack(kit, n)
        print("Packed " + kit.heading_pretty() + " X " + str(n))

    def _unpack_kit(self, kit: CircuitKit) -> None:
        n = self._input_int("Please enter number of " + kit.heading_pretty() + ": ", 1)
        if not self.app.can_unpack(kit.name, n):
            print("Not enough kits to unpack.")
            return
        self.app.perform_unpack(kit.name, n)
        print("Unpacked " + kit.heading_pretty() + " X " + str(n))

    def _buy_kit(self, kit: CircuitKit) -> None:
        n = self._input_int("Please enter number of " + kit.heading_pretty() + ": ", 1)
        ok = self.app.buy_circuit(kit.name, n)
        if ok:
            print("Bought " + kit.heading_pretty() + " X " + str(n))
            print("Completing Purchase Order " + datetime_now())
        else:
            print("Kit not found.")

    def purchase_orders_menu(self) -> None:
        Menu("PURCHASE ORDER", [
            ("Add Item from Catalogue to Order", self._purchase_add_item),
            ("BACK (CANCEL ORDER)", None),
        ], prompt="Select Option Number: ").run()

    def _purchase_add_item(self) -> None:
        comp = self.app.list_component_rows()
        kits = self.app.list_circuit_objects()
        index_map = {}
        i = 1
        print("PURCHASE ORDER")
        for qty, frag in comp:
            print(str(i) + ". " + self._component_caps(frag))
            index_map[i] = ("comp", frag)
            i = i + 1
        for qty, kit in kits:
            print(str(i) + ". " + kit.heading_caps())
            index_map[i] = ("kit", kit)
            i = i + 1
        print(str(i) + ". BACK")
        sel = self._input_int("Select Option Number: ", 1, i)
        if sel == i:
            return
        kind, obj = index_map[sel]
        q = self._input_int("Quantity: ", 1)
        if kind == "comp":
            self.app.buy_component(obj, q)
            print("Adding " + str(q) + " x " + self._component_caps(obj))
        else:
            ok = self.app.buy_circuit(obj.name, q)
            if ok:
                print("Adding " + str(q) + " x " + obj.heading_caps())
            else:
                print("Kit not found.")

    def customer_sales_menu(self) -> None:
        Menu("CUSTOMER SALE", [
            ("Add Item from Inventory to Sale", self._customer_sale_add_item),
            ("BACK (CANCEL ORDER)", None),
        ], prompt="Select Option Number: ").run()

    def _customer_sale_add_item(self) -> None:
        comp = self.app.list_component_rows()
        kits = self.app.list_circuit_objects()
        index_map = {}
        i = 1
        print("CUSTOMER SALE INVENTORY")
        for qty, frag in comp:
            print(str(i) + ". " + self._component_caps(frag) + " X " + str(qty))
            index_map[i] = ("comp", frag, qty)
            i = i + 1
        for qty, kit in kits:
            print(str(i) + ". " + kit.heading_caps() + " X " + str(qty))
            index_map[i] = ("kit", kit, qty)
            i = i + 1
        print(str(i) + ". BACK")
        sel = self._input_int("Select Option Number: ", 1, i)
        if sel == i:
            return
        kind, obj, have = index_map[sel]
        q = self._input_int("Quantity: ", 1)
        if q > have:
            print("Not enough stock.")
            return
        if kind == "comp":
            ok = self.app.sell_component(obj, q)
            if ok:
                print("Adding " + str(q) + " x " + self._component_caps(obj))
            else:
                print("Not enough stock.")
        else:
            ok = self.app.sell_circuit(obj.name, q)
            if ok:
                print("Adding " + str(q) + " x " + obj.heading_caps())
            else:
                print("Not enough stock.")

    def transactions_menu(self) -> None:
        lines = self.app.summarize_transactions()
        print("TRANSACTION HISTORY")
        if len(lines) == 0:
            print("No transactions yet.")
        else:
            for i, (op, ts, total) in enumerate(lines, 1):
                print(str(i) + ". " + op + " " + ts + ", total $" + format(total, ".2f"))
        Menu("TRANSACTION HISTORY", [
            ("SORT", lambda: None),
            ("BACK", None),
        ], prompt="Select Option Number: ").run()

    def close_app(self) -> None:
        print("Saving and Closing")
        self.app.save_components()
        self.app.save_kits()
        raise SystemExit(0)

    def datetime_now() -> str:
        import datetime
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
