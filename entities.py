from s_expression import *


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f"({self.x}, {self.y})"


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

    @property
    def line_segments(self):
        res = []
        last_loc = self.locations[0]
        for loc in self.locations[1:]:
            res.append((last_loc, loc))
            last_loc = loc
        return res


class BoundingBox:
    def __init__(self, ul_corner=Point(0, 0), lr_corner=Point(0, 0)):
        self.ul_corner = ul_corner
        self.lr_corner = lr_corner

    @staticmethod
    def from_line_segment(line_segment):
        point_1 = line_segment[0]
        point_2 = line_segment[1]

        ul_corner = Point(0, 0)
        lr_corner = Point(0, 0)
        if point_1.x < point_2.x:
            ul_corner.x = point_1.x
            lr_corner.x = point_2.x
        else:
            ul_corner.x = point_2.x
            lr_corner.x = point_1.x
        if point_1.y < point_2.y:
            ul_corner.y = point_1.y
            lr_corner.y = point_2.y
        else:
            ul_corner.y = point_2.y
            lr_corner.y = point_1.y

        return BoundingBox(ul_corner, lr_corner)

    def intersects(self, other: "BoundingBox"):
        return (
            self.ul_corner.x <= other.lr_corner.x
            and self.lr_corner.x >= other.ul_corner.x
            and self.ul_corner.y <= other.lr_corner.y
            and self.lr_corner.y >= other.ul_corner.y
        )

    def expand(self, x_len, y_len):
        self.ul_corner.x -= x_len / 2
        self.lr_corner.x += x_len / 2
        self.ul_corner.y -= y_len / 2
        self.lr_corner.y += y_len / 2

    def __add__(self, point: Point):
        return BoundingBox(self.ul_corner + point, self.lr_corner + point)


class Component:
    def __init__(self):
        self.human_name = ""
        self.pin_count = -1
        self.pin_locations = []
        self.inputs = []
        self.outputs = []
        self.location = Point(0, 0)
        self.mirrored_over_x = False
        self.mirrored_over_y = False
        self.bounding_box_backing = BoundingBox()

    def mirror_over_x(self):
        self.mirrored_over_x = not self.mirrored_over_x
        for pin in self.pin_locations:
            self.pin_locations[pin].y = -self.pin_locations[pin].y

    def mirror_over_y(self):
        self.mirrored_over_y = not self.mirrored_over_y
        for pin in self.pin_locations:
            self.pin_locations[pin].x = -self.pin_locations[pin].x

    @property
    def bounding_box(self) -> BoundingBox:
        return self.bounding_box_backing + self.location

    @bounding_box.setter
    def bounding_box(self, bounding_box):
        self.bounding_box_backing = bounding_box

    def __str__(self):
        return f"{self.human_name} at ({self.location.x}, {self.location.y})"


class LibraryComponent:
    def __init__(
        self,
        name,
        full_name,
        pin_locations,
        inputs,
        outputs,
        s_expression,
        properties,
        bounding_box,
    ):
        self.name = name
        self.full_name = full_name
        self.pin_count = len(pin_locations)
        self.pin_locations = pin_locations
        self.inputs = inputs
        self.outputs = outputs
        self.s_expression = s_expression
        self.properties = properties
        self.bounding_box = bounding_box


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
        self.bounding_box_backing = cell_config.bounding_box
