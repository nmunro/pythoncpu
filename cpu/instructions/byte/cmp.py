from .instruction import Instruction


class InstructionCMPByte(Instruction):
    def __init__(self, code):
        super().__init__("cmp.b", code)
        self.src = ""
        self.src_type = ""
        self.dest = ""
        self.dest_type = ""
        self.operands = 3

    def __str__(self):
        return f"{self.code}{str(self.src_type.value).zfill(2)}{self.src}{str(self.dest_type.value).zfill(2)}{self.dest}"
