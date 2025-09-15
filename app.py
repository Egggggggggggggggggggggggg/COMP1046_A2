from menu import Menu
from component.Wire import Wire
from circuitkit.LightCircuitKit import LightCircuitKit
from transaction.PurchaseOrder import PurchaseOrder

class App:
    def __init__(self):
        self.__components = []
        self.__circuits = []
        self.__transactions = []
        self.__menu = Menu("Main Menu", {
            1: ("Add Component", self.add_sample_component),
            2: ("View Components", self.view_components),
            3: ("Exit", self.exit_app)
        })
        self.__running = True

    def load_files(self):
        pass  # placeholder for CSV

    def save_files(self):
        pass  # placeholder for CSV

    def run(self):
        while self.__running:
            self.__menu.display()
            choice = self.__menu.get_choice()
            if choice is not None:
                action = self.__menu._Menu__options[choice][1]
                action()

    def add_sample_component(self):
        w = Wire(10.0, 2.5)
        self.__components.append(w)
        print("Added Wire: " + w.to_string())

    def view_components(self):
        if len(self.__components) == 0:
            print("No components available.")
        else:
            for c in self.__components:
                print(c.to_string())

    def exit_app(self):
        print("Exiting...")
        self.__running = False


if __name__ == "__main__":
    app = App()
    app.run()
