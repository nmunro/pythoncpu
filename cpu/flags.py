from prettytable import PrettyTable


class Flags:
    def __init__(self, *args):
        for arg in args:
            setattr(self, arg, 0)

    def set(self, flag, value):
        setattr(self, flag, value)

    def get(self, flag):
        getattr(self, flag)

    def clear(self, flag):
        self.set(flag, 0)

    def show(self):
        table = PrettyTable()
        table.field_names = ["Flag", "Value"]
        table.add_row(["Negative", self.n])
        table.add_row(["Zero", self.z])
        table.add_row(["Carry", self.c])
        table.add_row(["Overflow", self.v])
        print(table)
