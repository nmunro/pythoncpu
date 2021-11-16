from pathlib import Path
import unittest

from cpu.clock import Clock
from cpu.vm import VM


class MainTests(unittest.TestCase):
    def setUp(self):
        registers = 8
        clock = Clock(4, "hz")
        memory = 16

        self.vm = VM(registers, clock, memory)

    def test_smoke_test(self):
        self.vm.boot(Path("../examples/1.bin"))
        self.vm.run()

    def test_basic_noop(self):
        self.vm.boot(Path("../examples/2.bin"))
        self.vm.run()


if __name__ == '__main__':
    unittest.main()
