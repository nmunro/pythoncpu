class Instruction:
    def __init__(self, name, code):
        self.name = name.lower()
        self.code = f"{code}".zfill(2)
        self.operands = 1
        self.length = 1
        self.loop_count = 0
        self.src_type = None
        self.dest_type = None

    def __len__(self):
        return self.operands

    def __index__(self):
        return int(self)

    def __int__(self):
        return self.code

    def __hex__(self):
        return hex(self)

    def __eq__(self, other):
        if not type(other) == str:
            raise TypeError("Must be a string")

        return self.name == other

    def __str__(self):
        return f"{str(hex(int(self.code)))[2:].zfill(2)}"

    def __repr__(self):
        return f"<Instruction (self.name): {hex(self)}>"

    def __iter__(self):
        self.loop_count = 0
        return self

    def __next__(self):
        if self.loop_count < self.operands:
            result = self.loop_count
            self.loop_count += 1
            return result

        else:
            raise StopIteration
