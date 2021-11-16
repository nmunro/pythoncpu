from .instruction import Instruction


class InstructionHalt(Instruction):
    def __init__(self):
        super().__init__("halt", 4)

    def __str__(self):
        return f"{str(hex(int(self.code)))[2:].zfill(2)}"
