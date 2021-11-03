class Stack:
    def __init__(self, max_size=1000):
        self.max_size = max_size
        self.stack = []

    @property
    def top(self):
        try:
            return self.stack[-1]

        except IndexError:
            return None

    def pop(self):
        try:
            return self.stack.pop()

        except IndexError:
            return None

    def push(self, data):
        if len(self) < self.max_size:
            self.stack.append(data)

        else:
            raise Exception("Stack Blown")

    def __len__(self):
        return len(self.stack)

    @property
    def empty(self):
        return len(self) < 1

    def __str__(self):
        return f"Size: {len(self)} | Peek: {self.top}"

    def __repr__(self):
        return f"<Stack: {str(self)}>"
