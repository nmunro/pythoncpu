from .instruction import Instruction


class InstructionSubByte(Instruction):
    def __init__(self, code):
        super().__init__("sub.b", code)
        self.src = ""
        self.dest = ""
        self.operands = 3

    def __str__(self):
        return f"{self.code}{self.src.zfill(2)}{self.dest.zfill(2)}"
