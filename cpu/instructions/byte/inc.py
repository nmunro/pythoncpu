from .instruction import Instruction


class InstructionIncByte(Instruction):
    def __init__(self, code):
        super().__init__("inc.b", code)
        self.dest = ""
        self.operands = 2

    def __str__(self):
        return f"{str(hex(int(self.code)))[2:].zfill(2)}{self.dest.zfill(2)}"
