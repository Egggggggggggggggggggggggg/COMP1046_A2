class Menu:
    def __init__(self, app: "App") -> None:
        self.app = app


    def _show_menu(self, title: str, options: list[tuple[str, callable]]) -> None:
        while True:
            print("\n" + title)
            for i, option in enumerate(options, start=1):
                print(str(i) + ". " + option[0])
            choice = input("Please enter a number: ").strip()
            try:
                index = int(choice) - 1
                if index < 0 or index >= len(options):
                    raise ValueError
                name, action = options[index]
                if action is None:
                    return  # BACK
                action()
            except ValueError:
                print("Wrong input, must be a number between 1 and " + str(len(options)))
            except Exception as e:
                print("Error:", e)

    def _input_int(self, prompt: str, min_val: int = None, max_val: int = None) -> int:
        while True:
            s = input(prompt).strip()
            try:
                v = int(s)
                if min_val is not None and v < min_val:
                    print("Value must be at least " + str(min_val))
                    continue
                if max_val is not None and v > max_val:
                    print("Value must be at most " + str(max_val))
                    continue
                return v
            except Exception:
                print("Please enter a valid integer.")

    def _input_float(self, prompt: str, min_val: float = None, max_val: float = None) -> float:
        while True:
            s = input(prompt).strip()
            try:
                v = float(s)
                if min_val is not None and v < min_val:
                    print("Value must be at least " + str(min_val))
                    continue
                if max_val is not None and v > max_val:
                    print("Value must be at most " + str(max_val))
                    continue
                return v
            except Exception:
                print("Please enter a valid number.")

    def _title_case(self, text: str) -> str:
        if not text:
            return text
        return text[0].upper() + text[1:].lower()

    def _maybe_store(self, kind: str, payload: dict) -> None:
        try:
            if self.app and hasattr(self.app, "add_component"):
                self.app.add_component(kind, payload)
        except Exception as e:
            print("WARN: failed to store into app:", e)

    def main(self) -> None:
        options = [
            ("COMPONENTS", self._components_menu),
            ("CIRCUIT KITS", self._circuits_menu),
            ("PURCHASE ORDERS", self._purchase_orders_menu),
            ("CUSTOMER SALES", self._customer_sales_menu),
            ("TRANSACTION HISTORY", self._transactions_menu),
            ("CLOSE", self._close_app)
        ]
        self._show_menu("HOME MENU", options)

    def _components_menu(self) -> None:
        options = [
            ("NEW COMPONENT", self._new_component_menu),
            ("VIEW COMPONENTS", self._view_components),
            ("BACK", None)
        ]
        self._show_menu("COMPONENT MENU", options)

    def _new_component_menu(self) -> None:
        options = [
            ("WIRE", self._create_wire),
            ("BATTERY", self._create_battery),
            ("SOLAR PANEL", self._create_solar_panel),
            ("LIGHT GLOBE", self._create_light_globe),
            ("LED LIGHT", self._create_led_light),
            ("BACK", None)
        ]
        self._show_menu("NEW COMPONENT MENU", options)

    def _create_wire(self) -> None:
        print("NEW WIRE")
        length_mm = self._input_float("Please enter length (mm): ", min_val=0.001)
        price = self._input_float("Please enter price: ", min_val=0.0)
        qty = self._input_int("Please enter number of Wires: ", min_val=1)

        self._maybe_store("Wire", {
            "length_mm": length_mm,
            "price": price,
            "qty": qty
        })

        print("Added " + format(length_mm, ".0f") + "mm Wire $" + format(price, ".2f") + " X " + str(qty))

    def _create_battery(self) -> None:
        print("NEW BATTERY")
        print("Battery sizes are AA or AAA or C or D or E")
        size = input("Please enter battery size: ").strip().upper()

        valid_sizes = ["AA", "AAA", "C", "D", "E"]
        while size not in valid_sizes:
            print("Invalid size. Valid: AA, AAA, C, D, E")
            size = input("Please enter battery size: ").strip().upper()

        print("AA, AAA and C batteries are either 1.2 Volts or 1.5 Volts")
        print("D batteries are 1.5 Volts")
        print("E batteries are 9.0 Volts")

        allowed_voltages = []
        if size in ["AA", "AAA", "C"]:
            allowed_voltages = [1.2, 1.5]
        elif size == "D":
            allowed_voltages = [1.5]
        elif size == "E":
            allowed_voltages = [9.0]

        voltage = self._input_float("Please enter a voltage that matches the battery size: ", min_val=0.0)
        while float("{:.2f}".format(voltage)) not in [float("{:.2f}".format(v)) for v in allowed_voltages]:
            print("Voltage does not match the selected size. Allowed: " + ", ".join([str(v) for v in allowed_voltages]))
            voltage = self._input_float("Please enter a voltage that matches the battery size: ", min_val=0.0)

        price = self._input_float("Please enter price: ", min_val=0.0)
        qty = self._input_int("Please enter number of Batteries: ", min_val=1)

        self._maybe_store("Battery", {
            "size": size,
            "voltage": voltage,
            "price": price,
            "qty": qty
        })

        print("Added " + format(voltage, ".1f") + "V " + size + " Battery $" + format(price, ".2f") + " X " + str(qty))

    def _create_solar_panel(self) -> None:
        print("NEW SOLAR PANEL")
        print("Voltage is usually between 1 and 12")
        voltage = self._input_float("Please enter voltage (V): ", min_val=0.0001)
        print("Current is usually between 100 and 1000 milliAmps")
        current_ma = self._input_float("Please enter current (mA): ", min_val=0.0001)
        price = self._input_float("Please enter price: ", min_val=0.0)
        qty = self._input_int("Please enter number of Solar Panels: ", min_val=1)

        self._maybe_store("SolarPanel", {
            "voltage": voltage,
            "current_mA": current_ma,
            "price": price,
            "qty": qty
        })

        print("Added " + format(voltage, ".1f") + "V " + format(current_ma, ".1f") + "mA Solar Panel $" +
              format(price, ".2f") + " X " + str(qty))

    def _create_light_globe(self) -> None:
        print("NEW LIGHT GLOBE")
        print("Light Globe Colours:")
        print("warm, neutral, cool")

        allowed = ["warm", "neutral", "cool"]
        colour = input("Please enter light globe colour: ").strip().lower()
        while colour not in allowed:
            print("Invalid colour. Valid: warm, neutral, cool")
            colour = input("Please enter light globe colour: ").strip().lower()

        print("Voltage is usually between 1 and 12")
        voltage = self._input_float("Please enter voltage (V): ", min_val=0.0001)
        print("Current is usually between 100 and 1000 milliAmps")
        current_ma = self._input_float("Please enter current (mA): ", min_val=0.0001)
        price = self._input_float("Please enter price: ", min_val=0.0)
        qty = self._input_int("Please enter number of Light Globes: ", min_val=1)

        self._maybe_store("LightGlobe", {
            "colour": colour,
            "voltage": voltage,
            "current_mA": current_ma,
            "price": price,
            "qty": qty
        })

        label_colour = self._title_case(colour)
        print("Added " + format(voltage, ".1f") + "V " + format(current_ma, ".1f") + "mA " + label_colour +
              " Light Globe $" + format(price, ".2f") + " X " + str(qty))

    def _create_led_light(self) -> None:
        print("NEW LED LIGHT")
        print("LED Light Colours:")
        print("white, red, green, blue, yellow, orange, pink, aqua, violet")

        allowed = ["white", "red", "green", "blue", "yellow", "orange", "pink", "aqua", "violet"]
        colour = input("Please enter LED light colour: ").strip().lower()
        while colour not in allowed:
            print("Invalid colour. Valid: white, red, green, blue, yellow, orange, pink, aqua, violet")
            colour = input("Please enter LED light colour: ").strip().lower()

        print("Voltage is usually between 1 and 12")
        voltage = self._input_float("Please enter voltage (V): ", min_val=0.0001)
        print("Current is usually between 100 and 1000 milliAmps")
        current_ma = self._input_float("Please enter current (mA): ", min_val=0.0001)
        price = self._input_float("Please enter price: ", min_val=0.0)
        qty = self._input_int("Please enter number of LED Lights: ", min_val=1)

        self._maybe_store("LEDLight", {
            "colour": colour,
            "voltage": voltage,
            "current_mA": current_ma,
            "price": price,
            "qty": qty
        })

        label_colour = self._title_case(colour)
        print("Added " + format(voltage, ".1f") + "V " + format(current_ma, ".1f") + "mA " + label_colour +
              " LED Light $" + format(price, ".2f") + " X " + str(qty))

    
    def _view_components(self) -> None:
        print("[TODO] View all components")

    def _circuits_menu(self) -> None:
        options = [
            ("NEW CIRCUIT KIT", self._new_circuit_menu),
            ("VIEW CIRCUIT KITS", self._view_circuits),
            ("BACK", None)
        ]
        self._show_menu("CIRCUIT KIT MENU", options)

    def _new_circuit_menu(self) -> None:
        options = [
            ("LIGHT CIRCUIT KIT", lambda: print("[TODO] Create Light Circuit Kit")),
            ("SENSOR CIRCUIT KIT", lambda: print("[TODO] Create Sensor Circuit Kit")),
            ("BACK", None)
        ]
        self._show_menu("NEW CIRCUIT KIT MENU", options)

    def _view_circuits(self) -> None:
        print("[TODO] View all circuit kits")

    def _purchase_orders_menu(self) -> None:
        options = [
            ("NEW PURCHASE ORDER", lambda: print("[TODO] Create Purchase Order")),
            ("VIEW PURCHASE ORDERS", lambda: print("[TODO] View Purchase Orders")),
            ("BACK", None)
        ]
        self._show_menu("PURCHASE ORDERS MENU", options)

    def _customer_sales_menu(self) -> None:
        options = [
            ("NEW CUSTOMER SALE", lambda: print("[TODO] Create Customer Sale")),
            ("VIEW CUSTOMER SALES", lambda: print("[TODO] View Customer Sales")),
            ("BACK", None)
        ]
        self._show_menu("CUSTOMER SALES MENU", options)

    def _transactions_menu(self) -> None:
        options = [
            ("VIEW ALL TRANSACTIONS", lambda: print("[TODO] View Transactions")),
            ("SORT TRANSACTIONS", self._sort_transactions_menu),
            ("BACK", None)
        ]
        self._show_menu("TRANSACTION HISTORY MENU", options)

    def _sort_transactions_menu(self) -> None:
        options = [
            ("BY DATE ASCENDING", lambda: print("[TODO] Sort Date Asc")),
            ("BY DATE DESCENDING", lambda: print("[TODO] Sort Date Desc")),
            ("BY PRICE ASCENDING", lambda: print("[TODO] Sort Price Asc")),
            ("BY PRICE DESCENDING", lambda: print("[TODO] Sort Price Desc")),
            ("BACK", None)
        ]
        self._show_menu("SORT TRANSACTIONS MENU", options)

    def _close_app(self) -> None:
        print("Saving and Closing...")
        #save data if exists
        exit(0)
