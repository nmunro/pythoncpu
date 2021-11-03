class Instruction:
    def __init__(self, name):
        self.name = name
        self.src = None
        self.dest = None

    def __call__(self, *args):
        return self

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Instruction: {str(self)}>"


class InstructionMove(Instruction):
    def __init__(self):
        super().__init__("move")

    def __call__(self, *args):
        self.src = args[0]
        self.dest = args[1]
        return self

    def __str__(self):
        return f"{self.name} src: {self.src} dest: {self.dest}"


class InstructionJmp(Instruction):
    def __init__(self):
        super().__init__("jmp")

    def __call__(self, *args):
        self.src = args[0]
        return self


class InstructionRtn(Instruction):
    def __init__(self):
        super().__init__("rtn")


class InstructionHalt(Instruction):
    def __init__(self):
        super().__init__("halt")


class InstructionSet:
    def __init__(self):
        print("Loading instruction set...")

        self.instructions = {
            "move": InstructionMove(),
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
