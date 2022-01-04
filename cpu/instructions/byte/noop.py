from .instruction import Instruction


class InstructionNoOp(Instruction):
    def __init__(self, code):
        super().__init__("noop", code)

    def __len__(self):
        return 1
