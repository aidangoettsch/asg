from s_expression import *


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, o):
        return Point(self.x + o.x, self.y + o.y)

    def __str__(self):
        return f"({self.x}, {self.y})"


class BoundingBox:
    def __init__(self, ul_corner, lr_corner):
        self.ul_corner = ul_corner
        self.lr_corner = lr_corner


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


class LibraryComponent:
    def __init__(
        self, name, full_name, pin_locations, inputs, outputs, s_expression, properties
    ):
        self.name = name
        self.full_name = full_name
        self.pin_count = len(pin_locations)
        self.pin_locations = pin_locations
        self.inputs = inputs
        self.outputs = outputs
        self.s_expression = s_expression
        self.properties = properties


class LibraryProperty:
    def __init__(self, key, value, id, location, effects):
        self.key = key
        self.value = value
        self.id = id
        self.location = location
        self.effects = effects

    def to_s_expression(self, location_offset: Point):
        return SExpressionList(
            "property",
            [
                self.key,
                self.value,
                SExpressionList("id", [self.id]),
                SExpressionList(
                    "at",
                    [
                        self.location[0] + location_offset.x,
                        self.location[1] + location_offset.y,
                        self.location[2],
                    ],
                ),
                *(
                    [SExpressionList("effects", self.effects)]
                    if self.effects != []
                    else []
                ),
            ],
        )


class CircuitInout(Component):
    def __init__(self, identifier=""):
        super().__init__()
        self.human_name = "Inout" + ("" if identifier == "" else (" " + identifier))
        self.identifier = identifier
        self.pin_count = 1
        self.pin_locations = [Point(0, 0)]
        self.inputs = [0]
        self.outputs = [0]


class CircuitInput(Component):
    def __init__(self, identifier=""):
        super().__init__()
        self.human_name = "Input" + ("" if identifier == "" else (" " + identifier))
        self.identifier = identifier
        self.pin_count = 1
        self.pin_locations = [Point(0, 0)]
        self.outputs = [0]


class CircuitOutput(Component):
    def __init__(self, identifier=""):
        super().__init__()
        self.human_name = "Output" + ("" if identifier == "" else (" " + identifier))
        self.identifier = identifier
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


class Diode(Component):
    def __init__(self, model):
        super().__init__()
        self.human_name = "diode"
        self.pin_count = 2
        self.pin_locations = [Point(-10, 0), Point(10, 0)]
        self.inputs = [1]
        self.outputs = [0]
        self.resistance_ohms = model


class Cell(Component):
    def __init__(self, cell_config):
        super().__init__()
        self.human_name = cell_config.name
        self.pin_count = cell_config.pin_count
        self.inputs = cell_config.inputs
        self.outputs = cell_config.outputs
        self.pin_locations = cell_config.pin_locations
