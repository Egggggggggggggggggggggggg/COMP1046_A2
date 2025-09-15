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
                    return
                action()
            except ValueError:
                print(f"Wrong input, must be a number between 1 and {len(options)}")
            except Exception as e:
                print("Error:", e)

    # ============= Menu =============

    def main(self) -> None:
        options = [
            ("COMPONENTS", self._components_menu),
            ("CIRCUIT KITS", self._circuits_menu),
            ("PURCHASE ORDERS", self._purchase_orders_menu),
            ("CUSTOMER SALES", self._customer_sales_menu),
            ("TRANSACTION HISTORY", self._transactions_menu),
            ("CLOSE", None)
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
            ("WIRE", lambda: print("[TODO] Create Wire")),
            ("BATTERY", lambda: print("[TODO] Create Battery")),
            ("SOLAR PANEL", lambda: print("[TODO] Create Solar Panel")),
            ("LIGHT GLOBE", lambda: print("[TODO] Create Light Globe")),
            ("LED LIGHT", lambda: print("[TODO] Create LED Light")),
            ("SWITCH", lambda: print("[TODO] Create Switch")),
            ("SENSOR", lambda: print("[TODO] Create Sensor")),
            ("BUZZER", lambda: print("[TODO] Create Buzzer")),
            ("BACK", None)
        ]
        self._show_menu("NEW COMPONENT MENU", options)

    def _circuits_menu(self) -> None:
        print("[Circuits Menu TODO]")

    def _purchase_orders_menu(self) -> None:
        print("[Purchase Orders Menu TODO]")

    def _customer_sales_menu(self) -> None:
        print("[Customer Sales Menu TODO]")

    def _transactions_menu(self) -> None:
        print("[Transactions Menu TODO]")

    def _view_components(self) -> None:
        print("[View Components TODO]")
