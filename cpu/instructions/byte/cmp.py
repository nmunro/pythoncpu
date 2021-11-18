from .instruction import Instruction


class InstructionCMPByte(Instruction):
    def __init__(self):
        super().__init__("cmp.b", 6)
        self.source = ""
        self.destination = ""
        self.operands = 3

    def __str__(self):
        return f"{str(hex(int(self.code)))[2:].zfill(2)}{self.source}{self.destination}"
