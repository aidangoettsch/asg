from entities import *


class InputIL:
    def __init__(self, components, connections):
        self.components = components
        self.connections = connections


class OutputIL:
    def __init__(self):
        self.components = []
        self.lines = []
