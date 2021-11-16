from .byte import InstructionDefine
from .byte import InstructionHalt
from .byte import InstructionJmp
from .byte import InstructionNoOp
from .byte import InstructionMoveByte


class InstructionSet:
    def __init__(self):
        self.instructions = {
            "noop": InstructionNoOp(),
            "00": InstructionNoOp(),

            "move.b": InstructionMoveByte(),
            "01": InstructionMoveByte(),

            "jmp": InstructionJmp(),
            "02": InstructionJmp(),

            "halt": InstructionHalt(),
            "04": InstructionHalt(),

            "define": InstructionDefine(),
            "05": InstructionDefine(),
        }

    def __len__(self):
        return len(self.instructions)

    def __str__(self):
        return f"Instructions: {len(self)}"

    def __repr__(self):
        return f"<InstructionSet: {str(self)}>"

    def __getitem__(self, name):
        return self.instructions[name]
