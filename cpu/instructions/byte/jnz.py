from .instruction import Instruction


class InstructionJNZ(Instruction):
    def __init__(self, code):
        super().__init__("jnz", code)
        self._dest = ""

    @property
    def dest(self):
        return self._dest

    @dest.setter
    def dest(self, label):
        self._dest = f"{label}".zfill(2)

    def __str__(self):
        return f"{self.code}{self.dest}"
