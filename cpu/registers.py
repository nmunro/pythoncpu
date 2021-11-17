class Register:
    def __init__(self, name):
        self.name = name
        self.value = 0

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f"<Register: {str(self)}>"
