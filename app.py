from menu import Menu

class App:
    def __init__(self) -> None:
        self.components = []
        self.circuits = []
        self.transactions = []

    def run(self) -> None:
        Menu(self).main()

if __name__ == "__main__":
    App().run()
