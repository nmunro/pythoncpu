from .arithmetic import ArithmeticMixin
from .instruction import Instruction


class InstructionDivByte(Instruction, ArithmeticMixin):
    def __init__(self, code):
        super().__init__("div.b", code)
