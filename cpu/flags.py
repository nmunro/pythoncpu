from prettytable import PrettyTable


class Flags:
    def __init__(self, *args):
        self.flags = []

        for arg in args:
            self.flags.append(arg)
            setattr(self, arg, 0)

    def clear(self):
        for flag in self.flags:
            setattr(self, flag, 0)

    def show(self):
        table = PrettyTable()
        table.field_names = ["Flag", "Value"]
        table.add_row(["Negative", self.n])
        table.add_row(["Zero", self.z])
        table.add_row(["Carry", self.c])
        table.add_row(["Overflow", self.v])
        table.add_row(["Equal", self.e])
        print(table)
