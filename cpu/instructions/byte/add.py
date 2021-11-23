from .instruction import Instruction


class InstructionAddByte(Instruction):
    def __init__(self, code):
        super().__init__("add.b", code)
        self.src = ""
        self.dest = ""
        self.operands = 3

    def __str__(self):
        return f"{str(hex(int(self.code)))[2:].zfill(2)}{self.src.zfill(2)}{self.dest.zfill(2)}"
