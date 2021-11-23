from .byte import InstructionAddByte
from .byte import InstructionSubByte
from .byte import InstructionMulByte
from .byte import InstructionDivByte
from .byte import InstructionIncByte
from .byte import InstructionDecByte
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
        add_byte = InstructionAddByte("00")
        sub_byte = InstructionSubByte("01")
        mul_byte = InstructionMulByte("02")
        div_byte = InstructionDivByte("03")
        inc_byte = InstructionIncByte("04")
        dec_byte = InstructionDecByte("05")
        noop = InstructionNoOp("06")
        move_byte = InstructionMoveByte("07")
        jmp = InstructionJmp("08")
        jng = InstructionJNG("09")
        jnz = InstructionJNZ("0a")
        jeq = InstructionJEQ("0b")
        jne = InstructionJNE("0c")
        halt = InstructionHalt("0d")
        cmp_byte = InstructionCMPByte("0e")

        self.instructions = {
            f"{add_byte.name}": add_byte,
            f"{add_byte.code}": add_byte,

            f"{sub_byte.name}": sub_byte,
            f"{sub_byte.code}": sub_byte,

            f"{mul_byte.name}": mul_byte,
            f"{mul_byte.code}": mul_byte,

            f"{div_byte.name}": div_byte,
            f"{div_byte.code}": div_byte,

            f"{inc_byte.name}": inc_byte,
            f"{inc_byte.code}": inc_byte,

            f"{dec_byte.name}": dec_byte,
            f"{dec_byte.code}": dec_byte,

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
