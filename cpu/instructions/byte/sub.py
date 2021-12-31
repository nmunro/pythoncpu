from .arithmetic import ArithmeticMixin
from .instruction import Instruction


class InstructionSubByte(Instruction, ArithmeticMixin):
    def __init__(self, code):
        super().__init__("sub.b", code)
