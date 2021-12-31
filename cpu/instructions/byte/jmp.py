from .instruction import Instruction


class InstructionJmp(Instruction):
    def __init__(self, code):
        super().__init__("jmp", code)
        self._dest = ""

    @property
    def dest(self):
        return self._dest

    @dest.setter
    def dest(self, dest):
        self._dest = f"{dest}".zfill(2)

    def __str__(self):
        return f"{self.code}{self.dest}"
