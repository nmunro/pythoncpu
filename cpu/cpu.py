import time
from pathlib import Path

from prettytable import PrettyTable

from constants import (
    DATA_REGISTER_PREFIX,
    ADDRESS_REGISTER_PREFIX,
    MEMORY_CELL_PREFIX,
    DECIMAL_NUMBER_PREFIX
)

from flags import Flags
from instructions import InstructionSet
from registers import Register
from stack import Stack


class CPU:
    def __init__(self, registers, clock, vram):
        self.data_registers = [Register(f"{DATA_REGISTER_PREFIX}{x}") for x in range(registers)]
        self.address_registers = [Register(f"{ADDRESS_REGISTER_PREFIX}{x}") for x in range(registers)]
        self.start = 0
        self.program_counter = 0
        self.clock = clock
        self.vram = vram
        self.stop = False
        self.flags = Flags("z", "n", "v", "c", "e")
        self.stack = Stack()
        self.instruction_set = InstructionSet()

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

    def increment_program_counter(self, instruction):
        self.program_counter += len(instruction)

    def set_program_counter(self, location):
        self.program_counter = int(location)

    def run(self):
        # Since the start memory location is determined, load it into the program counter
        # and begin the fetch/execute cycle
        self.program_counter = self.start

        while not self.stop:
            try:
                # This will need to read the PC and load an instruction from memory
                instruction = self.fetch_instruction()
                self.execute_instruction(instruction)
                time.sleep(self.clock.tick)

            except IndexError as e:
                print(e)
                self.halt()

        else:
            self.halt()

    def write_data_register(self, location, value):
        try:
            self.data_registers[int(location)].value = int(value)

        except ValueError:
            self.data_registers[int(location[1:])].value = int(value)

    def read_data_register(self, location):
        try:
            return self.data_registers[int(location)].value

        except ValueError:
            return self.data_registers[int(location[1:])].value

    def write_address_register(self, location_value):
        self.address_registers[int(location)].value = int(value)

    def read_address_register(self, location):
        return self.address_registers[int(location)].value

    def write_vram(self, location, value):
        if value.startswith(DECIMAL_NUMBER_PREFIX):
            self.vram.write(hex(int(location)), int(value[2:]))

    def read_vram(self, location):
        return self.vram.read(location)

    def fetch_instruction(self):
        return self.instruction_set[self.read_vram(self.program_counter)]

    def execute_instruction(self, instruction):
        if instruction == "move.b":
            instruction.src_type = str(self.read_vram(self.program_counter+1))
            instruction.src = str(self.read_vram(self.program_counter+2))
            instruction.dest_type = str(self.read_vram(self.program_counter+3))
            instruction.dest = str(self.read_vram(self.program_counter+4))

            if instruction.src.startswith(DATA_REGISTER_PREFIX):
                if instruction.dest.startswith(DATA_REGISTER_PREFIX):
                    self.flags.n = int(int(instruction.src[1:]) < 0)
                    self.flags.z = int(int(instruction.src[1:]) == 0)
                    self.flags.e = int(int(self.read_data_register(instruction.src)) == int(self.read_vram(instruction.dest[1:])))
                    self.write_data_register(instruction.dest, instruction.src[1:])

                elif instruction.dest.startswith(ADDRESS_REGISTER_PREFIX):
                    pass

                elif instruction.dest.startswith(MEMORY_CELL_PREFIX):
                    pass

            elif instruction.src.startswith(ADDRESS_REGISTER_PREFIX):
                pass

            else:
                if instruction.dest.startswith(DATA_REGISTER_PREFIX):
                    self.flags.n = int(int(instruction.src[1:]) < 0)
                    self.flags.z = int(int(instruction.src[1:]) == 0)
                    self.flags.e = int(int(instruction.src) == int(self.read_data_register(instruction.dest)))
                    self.write_data_register(instruction.dest, instruction.src)

                elif instruction.dest.startswith(ADDRESS_REGISTER_PREFIX):
                    pass

                elif instruction.dest.startswith(MEMORY_CELL_PREFIX):
                    pass

            # These flags are cleared irrespective of what happens in a move
            self.flags.v = 0
            self.flags.c = 0

            # Move program counter forward
            self.increment_program_counter(instruction)

        elif instruction == "halt":
            # Set the global stop to the fetch/execute cycle can halt
            self.stop = True

        elif instruction == "noop":
            self.increment_program_counter(instruction)
            self.flags.clear()

        elif instruction == "jmp":
            instruction.dest_type = str(self.read_vram(self.program_counter+1))
            instruction.dest = str(self.read_vram(self.program_counter+2))
            self.set_program_counter(instruction.dest)

        elif instruction == "jnz":
            if not self.flags.z == 0:
                instruction.dest_type = str(self.read_vram(self.program_counter+1))
                instruction.dest = str(self.read_vram(self.program_counter+2))
                self.set_program_counter(instruction.dest)

            else:
                self.increment_program_counter(instruction)

        elif instruction == "jng":
            if self.flags.n < 0:
                instruction.dest_type = str(self.read_vram(self.program_counter+1))
                instruction.dest = str(self.read_vram(self.program_counter+2))
                self.set_program_counter(instruction.dest)

            else:
                self.increment_program_counter(instruction)

        elif instruction == "jeq":
            if self.flags.e == 1:
                instruction.dest_type = str(self.read_vram(self.program_counter+1))
                instruction.dest = str(self.read_vram(self.program_counter+2))
                self.set_program_counter(instruction.dest)

            else:
                self.increment_program_counter(instruction)

        elif instruction == "jne":
            if self.flags.e == 0:
                instruction.dest_type = str(self.read_vram(self.program_counter+1))
                instruction.dest = str(self.read_vram(self.program_counter+2))
                self.set_program_counter(instruction.dest)

            else:
                self.increment_program_counter(instruction)

        elif instruction == "cmp.b":
            instruction.src_type = str(self.read_vram(self.program_counter+1))
            instruction.src = str(self.read_vram(self.program_counter+2))
            instruction.dest_type = str(self.read_vram(self.program_counter+3))
            instruction.dest = str(self.read_vram(self.program_counter+4))
            result = 0

            # If dealing with src data registers
            if instruction.src.startswith(DATA_REGISTER_PREFIX):
                if instruction.dest.startswith(DATA_REGISTER_PREFIX):
                    result = self.read_data_register(instruction.dest) - self.read_data_register(instruction.src)
                    self.flags.e = int(self.read_data_register(instruction.dest) == self.read_data_register(instruction.src))

                elif instruction.dest.startswith(ADDRESS_REGISTER_PREFIX):
                    result = self.read_address_register(instruction.dest[1:]) - self.read_data_register(instruction.src)
                    self.flags.e = int(self.read_address_register(instruction.dest[1:]) == self.read_data_register(instruction.src))

                else:
                    result = int(instruction.dest) - self.read_data_register(instruction.src)

            # If dealing with src address registers
            elif instruction.src.startswith(ADDRESS_REGISTER_PREFIX):
                if instruction.dest.startswith(DATA_REGISTER_PREFIX):
                    result = self.read_data_register(instruction.dest) - self.read_address_register(instruction.src[1:])
                    self.flags.e = int(self.read_data_register(instruction.dest) == self.read_data_register(instruction.src))

                elif instruction.dest.startswith(ADDRESS_REGISTER_PREFIX):
                    result = self.read_address_register(instruction.dest[1:]) - self.read_address_register(instruction.src[1:])
                    self.flags.e = int(self.read_data_register(instruction.dest) == self.read_data_register(instruction.src))

                else:
                    result = int(instruction.dest) - self.read_address_register(instruction.src[1:])

            # If dealing with src being a number
            else:
                if instruction.dest.startswith(DATA_REGISTER_PREFIX):
                    result = int(int(self.read_data_register(instruction.dest)) - int(instruction.src))
                    self.flags.e = int(int(self.read_data_register(instruction.dest)) == int(instruction.src))

                elif instruction.dest.startswith(ADDRESS_REGISTER_PREFIX):
                    pass

                else:
                    result = int(instruction.dest) - int(instruction.src)
                    self.flags.e = int(int(instruction.dest) == int(instruction.src))

            # set ccr flags
            self.flags.n = int(result < 0)
            self.flags.z = int(result == 0)
            self.flags.v = 0
            self.flags.c = 0

            # Increment program counter
            self.increment_program_counter(instruction)

        elif instruction == "add.b":
            instruction.src_type = str(self.read_vram(self.program_counter+1))
            instruction.src = str(self.read_vram(self.program_counter+2))
            instruction.dest_type = str(self.read_vram(self.program_counter+3))
            instruction.dest = str(self.read_vram(self.program_counter+4))

            if instruction.src.startswith(DATA_REGISTER_PREFIX):
                if instruction.dest.startswith(DATA_REGISTER_PREFIX):
                    total = int(instruction.src) + self.read_data_register(instruction.dest)
                    self.flags.n = int(total < 0)
                    self.flags.z = int(total == 0)
                    self.flags.e = int(int(self.read_vram(instruction.src)) == int(self.read_vram(instruction.dest)))
                    self.write_data_register(instruction.dest, total)

                elif instruction.dest.startswith(ADDRESS_REGISTER_PREFIX):
                    pass

                elif instruction.dest.startswith(MEMORY_CELL_PREFIX):
                    pass

            elif instruction.src.startswith(ADDRESS_REGISTER_PREFIX):
                pass

            else:
                if instruction.dest.startswith(DATA_REGISTER_PREFIX):
                    total = int(instruction.src) + self.read_data_register(instruction.dest)
                    self.flags.n = int(total < 0)
                    self.flags.z = int(total == 0)
                    self.flags.e = int(int(instruction.src) == int(self.read_data_register(instruction.dest)))
                    self.write_data_register(instruction.dest, total)

                elif instruction.dest.startswith(ADDRESS_REGISTER_PREFIX):
                    pass

                elif instruction.dest.startswith(MEMORY_CELL_PREFIX):
                    pass

            self.flags.v = 0
            self.flags.c = 0

            # Move program counter forward
            self.increment_program_counter(instruction)

        elif instruction == "inc":
            instruction.dest_type = str(self.read_vram(self.program_counter+1))
            instruction.dest = str(self.read_vram(self.program_counter+2))

            # Data register
            if instruction.dest.startswith(DATA_REGISTER_PREFIX):
                origin = self.read_data_register(instruction.dest)
                self.write_data_register(instruction.dest, origin+1)

            # Address register
            elif instruction.dest.startswith(DATA_REGISTER_PREFIX):
                origin = self.read_address_register(instruction.dest)
                self.write_address_register(instruction.dest, origin+1)

            # Numbers, doesn't do anything except change CCRs
            else:
                origin = instruction.dest

            self.flags.z = int(int(origin+1) == 0)
            self.flags.e = int(origin == origin+1)
            self.flags.n = int(int(origin+1) < 0)

            self.increment_program_counter(instruction)

        elif instruction == "sub.b":
            instruction.src_type = str(self.read_vram(self.program_counter+1))
            instruction.src = str(self.read_vram(self.program_counter+2))
            instruction.dest_type = str(self.read_vram(self.program_counter+3))
            instruction.dest = str(self.read_vram(self.program_counter+4))

            if instruction.src.startswith(DATA_REGISTER_PREFIX) and instruction.dest.startswith(DATA_REGISTER_PREFIX):
                total = self.read_data_register(instruction.dest) - int(instruction.src)
                self.flags.n = int(total < 0)
                self.flags.z = int(total == 0)
                self.flags.e = int(int(self.read_vram(instruction.src)) == int(self.read_vram(instruction.dest)))
                self.write_data_register(instruction.dest, total)

            elif instruction.src.startswith(DATA_REGISTER_PREFIX) and instruction.dest.startswith(ADDRESS_REGISTER_PREFIX):
                pass

            elif instruction.src.startswith(DATA_REGISTER_PREFIX) and instruction.dest.startswith(MEMORY_CELL_PREFIX):
                pass

            elif instruction.src.startswith(ADDRESS_REGISTER_PREFIX):
                pass

            else:
                if instruction.dest.startswith(DATA_REGISTER_PREFIX):
                    total = self.read_data_register(instruction.dest) - int(instruction.src)
                    self.flags.n = int(total < 0)
                    self.flags.z = int(total == 0)
                    self.flags.e = int(int(instruction.src) == int(self.read_data_register(instruction.dest)))
                    self.write_data_register(instruction.dest, total)

                elif instruction.dest.startswith(ADDRESS_REGISTER_PREFIX):
                    pass

                elif instruction.dest.startswith(MEMORY_CELL_PREFIX):
                    pass

            self.flags.v = 0
            self.flags.c = 0

            # Move program counter forward
            self.increment_program_counter(instruction)

        elif instruction == "dec":
            instruction.dest_type = str(self.read_vram(self.program_counter+1))
            instruction.dest = str(self.read_vram(self.program_counter+2))

            # Data register
            if instruction.dest.startswith(DATA_REGISTER_PREFIX):
                origin = self.read_data_register(instruction.dest)
                self.write_data_register(instruction.dest, origin-1)

            # Address register
            elif instruction.dest.startswith(DATA_REGISTER_PREFIX):
                origin = self.read_address_register(instruction.dest)
                self.write_address_register(instruction.dest, origin-1)

            # Numbers, doesn't do anything except change CCRs
            else:
                origin = instruction.dest

            self.flags.z = int(int(origin+1) == 0)
            self.flags.e = int(origin == origin-1)
            self.flags.n = int(int(origin+1) < 0)

            self.increment_progrqam_counter(len(instruction))

        elif instruction == "mul.b":
            instruction.src_type = str(self.read_vram(self.program_counter+1))
            instruction.src = str(self.read_vram(self.program_counter+2))
            instruction.dest_type = str(self.read_vram(self.program_counter+3))
            instruction.dest = str(self.read_vram(self.program_counter+4))

            if instruction.src.startswith(DATA_REGISTER_PREFIX) and instruction.dest.startswith(DATA_REGISTER_PREFIX):
                total = self.read_data_register(instruction.dest) * int(instruction.src)
                self.flags.n = int(int(instruction.src) < 0)
                self.flags.z = int(int(instruction.src) == 0)
                self.flags.e = int(int(self.read_vram(instruction.src)) == int(self.read_vram(instruction.dest)))
                self.write_data_register(instruction.dest, total)

            elif instruction.src.startswith(DATA_REGISTER_PREFIX) and instruction.dest.startswith(ADDRESS_REGISTER_PREFIX):
                pass

            elif instruction.src.startswith(DATA_REGISTER_PREFIX) and instruction.dest.startswith(MEMORY_CELL_PREFIX):
                pass

            elif instruction.src.startswith(ADDRESS_REGISTER_PREFIX):
                pass

            else:
                if instruction.dest.startswith(DATA_REGISTER_PREFIX):
                    total = self.read_data_register(instruction.dest) * int(instruction.src)
                    self.flags.n = int(int(instruction.src) < 0)
                    self.flags.z = int(int(instruction.src) == 0)
                    self.flags.e = int(self.read_data_register(instruction.dest) == self.read_data_register(instruction.src))
                    self.write_data_register(instruction.dest, total)

                elif instruction.dest.startswith(ADDRESS_REGISTER_PREFIX):
                    pass

                elif instruction.dest.startswith(MEMORY_CELL_PREFIX):
                    pass

            self.flags.v = 0
            self.flags.c = 0

            # Move program counter forward
            self.increment_program_counter(instruction)

        elif instruction == "div.b":
            instruction.src_type = str(self.read_vram(self.program_counter+1))
            instruction.src = str(self.read_vram(self.program_counter+2))
            instruction.dest_type = str(self.read_vram(self.program_counter+3))
            instruction.dest = str(self.read_vram(self.program_counter+4))

            if instruction.src.startswith(DATA_REGISTER_PREFIX) and instruction.dest.startswith(DATA_REGISTER_PREFIX):
                total = self.read_data_register(instruction.dest) / int(instruction.src)
                self.flags.n = int(int(instruction.src) < 0)
                self.flags.z = int(int(instruction.src) == 0)
                self.flags.e = int(int(self.read_vram(instruction.src)) == int(self.read_vram(instruction.dest)))
                self.write_data_register(instruction.dest, total)

            elif instruction.src.startswith(DATA_REGISTER_PREFIX) and instruction.dest.startswith(ADDRESS_REGISTER_PREFIX):
                pass

            elif instruction.src.startswith(DATA_REGISTER_PREFIX) and instruction.dest.startswith(MEMORY_CELL_PREFIX):
                pass

            elif instruction.src.startswith(ADDRESS_REGISTER_PREFIX):
                pass

            else:
                if instruction.dest.startswith(DATA_REGISTER_PREFIX):
                    total = self.read_data_register(instruction.dest) / int(instruction.src)
                    self.flags.n = int(int(instruction.src) < 0)
                    self.flags.z = int(int(instruction.src) == 0)
                    self.flags.e = int(self.read_data_register(instruction.dest) == self.read_data_register(instruction.src))
                    self.write_data_register(instruction.dest, total)

                elif instruction.dest.startswith(ADDRESS_REGISTER_PREFIX):
                    pass

                elif instruction.dest.startswith(MEMORY_CELL_PREFIX):
                    pass

            self.flags.v = 0
            self.flags.c = 0

            # Move program counter forward
            self.increment_program_counter(instruction)

        else:
            exit(f"Runtime error: Unrecognised operand '{instruction.name}'")


    def halt(self):
        self.stop = True
        print("Halting and displaying machine state.")
        self.show()
        self.vram.show()
        self.flags.show()
        exit()

    def show(self):
        table = PrettyTable()
        table.field_names = ["Data Register", "Data Value", "Address Register", "Address Value"]
        for num in range(len(self.data_registers)):
            table.add_row([
                self.data_registers[num].name,
                self.data_registers[num].value,
                self.address_registers[num].name,
                self.address_registers[num].value,
            ])
        print(table)

    def __str__(self):
        return f"Clock {str(self.clock)} | Registers: {len(self.data_registers) * 2}"

    def __repr__(self):
        return f"<CPU: {str(self)}>"
