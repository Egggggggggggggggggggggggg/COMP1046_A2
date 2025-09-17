from typing import Callable, Optional, List, Tuple
from app import App

from component.Component import Component
from component.Light import Light
from component.Battery import Battery
from component.Buzzer import Buzzer

class Menu:
    def __init__(self, title: str, options: List[tuple[str, Optional[Callable[[], None]]]], prompt: str = "Please enter a number: ") -> None:
        self._title = title
        self._options = options
        self._prompt = prompt

    def _input_select(self) -> Optional[Callable[[], None]]:
        sel = input(self._prompt).strip()
        idx = int(sel) - 1
        if idx < 0 or idx >= len(self._options):
            raise ValueError("Wrong input, must be a number between 1 and " + str(len(self._options)))
        name, fn = self._options[idx]
        print(name)
        return fn

    def run(self) -> None:
        print(self._title)
        for i, (name, _) in enumerate(self._options, 1):
            print(str(i) + ". " + name)
        try:
            fn = self._input_select()
            if fn is None:
                return
            fn()
        except ValueError as e:
            print(str(e))
            self.run()
        except Exception as e:
            print("Error: " + str(e))
            self.run()


class UI:
    def __init__(self, app: App) -> None:
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

    def _title_case(self, text: str) -> str:
        return text[:1].upper() + text[1:].lower() if text else text

    #       HOME
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

    #       COMPONENTS
    def components_menu(self) -> None:
        Menu("COMPONENT MENU", [
            ("NEW COMPONENT", self.new_component_menu),
            ("VIEW COMPONENTS", self.view_components),
            ("BACK", None),
        ]).run()

    def new_component_menu(self) -> None:
        Menu("NEW COMPONENT MENU", [
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

    def create_wire(self) -> None:
        print("NEW WIRE")
        length_mm = self._input_float("Please enter length (mm): ", min_val=0.001)
        price = self._input_float("Please enter price: ", min_val=0.0)
        qty = self._input_int("Please enter number of Wires: ", min_val=1)
        comp = Component(str(int(length_mm)) + "mm Wire", price)
        self.app.add_circuitkit_object(qty, comp)
        print("Added " + format(length_mm, ".0f") + "mm Wire $" + format(price, ".2f") + " X " + str(qty))

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
        voltage = self._input_float("Please enter a voltage that matches the battery size: ", min_val=0.0)
        while round(voltage, 2) not in [round(v, 2) for v in valid[size]]:
            print("Voltage does not match the selected size. Allowed: " + ", ".join(map(str, valid[size])))
            voltage = self._input_float("Please enter a voltage that matches the battery size: ", min_val=0.0)
        price = self._input_float("Please enter price: ", min_val=0.0)
        qty = self._input_int("Please enter number of Batteries: ", min_val=1)
        comp = Battery(size + " Battery", price, voltage)
        self.app.add_circuitkit_object(qty, comp)
        print("Added " + format(voltage, ".1f") + "V " + size + " Battery $" + format(price, ".2f") + " X " + str(qty))

    def create_solar_panel(self) -> None:
        print("NEW SOLAR PANEL")
        print("Voltage is usually between 1 and 12")
        voltage = self._input_float("Please enter voltage (V): ", min_val=0.0001)
        print("Current is usually between 100 and 1000 milliAmps")
        current_mA = self._input_float("Please enter current (mA): ", min_val=0.0001)
        price = self._input_float("Please enter price: ", min_val=0.0)
        qty = self._input_int("Please enter number of Solar Panels: ", min_val=1)
        comp = Light("Solar Panel", price, "", voltage, current_mA / 1000.0)
        self.app.add_circuitkit_object(qty, comp)
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
        voltage = self._input_float("Please enter voltage (V): ", min_val=0.0001)
        print("Current is usually between 100 and 1000 milliAmps")
        current_mA = self._input_float("Please enter current (mA): ", min_val=0.0001)
        price = self._input_float("Please enter price: ", min_val=0.0)
        qty = self._input_int("Please enter number of Light Globes: ", min_val=1)
        comp = Light("Light Globe", price, colour, voltage, current_mA / 1000.0)
        self.app.add_circuitkit_object(qty, comp)
        label = self._title_case(colour)
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
        voltage = self._input_float("Please enter voltage (V): ", min_val=0.0001)
        print("Current is usually between 100 and 1000 milliAmps")
        current_mA = self._input_float("Please enter current (mA): ", min_val=0.0001)
        price = self._input_float("Please enter price: ", min_val=0.0)
        qty = self._input_int("Please enter number of LED Lights: ", min_val=1)
        comp = Light("LED Light", price, colour, voltage, current_mA / 1000.0)
        self.app.add_circuitkit_object(qty, comp)
        label = self._title_case(colour)
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
        voltage = self._input_float("Please enter voltage (V): ", min_val=0.0001)
        price = self._input_float("Please enter price: ", min_val=0.0)
        qty = self._input_int("Please enter number of Switches: ", min_val=1)
        comp = Component(self._title_case(swtype) + " Switch", price)
        self.app.add_circuitkit_object(qty, comp)
        print("Added " + format(voltage, ".1f") + "V " + self._title_case(swtype) + " Switch $" + format(price, ".2f") + " X " + str(qty))

    def create_sensor(self) -> None:
        print("NEW SENSOR")
        print("Sensor types:")
        print("light, motion, infrared, sound, touch, dust, temperature, humidity")
        allowed = {"light","motion","infrared","sound","touch","dust","temperature","humidity"}
        stype = input("Please enter sensor type: ").strip().lower()
        while stype not in allowed:
            print("Invalid type. Valid: " + ", ".join(sorted(allowed)))
            stype = input("Please enter sensor type: ").strip().lower()
        print("Voltage is usually between 1 and 12")
        voltage = self._input_float("Please enter voltage (V): ", min_val=0.0001)
        price = self._input_float("Please enter price: ", min_val=0.0)
        qty = self._input_int("Please enter number of Sensors: ", min_val=1)
        comp = Component(self._title_case(stype) + " Sensor", price)
        self.app.add_circuitkit_object(qty, comp)
        print("Added " + format(voltage, ".1f") + "V " + self._title_case(stype) + " Sensor $" + format(price, ".2f") + " X " + str(qty))

    def create_buzzer(self) -> None:
        print("NEW BUZZER")
        freq = self._input_float("Please enter frequency (Hz): ", min_val=0.0001)
        spl  = self._input_float("Please enter sound pressure (dB): ", min_val=0.0001)
        print("Voltage is usually between 1 and 12")
        voltage = self._input_float("Please enter voltage (V): ", min_val=0.0001)
        print("Current is usually between 100 and 1000 milliAmps")
        current_mA = self._input_float("Please enter current (mA): ", min_val=0.0001)
        price = self._input_float("Please enter price: ", min_val=0.0)
        qty = self._input_int("Please enter number of Buzzers: ", min_val=1)
        comp = Buzzer("Buzzer", price, voltage, current_mA / 1000.0, freq, spl)
        self.app.add_circuitkit_object(qty, comp)
        print("Added " + format(voltage, ".1f") + "V " + format(current_mA, ".1f") + "mA " +
              format(freq, ".1f") + "Hz " + str(int(spl)) + "dB Buzzer $" + format(price, ".2f") + " X " + str(qty))

    #       VIEW/BUY/SELL
    def _format_component_row_for_list(self, row: List[str]) -> str:
        """
        Per-kind formatting for ALL COMPONENTS list (all-caps style).
        """
        if not row or len(row) < 2:
            return "INVALID ROW"

        qty = row[0]
        kind = row[1].strip().lower()

        def _fmt(val: str, digits: int) -> str:
            try:
                return format(float(val), "." + str(digits) + "f")
            except Exception:
                return val

        if kind == "wire":
            length_mm = _fmt(row[2], 0)
            price = _fmt(row[3], 2)
            return length_mm + "MM WIRE $" + price + " X " + qty

        if kind == "battery":
            size = row[2].upper()
            voltage = _fmt(row[3], 1)
            price = _fmt(row[4], 2)
            return voltage + "V " + size + " BATTERY $" + price + " X " + qty

        if kind == "solar panel":
            voltage = _fmt(row[2], 1)
            try:
                current_mA = float(row[3]) * 1000.0
                current_str = format(current_mA, ".1f")
            except Exception:
                current_str = row[3]
            price = _fmt(row[4], 2)
            return voltage + "V " + current_str + "MA SOLAR PANEL $" + price + " X " + qty

        if kind == "light globe":
            colour = row[2].upper()
            voltage = _fmt(row[3], 1)
            current_mA = _fmt(row[4], 1)
            price = _fmt(row[5], 2)
            return voltage + "V " + current_mA + "MA " + colour + " LIGHT GLOBE $" + price + " X " + qty

        if kind == "led light":
            colour = row[2].upper()
            voltage = _fmt(row[3], 1)
            current_mA = _fmt(row[4], 1)
            price = _fmt(row[5], 2)
            return voltage + "V " + current_mA + "MA " + colour + " LED LIGHT $" + price + " X " + qty

        if kind == "switch":
            swtype = row[2].upper()
            voltage = _fmt(row[3], 1)
            price = _fmt(row[4], 2)
            return voltage + "V " + swtype + " SWITCH $" + price + " X " + qty

        if kind == "sensor":
            stype = row[2].upper()
            voltage = _fmt(row[3], 1)
            price = _fmt(row[4], 2)
            return voltage + "V " + stype + " SENSOR $" + price + " X " + qty

        if kind == "buzzer":
            freq = _fmt(row[2], 1)
            try:
                spl_int = str(int(float(row[3])))
            except Exception:
                spl_int = row[3]
            voltage = _fmt(row[4], 1)
            current_mA = _fmt(row[5], 1)
            price = _fmt(row[6], 2)
            return voltage + "V " + current_mA + "MA " + freq + "HZ " + spl_int + "DB BUZZER $" + price + " X " + qty

        name = " ".join(row[1:]).upper()
        return name + " X " + qty

    def _format_component_heading_caps(self, row: List[str]) -> str:
        # e.g. 1.4V 0.4MA SOLAR PANEL $14.00
        kind = row[1].strip().lower()

        def _f(v, n):
            try:
                return format(float(v), "." + str(n) + "f")
            except:
                return v

        if kind == "wire":
            return _f(row[2], 0) + "MM WIRE $" + _f(row[3], 2)

        if kind == "battery":
            return _f(row[3], 1) + "V " + row[2].upper() + " BATTERY $" + _f(row[4], 2)

        if kind == "solar panel":
            v = _f(row[2], 1)
            try:
                ma = format(float(row[3]) * 1000.0, ".1f")
            except:
                ma = row[3]
            return v + "V " + ma + "MA SOLAR PANEL $" + _f(row[4], 2)

        if kind == "light globe":
            return _f(row[3], 1) + "V " + _f(row[4], 1) + "MA " + row[2].upper() + " LIGHT GLOBE $" + _f(row[5], 2)

        if kind == "led light":
            return _f(row[3], 1) + "V " + _f(row[4], 1) + "MA " + row[2].upper() + " LED LIGHT $" + _f(row[5], 2)

        if kind == "switch":
            return _f(row[3], 1) + "V " + row[2].upper() + " SWITCH $" + _f(row[4], 2)

        if kind == "sensor":
            return _f(row[3], 1) + "V " + row[2].upper() + " SENSOR $" + _f(row[4], 2)

        if kind == "buzzer":
            return _f(row[4], 1) + "V " + _f(row[5], 1) + "MA " + _f(row[2], 1) + "HZ " + str(int(float(row[3]))) + "DB BUZZER $" + _f(row[6], 2)

        return " ".join(row[1:]).upper()

    def _format_component_heading_pretty(self, row: List[str]) -> str:
        # e.g. 1.4V 0.4mA Solar Panel $14.00
        kind = row[1].strip().lower()

        def _f(v, n):
            try:
                return format(float(v), "." + str(n) + "f")
            except:
                return v

        def _tc(s):
            return s[:1].upper() + s[1:].lower()

        if kind == "wire":
            return _f(row[2], 0) + "mm Wire $" + _f(row[3], 2)

        if kind == "battery":
            return _f(row[3], 1) + "V " + row[2].upper() + " Battery $" + _f(row[4], 2)

        if kind == "solar panel":
            v = _f(row[2], 1)
            try:
                ma = format(float(row[3]) * 1000.0, ".1f")
            except:
                ma = row[3]
            return v + "V " + ma + "mA Solar Panel $" + _f(row[4], 2)

        if kind == "light globe":
            return _f(row[3], 1) + "V " + _f(row[4], 1) + "mA " + _tc(row[2]) + " Light Globe $" + _f(row[5], 2)

        if kind == "led light":
            return _f(row[3], 1) + "V " + _f(row[4], 1) + "mA " + _tc(row[2]) + " LED Light $" + _f(row[5], 2)

        if kind == "switch":
            return _f(row[3], 1) + "V " + _tc(row[2]) + " Switch $" + _f(row[4], 2)

        if kind == "sensor":
            return _f(row[3], 1) + "V " + _tc(row[2]) + " Sensor $" + _f(row[4], 2)

        if kind == "buzzer":
            return _f(row[4], 1) + "V " + _f(row[5], 1) + "mA " + _f(row[2], 1) + "Hz " + str(int(float(row[3]))) + "dB Buzzer $" + _f(row[6], 2)

        return " ".join(row[1:])

    def view_components(self) -> None:
        rows = self.app.list_circuitKit()
        print("ALL COMPONENTS")
        if not rows:
            print("No components yet.")
            return

        options = []
        for idx, row in enumerate(rows):
            label = self._format_component_row_for_list(row)
            options.append((label, (lambda i=idx: self._component_actions(i))))
        options.append(("BACK", None))

        Menu("ALL COMPONENTS", options).run()

    def _component_actions(self, row_index: int) -> None:
        row = self.app.get_circuitkit_row(row_index)
        title = self._format_component_heading_caps(row)
        print(title)
        Menu(title, [
            ("BUY",  (lambda: self._buy_component(row_index))),
            ("SELL", (lambda: self._sell_component(row_index))),
            ("BACK", None),
        ]).run()
        self.view_components()

    def _buy_component(self, row_index: int) -> None:
        row = self.app.get_circuitkit_row(row_index)
        pretty = self._format_component_heading_pretty(row)
        print("Buying " + pretty)
        qty = self._input_int("Please enter number of " + pretty + ": ", min_val=1)
        self.app.change_circuitkit_qty(row_index, qty)
        ts = __import__("datetime").datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.app.add_component_transaction("Purchase Order", row, qty, ts)
        caps = self._format_component_heading_caps(row)
        print("Bought " + caps + " X " + str(qty))
        print("Completing Purchase Order " + ts)

    def _sell_component(self, row_index: int) -> None:
        row = self.app.get_circuitkit_row(row_index)
        pretty = self._format_component_heading_pretty(row)
        print("Selling " + pretty)
        qty = self._input_int("Please enter number of " + pretty + ": ", min_val=1)
        self.app.change_circuitkit_qty(row_index, -qty)
        ts = __import__("datetime").datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.app.add_component_transaction("Customer Sale", row, qty, ts)
        print("Sold " + pretty + " X " + str(qty))
        print("Completing Customer Sale " + ts)

    #       CIRCUIT KITS
    def circuits_menu(self) -> None:
        Menu("CIRCUIT KIT MENU", [
            ("NEW CIRCUIT KIT", self.new_circuit_menu),
            ("VIEW CIRCUIT KITS", self.view_circuitkits),
            ("BACK", None),
        ]).run()

    def new_circuit_menu(self) -> None:
        Menu("NEW CIRCUIT KIT MENU", [
            ("LIGHT GLOBE CIRCUIT KIT", lambda: print("[TODO] Create Light Globe Circuit Kit")),
            ("LED LIGHT CIRCUIT KIT",   lambda: print("[TODO] Create LED Light Circuit Kit")),
            ("SENSOR CIRCUIT KIT WITH LIGHT GLOBE", lambda: print("[TODO] Create Sensor+Globe Circuit Kit")),
            ("SENSOR CIRCUIT KIT WITH LED LIGHT",   lambda: print("[TODO] Create Sensor+LED Circuit Kit")),
            ("SENSOR CIRCUIT KIT WITH BUZZER",      lambda: print("[TODO] Create Sensor+Buzzer Circuit Kit")),
            ("SENSOR CIRCUIT KIT WITH LIGHT GLOBE AND SWITCH", lambda: print("[TODO] Create Sensor+Globe+Switch Circuit Kit")),
            ("SENSOR CIRCUIT KIT WITH LED LIGHT AND SWITCH",   lambda: print("[TODO] Create Sensor+LED+Switch Circuit Kit")),
            ("SENSOR CIRCUIT KIT WITH BUZZER AND SWITCH",      lambda: print("[TODO] Create Sensor+Buzzer+Switch Circuit Kit")),
            ("BACK", None),
        ]).run()

    def view_circuitkits(self) -> None:
        print("ALL CIRCUIT KITS (inventory in circuitKit.csv)")
        rows = self.app.list_circuitKit()
        if not rows:
            print("No circuit kits yet.")
            return
        for i, row in enumerate(rows, 1):
            print(str(i) + " " + ", ".join(row))

    #       PURCHASE/SALES
    def purchase_orders_menu(self) -> None:
        Menu("PURCHASE ORDERS MENU", [
            ("NEW PURCHASE ORDER", lambda: print("[TODO] Create Purchase Order")),
            ("VIEW PURCHASE ORDERS", lambda: print("[TODO] View Purchase Orders")),
            ("BACK", None),
        ]).run()

    def customer_sales_menu(self) -> None:
        Menu("CUSTOMER SALES MENU", [
            ("NEW CUSTOMER SALE", lambda: print("[TODO] Create Customer Sale")),
            ("VIEW CUSTOMER SALES", lambda: print("[TODO] View Customer Sales")),
            ("BACK", None),
        ]).run()

    def transactions_menu(self) -> None:
        Menu("TRANSACTION HISTORY MENU", [
            ("VIEW ALL TRANSACTIONS", self.view_transactions),
            ("SORT TRANSACTIONS", self.sort_transactions_menu),
            ("BACK", None),
        ]).run()

    def view_transactions(self) -> None:
        print("ALL TRANSACTIONS")
        rows = self.app.list_transactions()
        if not rows:
            print("No transactions yet.")
            return
        for i, row in enumerate(rows, 1):
            print(str(i) + " " + ", ".join(row))

    def sort_transactions_menu(self) -> None:
        Menu("SORT TRANSACTIONS MENU", [
            ("BY DATE ASCENDING", lambda: print("[TODO] Sort Date Asc")),
            ("BY DATE DESCENDING", lambda: print("[TODO] Sort Date Desc")),
            ("BY WHOLESALE PRICE ASCENDING", lambda: print("[TODO] Sort Wholesale Asc")),
            ("BY WHOLESALE PRICE DESCENDING", lambda: print("[TODO] Sort Wholesale Desc")),
            ("BY RETAIL PRICE ASCENDING", lambda: print("[TODO] Sort Retail Asc")),
            ("BY RETAIL PRICE DESCENDING", lambda: print("[TODO] Sort Retail Desc")),
            ("BACK", None),
        ]).run()

    #       CLOSE
    def close_app(self) -> None:
        print("Saving and Closing")
        self.app.save()
        raise SystemExit(0)
