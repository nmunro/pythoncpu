from .instruction import Instruction


class InstructionHalt(Instruction):
    def __init__(self, code):
        super().__init__("halt", code)

    def __str__(self):
        return self.code
