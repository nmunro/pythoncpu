from .byte import InstructionDefine
from .byte import InstructionHalt
from .byte import InstructionJNG
from .byte import InstructionJNZ
from .byte import InstructionJmp
from .byte import InstructionJEQ
from .byte import InstructionJNE
from .byte import InstructionNoOp
from .byte import InstructionMoveByte
from .byte import InstructionCMPByte


class InstructionSet:
    def __init__(self):
        noop = InstructionNoOp()
        move_byte = InstructionMoveByte()
        jmp = InstructionJmp()
        jng = InstructionJNG()
        jnz = InstructionJNZ()

        jeq = InstructionJEQ()
        jne = InstructionJNE()

        halt = InstructionHalt()
        define = InstructionDefine()
        cmp_byte = InstructionCMPByte()

        self.instructions = {
            f"{noop.name}": noop,
            f"{noop.code}": noop,

            f"{move_byte.name}": move_byte,
            f"{move_byte.code}": move_byte,

            f"{jmp.name}": jmp,
            f"{jmp.code}": jmp,

            f"{jng.name}": jng,
            f"{jng.code}": jng,

            f"{jnz.name}": jnz,
            f"{jnz.code}": jnz,

            f"{jeq.name}": jeq,
            f"{jeq.code}": jeq,

            f"{jne.name}": jne,
            f"{jne.code}": jne,

            f"{halt.name}": halt,
            f"{halt.code}": halt,

            f"{define.name}": define,
            f"{define.code}": define,

            f"{cmp_byte.name}": cmp_byte,
            f"{cmp_byte.code}": cmp_byte,
        }

    def __len__(self):
        return len(self.instructions)

    def __str__(self):
        return f"Instructions: {len(self)}"

    def __repr__(self):
        return f"<InstructionSet: {str(self)}>"

    def __getitem__(self, name):
        return self.instructions[name]
