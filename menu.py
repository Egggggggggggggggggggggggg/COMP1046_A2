class Menu:
    def __init__(self, app: "App") -> None:
        self.app = app

    def main(self) -> None:
        while True:
            print("\nHOME MENU")
            print("1. COMPONENTS")
            print("2. CIRCUIT KITS")
            print("3. PURCHASE ORDERS")
            print("4. CUSTOMER SALES")
            print("5. TRANSACTION HISTORY")
            print("6. CLOSE")
            choice = input("Please enter a number: ").strip()
            if choice == "1":
                self._components_menu()
            elif choice == "2":
                self._circuits_menu()
            elif choice == "3":
                self._transactions_menu()
            elif choice == "4":
                print("Exiting...")
                return
            else:
                print("Invalid choice.")

    def _components_menu(self) -> None:
        print("[Components]")

    def _circuits_menu(self) -> None:
        print("[Circuits]")

    def _transactions_menu(self) -> None:
        print("[Transactions]")
