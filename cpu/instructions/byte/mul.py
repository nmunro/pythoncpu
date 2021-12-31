from .arithmetic import ArithmeticMixin
from .instruction import Instruction


class InstructionMulByte(Instruction, ArithmeticMixin):
    def __init__(self, code):
        super().__init__("mul.b", code)
