class Menu:
    def __init__(self, app: "App") -> None:
        self.app = app

    def main(self) -> None:
        while True:
            print("\n==== HOME MENU ====")
            print("1. COMPONENTS")
            print("2. CIRCUIT KITS")
            print("3. PURCHASE ORDERS")
            print("4. CUSTOMER SALES")
            print("5. TRANSACTION HISTORY")
            print("6. EXIT")

            choice = input("Please enter a number: ").strip()

            if choice == "1":
                self._components_menu()
            elif choice == "2":
                self._circuits_menu()
            elif choice == "3":
                self._purchase_orders_menu()
            elif choice == "4":
                self._customer_sales_menu()
            elif choice == "5":
                self._transactions_menu()
            elif choice == "6":
                print("Closing application...")
                return
            else:
                print("Invalid choice. Try again.")

    # ----- Submenus -----
    def _components_menu(self) -> None:
        while True:
            print("\n[COMPONENTS MENU]")
            print("1. Add Component")
            print("2. View Components")
            print("3. Back to Home")
            choice = input("Enter choice: ").strip()
            if choice == "1":
                self.app.add_sample_component()  # Example method in App
            elif choice == "2":
                self.app.view_components()
            elif choice == "3":
                return
            else:
                print("Invalid choice.")

    def _circuits_menu(self) -> None:
        while True:
            print("\n[CIRCUIT KITS MENU]")
            print("1. Create Light Circuit Kit")
            print("2. Create Sensor Circuit Kit")
            print("3. Back to Home")
            choice = input("Enter choice: ").strip()
            if choice == "1":
                print("Creating Light Circuit Kit...")
                # call app method here
            elif choice == "2":
                print("Creating Sensor Circuit Kit...")
                # call app method here
            elif choice == "3":
                return
            else:
                print("Invalid choice.")

    def _purchase_orders_menu(self) -> None:
        while True:
            print("\n[PURCHASE ORDERS MENU]")
            print("1. Create Purchase Order")
            print("2. View Purchase Orders")
            print("3. Back to Home")
            choice = input("Enter choice: ").strip()
            if choice == "1":
                print("Creating Purchase Order...")
                # call app method
            elif choice == "2":
                print("Viewing Purchase Orders...")
                # call app method
            elif choice == "3":
                return
            else:
                print("Invalid choice.")

    def _customer_sales_menu(self) -> None:
        while True:
            print("\n[CUSTOMER SALES MENU]")
            print("1. Create Customer Sale")
            print("2. View Customer Sales")
            print("3. Back to Home")
            choice = input("Enter choice: ").strip()
            if choice == "1":
                print("Creating Customer Sale...")
                # call app method
            elif choice == "2":
                print("Viewing Customer Sales...")
                # call app method
            elif choice == "3":
                return
            else:
                print("Invalid choice.")

    def _transactions_menu(self) -> None:
        while True:
            print("\n[TRANSACTION HISTORY MENU]")
            print("1. View All Transactions")
            print("2. Search Transactions by Date")
            print("3. Back to Home")
            choice = input("Enter choice: ").strip()
            if choice == "1":
                print("Showing all transactions...")
                # call app method
            elif choice == "2":
                print("Searching transactions by date...")
                # call app method
            elif choice == "3":
                return
            else:
                print("Invalid choice.")
