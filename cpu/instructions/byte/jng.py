from .instruction import Instruction


class InstructionJNG(Instruction):
    def __init__(self):
        super().__init__("jng", 8)
        self.label = ""
        self.operands = 2

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, label):
        self._label = f"{label}".zfill(2)

    def __str__(self):
        return f"{str(hex(int(self.code)))[2:].zfill(2)}{self.label}"
