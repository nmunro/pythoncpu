from cpu import CPU
from vram import VRAM


class VM:
    def __init__(self, registers, clock, vram):
        self.vram = VRAM(vram)
        self.cpu = CPU(registers, clock, self.vram)

    def boot(self, program):
        print(self)
        self.cpu.boot(program)

    def run(self):
        while not self.cpu.stop:
            self.cpu.run()

    def halt(self):
        self.cpu.halt()
        self.cpu.show()

    def __str__(self):
        output = ["NMunro VM", f"CPU: {str(self.cpu)}", f"Memory: {str(self.vram)}"]
        return "\n".join(output)

    def __repr__(self):
        return f"<VM: {str(self)}>"
