import time
from pathlib import Path

from prettytable import PrettyTable

from flags import Flags
from instructions import InstructionSet
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
        self.start = 0
        self.program_counter = 0
        self.clock = clock
        self.vram = vram
        self.stop = False
        self.flags = Flags("z", "n", "v", "c")
        self.stack = Stack()
        self.instruction_set = InstructionSet()

        # Needed prefixs
        self.MEMORY_CELL_PREFIX = "0x"
        self.REGISTER_PREFIX = "d"

        # Data types
        self.DECIMAL_NUMBER_PREFIX = "#$"

    def load_code(self, program_name):
        with Path(program_name).open() as f:
            code = [line.strip() for line in f.readlines()]
            start = 0
            length = 0
            start_tracking = False
            instructions = []

            for num, line in enumerate(code):
                if start_tracking:
                    instructions.append(line)

                elif line.startswith("START:"):
                    start = code[num].split(" ")[1]

                elif line.startswith("LENGTH:"):
                    length = code[num].split(" ")[1]

                elif line.startswith(".CODE"):
                    start_tracking = True

            return int(start), length, instructions

    def boot(self, program_name: str) -> None:
        instructions = []
        start, length, instructions = self.load_code(program_name)
        num = 0

        for a, seq in enumerate(instructions, 1):
            for n, x in enumerate([x for x in range(0, len(seq), 2)]):
                self.vram.write(num, seq[x:x+2])
                num += 1
                time.sleep(self.clock.tick)
                print("\r", f"Loading instruction: {str(a).zfill(len(str(length)))}/{length}...", end="")

        print("\r", f"Loading instruction {length}/{length}... Done!")
        self.start = start

    def increment_program_counter(self):
        self.program_counter += 1

    def set_program_counter(self, location):
        self.program_counter = int(location)

    def run(self):
        # Since the start memory location is determined, load it into the program counter
        # and begin the fetch/execute cycle
        self.program_counter = self.start

        while not self.stop:
            try:
                # This will need to read the PC and load an instruction from memory
                self.execute_instruction(self.fetch_instruction())
                time.sleep(self.clock.tick)

            except IndexError as e:
                print(e)
                self.halt()

        else:
            self.halt()

    def write_register(self, location, value):
        self.registers[int(location)].value = int(value)

    def read_register(self, location):
        return self.registers[int(location)].value

    def write_vram(self, location, value):
        if value.startswith(self.DECIMAL_NUMBER_PREFIX):
            self.vram.write(hex(int(location)), int(value[2:]))

    def read_vram(self, location):
        return self.vram.read(location)

    def fetch_instruction(self):
        return self.instruction_set[self.read_vram(self.program_counter)]

    def execute_instruction(self, instruction):
        if instruction == "move.b":
            instruction.src = str(self.read_vram(self.program_counter+1))
            instruction.dest = str(self.read_vram(self.program_counter+2))

            if instruction.dest.startswith(self.MEMORY_CELL_PREFIX):
                self.write_vram(instruction.dest[2:], instruction.src)
                self.flags.set("n", int(self.read_vram(instruction.dest[2:]) < 0))
                self.flags.set("z", int(self.read_vram(instruction.dest[2:]) == 0))

            elif instruction.dest.startswith(self.REGISTER_PREFIX):
                self.write_register(instruction.dest[1:], instruction.src)
                self.flags.set("n", int(self.read_register(instruction.dest[1:]) < 0))
                self.flags.set("z", int(self.read_register(instruction.dest[1:]) == 0))

            # These flags are cleared irrespective of what happens in a move
            self.flags.clear("v")
            self.flags.clear("c")

            # Move program counter forward
            for args in range(len(instruction)):
                self.increment_program_counter()

        elif instruction == "halt":
            # Set the global stop to the fetch/execute cycle can halt
            self.stop = True

        elif instruction == "define":
            instruction.label = str(self.read_vram(self.program_counter+1))

            for args in range(len(instruction)):
                self.increment_program_counter()

        elif instruction == "noop":
            for args in range(len(instruction)):
                self.increment_program_counter()

        elif instruction == "jmp":
            instruction.label = str(self.read_vram(self.program_counter+1))
            self.set_program_counter(instruction.label)

    def halt(self):
        self.stop = True
        print("Halting and displaying machine state.")
        self.show()
        self.vram.show()
        self.flags.show()
        exit()

    def show(self):
        table = PrettyTable()
        table.field_names = ["Register", "Value"]
        [table.add_row([f"{register.name}", register.value]) for register in self.registers]
        print(table)

    def __str__(self):
        return f"Clock {str(self.clock)} | Registers: {len(self.registers)}"

    def __repr__(self):
        return f"<CPU: {str(self)}>"
