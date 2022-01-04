from .instruction import Instruction


class InstructionMoveByte(Instruction):
    def __init__(self, code):
        super().__init__("move.b", code)

    def __len__(self):
        return 5

    def __str__(self):
        return f"{self.code}{str(self.src_type.value).zfill(2)}{self.src.zfill(2)}{str(self.dest_type.value).zfill(2)}{self.dest.zfill(2)}"
