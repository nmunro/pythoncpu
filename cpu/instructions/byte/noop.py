from .instruction import Instruction


class InstructionNoOp(Instruction):
    def __init__(self):
        super().__init__("noop", 0)
