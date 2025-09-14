class Menu:
    def __init__(self, app: "App") -> None:
        self.app = app

    def main(self) -> None:
        while True:
            print("\n=== Main Menu ===")
            print("1) Components")
            print("2) Circuits")
            print("3) Transactions")
            print("4) Exit")
            choice = input("Select: ").strip()
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
