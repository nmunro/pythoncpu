import math

from prettytable import PrettyTable


class Cell:
    def __init__(self, offset, address):
        self.offset = offset
        self.address = address
        self.value = 0

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f"<Cell: {self.offset}:{self.address}: {str(self)}>"


class VRAM:
    BASE_SIZE = 16
    KB_SIZE = 1024
    MB_SIZE = 1024000

    def __init__(self, size=16):
        self.size = size
        self.cells = [[Cell(offset, address) for address in range(self.BASE_SIZE)] for offset in range(self.size)]

    def write(self, cell, data):
        if type(cell) == int:
            cell = hex(cell)

        offset = math.trunc(int(cell, self.BASE_SIZE) / self.BASE_SIZE)
        address = int(cell, self.BASE_SIZE) % self.BASE_SIZE
        self.write_byte(offset, address, data)

    def write_byte(self, offset, address, data):
        self.cells[offset][address].value = data

    def write_bytes(self, offset, address, data):
        print(data)

    def read(self, cell):
        if type(cell) == int:
            cell = hex(cell)

        offset = math.trunc(int(cell, self.BASE_SIZE) / self.BASE_SIZE)
        address = int(cell, self.BASE_SIZE) % self.BASE_SIZE
        return self.read_byte(offset, address)

    def read_byte(self, offset, address):
        return self.cells[offset][address].value

    def show(self):
        table = PrettyTable()
        table.field_names = ["Offset", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]

        for num, offset in enumerate(self.cells):
            table.add_row([f"0x{str(num).ljust(2, '0')}", *offset])

        print(table)

    def offset(self, number):
        return self.cells[number]

    def __len__(self):
        return self.size * self.BASE_SIZE

    def __str__(self):
        if len(self) >= self.MB_SIZE:
            return f"Memory: {math.floor(len(self) / 1000000)} megabyte(s)"

        elif len(self) >= self.KB_SIZE:
            return f"Memory: {math.floor(len(self) / 1000)} kilobyte(s)"

        else:
            return f"Memory: {len(self)} byte(s)"

    def __repr__(self):
        return "<VRAM: {str(self)}>"
