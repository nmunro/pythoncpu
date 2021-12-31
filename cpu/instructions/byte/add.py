from .arithmetic import ArithmeticMixin
from .instruction import Instruction


class InstructionAddByte(Instruction, ArithmeticMixin):
    def __init__(self, code):
        super().__init__("add.b", code)
