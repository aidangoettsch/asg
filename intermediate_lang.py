from entities import *


class InputIL:
    def __init__(self):
        self.components = [
            CircuitInput(),
            Resistor(),
            Resistor(),
            CircuitOutput(),
        ]
        self.connections = [
            Connection(0, 0, 1, 0),
            Connection(1, 1, 2, 0),
            Connection(2, 1, 3, 0),
        ]


class OutputIL:
    def __init__(self):
        self.components = []
        self.lines = []
