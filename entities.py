class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, o):
        return Point(self.x + o.x, self.y + o.y)


class Connection:
    def __init__(self, start_entity, start_pin, end_entity, end_pin):
        self.start_entity = start_entity
        self.start_pin = start_pin
        self.end_entity = end_entity
        self.end_pin = end_pin


class Line:
    def __init__(self, connection, *locations):
        self.connection = connection
        self.locations = locations


class Component:
    def __init__(self):
        self.human_name = ""
        self.pin_count = -1
        self.pin_locations = []
        self.inputs = []
        self.outputs = []
        self.location = Point(0, 0)

    def __str__(self):
        return f"{self.human_name} at ({self.location.x}, {self.location.y})"


class CircuitInput(Component):
    def __init__(self):
        super().__init__()
        self.human_name = "circuit_input"
        self.pin_count = 1
        self.pin_locations = [Point(0, 0)]
        self.outputs = [0]


class CircuitOutput(Component):
    def __init__(self):
        super().__init__()
        self.human_name = "circuit_output"
        self.pin_count = 1
        self.pin_locations = [Point(0, 0)]
        self.inputs = [0]


class Resistor(Component):
    def __init__(self):
        super().__init__()
        self.human_name = "resistor"
        self.pin_count = 2
        self.pin_locations = [Point(-10, 0), Point(10, 0)]
        self.inputs = [0]
        self.outputs = [1]
