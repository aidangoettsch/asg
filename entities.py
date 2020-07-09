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


class CircuitInout(Component):
    def __init__(self, identifier=""):
        super().__init__()
        self.human_name = "Inout" + ("" if identifier == "" else (" " + identifier))
        self.pin_count = 1
        self.pin_locations = [Point(0, 0)]
        self.inputs = [0]
        self.outputs = [0]


class CircuitInput(Component):
    def __init__(self, identifier=""):
        super().__init__()
        self.human_name = "Input" + ("" if identifier == "" else (" " + identifier))
        self.pin_count = 1
        self.pin_locations = [Point(0, 0)]
        self.outputs = [0]


class CircuitOutput(Component):
    def __init__(self, identifier=""):
        super().__init__()
        self.human_name = "Output" + ("" if identifier == "" else (" " + identifier))
        self.pin_count = 1
        self.pin_locations = [Point(0, 0)]
        self.inputs = [0]


class Resistor(Component):
    def __init__(self, resistance_ohms):
        super().__init__()
        self.human_name = "resistor"
        self.pin_count = 2
        self.pin_locations = [Point(-10, 0), Point(10, 0)]
        self.inputs = [1]
        self.outputs = [0]
        self.resistance_ohms = resistance_ohms


class Cell(Component):
    cell_configs = {
        "BUFX2": {
            "pin_count": 4,
            "inputs": [2],
            "outputs": [3],
            "pin_locations": [Point(0, 0), Point(0, 0), Point(0, 0), Point(0, 0)],
        },
        "INVX1": {
            "pin_count": 4,
            "inputs": [0],
            "outputs": [1],
            "pin_locations": [Point(0, 0), Point(0, 0), Point(0, 0), Point(0, 0)],
        },
        "NAND2X1": {
            "pin_count": 5,
            "inputs": [3, 4],
            "outputs": [1],
            "pin_locations": [
                Point(0, 0),
                Point(0, 0),
                Point(0, 0),
                Point(0, 0),
                Point(0, 0),
            ],
        },
        "OAI21X1": {
            "pin_count": 6,
            "inputs": [2, 3, 5],
            "outputs": [4],
            "pin_locations": [
                Point(0, 0),
                Point(0, 0),
                Point(0, 0),
                Point(0, 0),
                Point(0, 0),
                Point(0, 0),
            ],
        },
    }

    def __init__(self, cell_fullname):
        super().__init__()
        self.human_name = cell_fullname
        cell_config = Cell.cell_configs[cell_fullname]
        self.pin_count = cell_config["pin_count"]
        self.inputs = cell_config["inputs"]
        self.outputs = cell_config["outputs"]
        self.pin_locations = cell_config["pin_locations"]
