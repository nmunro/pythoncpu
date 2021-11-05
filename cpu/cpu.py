import time
from pathlib import Path

from prettytable import PrettyTable

from instruction import InstructionSet
from stack import Stack


class Register:
    def __init__(self, name):
        self.name = name
        self.value = 0

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f"<Register: {str(self)}>"


class CPU:
    def __init__(self, registers, clock, vram):
        self.registers = [Register(x) for x in range(registers)]
        self.program_counter = 0
        self.clock = clock
        self.vram = vram
        self.stop = False
        self.z = 0  # zero flag, if the result of some operation was zero
        self.n = 0  # negative flag, if the result of some operation was a negative number
        self.v = 0  # overflow flag, when a value to0 large to store in a register was attempted
        self.c = 0  # carry flag, when a value is too large to store in a register the "carry" can be flagged
        self.program_name = ""
        self.program = []
        self.stack = Stack()
        self.functions = {}
        self.instruction_set = InstructionSet()

    def load_program(self, instruction):
        self.program.append(instruction)

    def boot(self, program_name):
        self.program_name = program_name
        print("Booting...")

        with Path(self.program_name).open() as f:
            for num, line in enumerate([line.strip() for line in f.readlines() if not line.strip() == ""]):
                instruction = line.split(" ", 1)

                if instruction[0].endswith(":"): # If this line is a function
                    self.functions[instruction[0][:-1]] = num
                    self.load_program(instruction[1])

                else:
                    self.load_program(" ".join(instruction))

    def increment_program_counter(self):
        self.program_counter += 1

    def set_program_counter(self, location):
        self.program_counter = location

    def run(self):
        print(f"\nBegin execution of: {self.program_name}\n")
                
        # Find the "start:" function and set the program counter to that!
        self.program_counter = self.functions["start"]

        while self.program and not self.stop:
            try:
                instruction, args = self.fetch_instruction(self.program[self.program_counter])
                self.execute_instruction(instruction, args)
                self.increment_program_counter()
                time.sleep(self.clock.tick)

            except IndexError:
                self.halt()

        else:
            self.halt()

    def write_register(self, value, location):
        if value.startswith("#$"):
            self.registers[int(location)].value = int(value[2:])

    def write_vram(self, value, location):
        if value.startswith("#$"):
            self.vram.write(hex(int(location)), int(value[2:]))

    def fetch_instruction(self, instruction):
        # remove label, if present
        match instruction.split(" "):
            case[instruction, args]:
                return self.instruction_set[instruction], args.split(",")

            case[instruction]:
                return self.instruction_set[instruction], [""]

    def execute_instruction(self, instruction, args):
        if str(instruction) == "move.b":
            instruction(*args)

            if instruction.dest.startswith("0x"):
                self.write_vram(instruction.src, instruction.dest[2:])

            elif instruction.dest.startswith("rx"):
                self.write_register(instruction.src, instruction.dest[2:])

        elif instruction.name == "halt":
            self.stop = True

    def halt(self):
        self.stop = True
        print("Halting!")
        self.show()
        self.vram.show()
        exit()

    def show(self):
        table = PrettyTable()
        table.field_names = ["Register", "Value"]

        for register in self.registers:
            table.add_row([f"{register.name}", register.value])

        print(table)

    def __str__(self):
        return f"Clock {str(self.clock)} | Registers: {len(self.registers)}"

    def __repr__(self):
        return f"<CPU: {str(self)}>"
