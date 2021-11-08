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
        self.functions = {}
        self.instruction_set = InstructionSet()

    def boot(self, program_name: str) -> None:
        print(f"Loading program {program_name} into lower memory...")

        functions = []

        with Path(program_name).open() as f:
            byte_sequence = []

            for num, line in enumerate([line.strip() for line in f.readlines() if not line.strip() == "" and not line.strip().startswith(";")]):
                # Remember to find comments elsewhere in a line (not the beginning) and grab everything before the ";" character, attempt to use that as an instruction
                instruction = line.split(" ", 1)
                parsed_instruction = None

                # If this line defines a function
                if instruction[0].endswith(":"):
                    parsed_instruction, args = self.read_instruction(instruction[1])
                    parsed_instruction(*args)
                    byte_sequence.append("##")
                    functions.append(instruction[0][:-1])

                else:
                    parsed_instruction, args = self.read_instruction(" ".join(instruction))
                    parsed_instruction(*args)

                if parsed_instruction == "move.b":
                    byte_sequence.append(str(parsed_instruction))

                elif parsed_instruction == "halt":
                    byte_sequence.append(str(parsed_instruction))

                elif parsed_instruction == "rtn":
                    byte_sequence.append(str(parsed_instruction))

        byte_sequence = "".join(byte_sequence)

        fn_offset = 0
        fn_count = 0

        for num, x in enumerate([x for x in range(0, len(byte_sequence), 2)]):
            if byte_sequence[x:x+2] == "##":
                self.functions[functions[fn_count]] = fn_offset
                fn_count += 1

            else:
                fn_offset += 1

        byte_sequence = byte_sequence.replace("##", "")

        for num, x in enumerate([x for x in range(0, len(byte_sequence), 2)]):
            self.vram.write(num, byte_sequence[x:x+2])

        print("Done!")

    def increment_program_counter(self):
        self.program_counter += 1

    def set_program_counter(self, location):
        self.program_counter = location

    def run(self):
        # Find the "start:" function and set the program counter to that!
        self.program_counter = self.functions["start"]
        print(f"Program Counter: {self.program_counter}")

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
        if value.startswith("#$"):
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
        return self.instruction_set[self.read_vram(self.program_counter)]

    def execute_instruction(self, instruction):
        if instruction == "move.b":
            instruction.src = str(self.read_vram(self.program_counter+1))
            instruction.dest = str(self.read_vram(self.program_counter+2))

            if instruction.dest.startswith("0x"):
                self.write_vram(instruction.dest[2:], instruction.src)

            elif instruction.dest.startswith("d"):
                self.write_register(instruction.dest[1:], instruction.src)

            for ticks in range(len(instruction)):
                self.increment_program_counter()

        elif instruction == "halt":
            self.stop = True

        elif instruction == "jmp":
            print("not implemented")

        elif instruction == "rtn":
            print("not implemented")


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
