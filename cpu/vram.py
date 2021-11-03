import math

from prettytable import PrettyTable


class Cell:
    def __init__(self, col, row):
        self.col = col
        self.row = row
        self.value = 0

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f"<Cell [{self.row}:{self.col}: {str(self)}>"


class VRAM:
    BASE_SIZE = 16

    def __init__(self, size=16):
        self.size = size
        self.cells = [[Cell(col, row) for col in range(16)] for row in range(self.size)]

    def write(self, cell, data):
        row = math.trunc(int(cell, self.BASE_SIZE) / self.BASE_SIZE)
        col = int(cell, self.BASE_SIZE) % self.BASE_SIZE
        self.cells[row][col].value = data

    def read(self, cell):
        row = math.trunc(int(cell, self.BASE_SIZE) / self.BASE_SIZE)
        col = int(cell, self.BASE_SIZE) % self.BASE_SIZE
        return hex(self.cells[row][col].value)

    def __len__(self):
        return self.size * self.BASE_SIZE

    def show(self):
        table = PrettyTable()
        table.field_names = ["Address", "Value"]

        for row in self.cells:
            for col in row:
                table.add_row([f"0x{col.row}{col.col}".ljust(6, " "), col.value])

        print(table)

    def __str__(self):
        if len(self) >= 1024000:
            return f"Memory: {math.floor(len(self) / 1000000)} megabyte(s)"

        elif len(self) >= 1000:
            return f"Memory: {math.floor(len(self) / 1000)} kilobyte(s)"

        else:
            return f"Memory: {len(self)} byte(s)"

    def __repr__(self):
        return "<VRAM: {str(self)}>"
