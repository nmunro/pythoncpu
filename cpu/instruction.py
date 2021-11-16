from enum import Enum

class Length(Enum):
    byte = 1 # 1 byte
    word = 2 # 2 bytes
    long = 4 # 4 bytes

class Instruction:
    def __init__(self, name, code):
        self.name = name.lower()
        self.code = f"{code}".zfill(2)
        self.operands = 1
        self.length = Length.byte

    def __len__(self):
        return self.operands

    def __index__(self):
        return int(self)

    def __int__(self):
        return self.code

    def __hex__(self):
        return hex(self)

    def __eq__(self, other):
        if not type(other) == str:
            raise TypeError("Must be a string")

        return self.name == other

    def __str__(self):
        return f"{str(hex(int(self.code)))[2:].zfill(2)}"

    def __repr__(self):
        return f"<Instruction (self.name): {hex(self)}>"


class InstructionNoOp(Instruction):
    def __init__(self):
        super().__init__("noop", 0)


class InstructionMoveByte(Instruction):
    def __init__(self):
        super().__init__("move.b", 1)
        self.src = ""
        self.dest = ""
        self.operands = 3

    def __str__(self):
        return f"{str(hex(int(self.code)))[2:].zfill(2)}{self.src.zfill(2)}{self.dest.zfill(2)}"


class InstructionJmp(Instruction):
    def __init__(self):
        super().__init__("jmp", 2)
        self.label = ""
        self.operands = 2

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, label):
        self._label = f"{label}".zfill(2)

    def __str__(self):
        return f"{str(hex(int(self.code)))[2:].zfill(2)}{self.label}"


class InstructionHalt(Instruction):
    def __init__(self):
        super().__init__("halt", 4)

    def __str__(self):
        return f"{str(hex(int(self.code)))[2:].zfill(2)}"


class InstructionDef(Instruction):
    def __init__(self):
        super().__init__("def", 5)
        self._label = ""
        self.operands = 2

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, label):
        self._label = f"{label}".zfill(2)

    def __str__(self):
        return f"{str(hex(int(self.code)))[2:].zfill(2)}{self.label}"


class InstructionSet:
    def __init__(self):
        self.instructions = {
            "noop": InstructionNoOp(),
            "00": InstructionNoOp(),

            "move.b": InstructionMoveByte(),
            "01": InstructionMoveByte(),

            "jmp": InstructionJmp(),
            "02": InstructionJmp(),

            "halt": InstructionHalt(),
            "04": InstructionHalt(),

            "def": InstructionDef(),
            "05": InstructionDef(),
        }

    def __len__(self):
        return len(self.instructions)

    def __str__(self):
        return f"Instructions: {len(self)}"

    def __repr__(self):
        return f"<InstructionSet: {str(self)}>"

    def __getitem__(self, name):
        return self.instructions[name]
