from enum import Enum


class Magnitude(Enum):
    HZ = 1
    KHZ = 1000
    MHZ = 1000000
    GHZ = 1000000000


class Clock:
    def __init__(self, speed, magnitude):
        self.speed = speed
        self.magnitude = Magnitude[magnitude.upper()]

    @property
    def tick(self):
        return 1 / (self.speed * self.magnitude.value)

    def __str__(self):
        return f"{self.speed} {self.magnitude.name}"

    def __repr__(self):
        return f"<Clock: {str(self)}>"
