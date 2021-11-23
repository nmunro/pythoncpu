from .instruction import Instruction


class InstructionCMPByte(Instruction):
    def __init__(self, code):
        super().__init__("cmp.b", code)
        self.src = ""
        self.dest = ""
        self.operands = 3

    def __str__(self):
        return f"{self.code}{self.src}{self.dest}"
