from .instruction import Instruction


class InstructionJEQ(Instruction):
    def __init__(self, code):
        super().__init__("jeq", code)
        self._dest = ""

    @property
    def dest(self):
        return self._dest

    @dest.setter
    def dest(self, label):
        self._dest = f"{label}".zfill(2)

    def __len__(self):
        return 2

    def __str__(self):
        return f"{self.code}{self.dest}"
