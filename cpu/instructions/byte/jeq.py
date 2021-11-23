from .instruction import Instruction


class InstructionJEQ(Instruction):
    def __init__(self, code):
        super().__init__("jeq", code)
        self._label = ""
        self.operands = 2

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, label):
        self._label = f"{label}".zfill(2)

    def __str__(self):
        return f"{self.code}{self.label}"
