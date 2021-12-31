from .instruction import Instruction

class ArithmeticMixin:
    def __str__(self):
        return f"{self.code}{str(self.src_type.value).zfill(2)}{self.src.zfill(2)}{str(self.dest_type.value).zfill(2)}{self.dest.zfill(2)}"
