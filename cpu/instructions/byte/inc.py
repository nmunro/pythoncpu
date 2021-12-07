from .instruction import Instruction


class InstructionIncByte(Instruction):
    def __init__(self, code):
        super().__init__("inc", code)
        self.dest = ""
        self.operands = 2

    def __str__(self):
        return f"{self.code}{self.dest.zfill(2)}"
