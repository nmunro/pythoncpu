from .instruction import Instruction


class InstructionDecByte(Instruction):
    def __init__(self, code):
        super().__init__("dec", code)

    def __str__(self):
        return f"{self.code}{self.dest_type.zfill(2)}{self.dest.zfill(2)}"
