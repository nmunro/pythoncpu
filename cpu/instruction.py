class Instruction:
    def __init__(self, name, code):
        self.name = name
        self.code = code
        self.src = None
        self.dest = None

    def __call__(self, *args):
        return self

    def __index__(self):
        return int(self)

    def __int__(self):
        return self.code

    def __hex__(self):
        return hex(self)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Instruction{str(self)}: {hex(self)}>"


class InstructionMoveByte(Instruction):
    def __init__(self):
        super().__init__("Move.b", 0)

    def __call__(self, *args):
        self.src = args[0]
        self.dest = args[1]
        return self


class InstructionJmp(Instruction):
    def __init__(self):
        super().__init__("Jmp", 1)

    def __call__(self, *args):
        self.src = args[0]
        return self


class InstructionRtn(Instruction):
    def __init__(self):
        super().__init__("Rtn", 2)


class InstructionHalt(Instruction):
    def __init__(self):
        super().__init__("Halt", 3)


class InstructionSet:
    def __init__(self):
        print("Loading instruction set...")

        self.instructions = {
            "move.b": InstructionMoveByte(),
            "jmp": InstructionJmp(),
            "rtn": InstructionRtn(),
            "halt": InstructionHalt(),
        }

        print(f"Loaded {len(self)} instructions!")

    def __len__(self):
        return len(self.instructions)

    def __str__(self):
        return f"Instructions: {len(self)}"

    def __repr__(self):
        return f"<InstructionSet: {str(self)}>"

    def __getitem__(self, name):
        return self.instructions[name]
