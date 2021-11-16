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
        self.program = []
        self.stack = Stack()
        self.labels = {}
        self.instruction_set = InstructionSet()

        # Needed prefixs
        self.MEMORY_CELL_PREFIX = "0x"
        self.REGISTER_PREFIX = "d"

        # Data types
        self.DECIMAL_NUMBER_PREFIX = "#$"

    def read_lines(self, lines):
        return [line.strip() for line in lines if not line.strip() == "" and not line.strip().startswith(";")]

    def load_code(self, program_name):
        with Path(program_name).open() as f:
            return self.read_lines(f.readlines())

    def boot(self, program_name: str) -> None:
        print(f"Loading program {program_name} into lower memory...")

        labels = {}
        instructions = []
        fn_offset = 0
        code = self.load_code(program_name)

        # First pass to find labels
        offset = 0

        for num, instruction in enumerate(code):
            parsed_instruction, args = self.read_instruction(instruction)
            offset += parsed_instruction.operands * parsed_instruction.length.value

            if parsed_instruction == "def":
                labels[args[0]] = offset
                parsed_instruction.label = labels[args[0]]

        # Second pass parsing
        for num, instruction in enumerate(code):
            # Remember to find comments elsewhere in a line (not the beginning) and grab everything before the ";" character, attempt to use that as an instruction
            parsed_instruction, args = self.read_instruction(instruction)

            # If this line defines a label
            if parsed_instruction == "def":
                labels[args[0]] = fn_offset
                parsed_instruction.label = labels[args[0]]
                instructions.append(str(parsed_instruction))

            elif parsed_instruction == "move.b":
                parsed_instruction.src = args[0][2:]
                parsed_instruction.dest = args[1]
                instructions.append(str(parsed_instruction))

            elif parsed_instruction == "halt":
                instructions.append(str(parsed_instruction))

            elif parsed_instruction == "noop":
                instructions.append(str(parsed_instruction))

            elif parsed_instruction == "jmp":
                parsed_instruction.label = labels[args[0]];
                instructions.append(str(parsed_instruction))

            # Update label offset
            fn_offset += len(parsed_instruction)

        self.labels = labels

        num = 0
        for seq in instructions:
            for n, x in enumerate([x for x in range(0, len(seq), 2)]):
                self.vram.write(num, seq[x:x+2])
                num += 1

        print("Done!")

    def increment_program_counter(self):
        self.program_counter += 1

    def set_program_counter(self, location):
        self.program_counter = int(location)

    def run(self):
        # Find the "start:" function and set the program counter to that, offset it by two (for the def and start)!
        self.program_counter = self.labels["start"]

        while not self.stop:
            try:
                # This will need to read the PC and load an instruction from memory not from self.program
                instruction = self.fetch_instruction()
                self.execute_instruction(instruction)
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

    def read_instruction(self, instruction):
        match instruction.split(" "):
            case[instruction, args]:
                return self.instruction_set[instruction], args.split(",")

            case[instruction]:
                return self.instruction_set[instruction], [""]

    def fetch_instruction(self):
        try:
            return self.instruction_set[self.read_vram(self.program_counter)]

        except KeyError as e:
            self.vram.show()

    def execute_instruction(self, instruction):
        if instruction == "move.b":
            instruction.src = str(self.read_vram(self.program_counter+1))
            instruction.dest = str(self.read_vram(self.program_counter+2))

            if instruction.dest.startswith(self.MEMORY_CELL_PREFIX):
                self.write_vram(instruction.dest[2:], instruction.src)

            elif instruction.dest.startswith(self.REGISTER_PREFIX):
                self.write_register(instruction.dest[1:], instruction.src)

            for args in range(len(instruction)):
                self.increment_program_counter()

        elif instruction == "halt":
            self.stop = True

        elif instruction == "def":
            instruction.label = str(self.read_vram(self.program_counter+1))

            for args in range(len(instruction)):
                self.increment_program_counter()

        elif instruction == "noop":
            pass

        elif instruction == "jmp":
            instruction.label = str(self.read_vram(self.program_counter+1))
            self.set_program_counter(instruction.label)

    def halt(self):
        self.stop = True
        print("Halting!")
        self.show()
        self.vram.show()
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
