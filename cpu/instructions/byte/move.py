from .instruction import Instruction


class InstructionMoveByte(Instruction):
    def __init__(self):
        super().__init__("move.b", "01")
        self.src = ""
        self.dest = ""
        self.operands = 3

    def __str__(self):
        return f"{str(hex(int(self.code)))[2:].zfill(2)}{self.src.zfill(2)}{self.dest.zfill(2)}"
