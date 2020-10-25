from asg.grammar import *
from typing import List, Tuple, Dict, Union


class Point:
    """
    A point in 2D space
    """

    def __init__(self, x: float, y: float):
        """
        Create a point
        :param x: X coordinate
        :param y: Y coordinate
        """
        self.x = x
        self.y = y

    def __add__(self, other: "Point"):
        """
        Add two points together
        :param other: Another point
        :return: A point at the sum of the X and Y locations of this point and other
        """
        return Point(self.x + other.x, self.y + other.y)

    def __mul__(self, other: float):
        """
        Shift the point further from the origin by a factor of other
        :param other: Scalar to multiply by
        :return: A point multiplied by the scalar other
        """
        return Point(self.x / other, self.y / other)

    def __truediv__(self, other: float):
        """
        Shift the point closer to the origin by a factor of other
        :param other: Scalar to divide by
        :return: A point divided by the scalar other
        """
        return Point(self.x / other, self.y / other)

    def __floordiv__(self, other: float):
        """
        Shift the point closer to the origin by a factor of other, with
        x and y rounded to the nearest integer
        :param other: Scalar to divide by
        :return: A point divided by the scalar other
        """
        return Point(int(self.x // other), int(self.y // other))

    def __eq__(self, other: "Point"):
        """
        Check if two points are equal to each other
        :param other: Another point
        :return: If this point is at the same location as other
        """
        return self.x == other.x and self.y == other.y

    def as_tuple(self) -> Tuple[float, float]:
        return self.x, self.y

    def __hash__(self):
        return int(self.x * 33 + self.y)

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

    def __str__(self):
        return f"({self.x}, {self.y})"


class Connection:
    """
    A connection between two components
    """

    def __init__(
        self,
        net_name: str,
        start_entity: int,
        start_pin: int,
        end_entity: int,
        end_pin: int,
    ):
        """
        Create a connection
        :param net_name: The name of the net from the netlist
        :param start_entity: The index of the component where the connection starts
        :param start_pin: The index of the pin on the component where the connection starts
        :param end_entity: The index of the component where the connection ends
        :param end_pin: The index of the pin on the component where the connection ends
        """
        self.net_name = net_name
        self.start_entity = start_entity
        self.start_pin = start_pin
        self.end_entity = end_entity
        self.end_pin = end_pin


class Line:
    """
    A graphical representation of the connection between two components
    """

    def __init__(self, connection: Connection, *locations: List[Point]):
        """
        Create a line
        :param connection: The connection between the locations
        :param locations: A list of points which represent the route the line travels
        """
        self.connection = connection
        self.locations = list(locations)

    @property
    def line_segments(self):
        """
        :return: The line segments that make up this line
        """
        res = []
        last_loc = self.locations[0]
        for loc in self.locations[1:]:
            res.append((last_loc, loc))
            last_loc = loc
        return res


class BoundingBox:
    """
    A rectangle which represents a bounding box which can be checked for intersection
    with other bounding boxes.
    """

    def __init__(self, ul_corner=Point(0, 0), lr_corner=Point(0, 0)):
        """
        Create a bounding box
        :param ul_corner: The upper left corner of the bounding box
        :param lr_corner: The lower left corner of the bounding box
        """
        self.ul_corner = ul_corner
        self.lr_corner = lr_corner

    @staticmethod
    def from_line_segment(line_segment: Tuple[Point]) -> "BoundingBox":
        """
        :param line_segment: A line segment, represented as a tuple of two points
        :return: The bounding box which encompasses the line segment
        """
        point_1 = line_segment[0]
        point_2 = line_segment[1]

        # Combine the coordinates from the segment to match the
        # corners used to represent the bounding box
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

    def intersects(self, other: "BoundingBox") -> bool:
        """
        Checks if this box intersects with other
        :param other: Another bounding box
        :return: If this bounding box intersects with other
        """
        return (
            self.ul_corner.x <= other.lr_corner.x
            and self.lr_corner.x >= other.ul_corner.x
            and self.ul_corner.y <= other.lr_corner.y
            and self.lr_corner.y >= other.ul_corner.y
        )

    def expand(self, x_len: float, y_len: float) -> None:
        """
        Expand this bounding box, keeping this center the same, but increasing
        the width and height by x_len and y_len, respectively
        :param x_len: The length to increase the width by
        :param y_len: The length to increase the height by
        :return: None
        """
        self.ul_corner.x -= x_len / 2
        self.lr_corner.x += x_len / 2
        self.ul_corner.y -= y_len / 2
        self.lr_corner.y += y_len / 2

    @property
    def center(self) -> Point:
        """
        The center of the bounding box
        :return: The center of the bounding box
        """
        return (self.ul_corner + self.lr_corner) / 2

    def __add__(self, other: Point) -> "BoundingBox":
        """
        Move the center of a bounding box, keeping the size the same
        :param other: The point which represents the offset
        :return: A new bounding box with the same size as this box, but shifted by other
        """
        return BoundingBox(self.ul_corner + other, self.lr_corner + other)


class Component:
    """
    A component in a schematic
    """

    def __init__(self, netlist_id):
        """
        Create a component
        """
        self.netlist_id = netlist_id
        self.human_name = ""
        self.pin_count = -1
        self.pin_locations = {}
        self.inputs = []
        self.outputs = []
        self.location = Point(0, 0)
        self.mirrored_over_x = False
        self.mirrored_over_y = False

        # Backing field for the bounding box property getter and setter
        self.bounding_box_backing = BoundingBox()

    def mirror_over_x(self):
        """
        Mirror the component over the horizontal axis and flip pin locations as needed
        :return: None
        """
        self.mirrored_over_x = not self.mirrored_over_x
        for pin in self.pin_locations:
            self.pin_locations[pin].y = -self.pin_locations[pin].y

    def mirror_over_y(self):
        """
        Mirror the component over the vertical axis and flip pin locations as needed
        :return: None
        """
        self.mirrored_over_y = not self.mirrored_over_y
        for pin in self.pin_locations:
            self.pin_locations[pin].x = -self.pin_locations[pin].x

    @property
    def bounding_box(self) -> BoundingBox:
        """
        :return: The bounding box of this component
        The backing field is offset by the location of the component
        """
        return self.bounding_box_backing + self.location

    @bounding_box.setter
    def bounding_box(self, bounding_box: BoundingBox) -> None:
        """
        Sets the new bounding box of the component
        :param bounding_box: The new bounding box, with (0, 0) being the center of the component
        :return: None
        """
        self.bounding_box_backing = bounding_box

    def __str__(self) -> str:
        """
        :return: A string representation of this component
        """
        return f"{self.human_name} at ({self.location.x}, {self.location.y})"


class LibraryProperty:
    """
    A property of an EESchema symbol
    """

    def __init__(
        self,
        key: str,
        value: Atom or str,
        ident: str,
        location: Tuple[float],
        effects: List[Atom],
    ):
        """
        Create a library property
        :param key: The property key
        :param value: The value of the property
        :param ident: A UUID for the property
        :param location: A tuple representing x, y, and orientation
        :param effects: Effects on the text of the property
        """
        self.key = key
        self.value = value
        self.id = ident
        self.location = location
        self.effects = effects

    def to_s_expression(self, location_offset: Point) -> Atom:
        """
        Transforms the property into an s-expression with an offset applied to its location
        :param location_offset: The location of the component this property belongs to
        :return: An s-expression which represents this property at the appropriate location
        """
        return Atom(
            "property",
            [
                self.key,
                self.value,
                Atom("id", [self.id]),
                Atom(
                    "at",
                    [
                        self.location[0] + location_offset.x,
                        self.location[1] + location_offset.y,
                        self.location[2],
                    ],
                ),
                *([Atom("effects", self.effects)] if self.effects != [] else []),
            ],
        )


class LibrarySymbol:
    """
    A symbol defined in a symbol library
    """

    def __init__(
        self,
        name: str,
        full_name: str,
        pin_locations: Dict[int, Point],
        inputs: List[int],
        outputs: List[int],
        raw_data: Union[Atom, str],
        properties: List[LibraryProperty],
        bounding_box: BoundingBox,
    ):
        """
        Create a library symbol
        :param name: The name of the symbol
        :param full_name: The full name of a component descended form this symbol
        :param pin_locations: The locations of pins on this symbol
        :param inputs: Which pins on this symbol are inputs
        :param outputs: Which pins on this symbol are outputs
        :param raw_data: Raw data for this symbol which comes from the specific schematic software
        :param properties: Properties of this symbol in EESchema
        :param bounding_box: The bounding box of this symbol
        """
        self.name = name
        self.full_name = full_name
        self.pin_count = len(pin_locations)
        self.pin_locations = pin_locations
        self.inputs = inputs
        self.outputs = outputs
        self.raw_data = raw_data
        self.properties = properties
        self.bounding_box = bounding_box


class CircuitInout(Component):
    """
    An input or output to the circuit that is currently ambiguous
    """

    def __init__(self, identifier=""):
        """
        Creates a CircuitInout
        :param identifier: The identifier of this input or output
        """
        super().__init__(identifier)
        self.human_name = "Inout" + ("" if identifier == "" else (" " + identifier))
        self.identifier = identifier
        self.pin_count = 1
        self.pin_locations = {
            0: Point(0, 0),
        }
        self.inputs = [0]
        self.outputs = [0]


class CircuitInput(Component):
    """
    An input to the circuit
    """

    def __init__(self, identifier=""):
        """
        Creates a CircuitInput
        :param identifier: The identifier of this input
        """
        super().__init__(identifier)
        self.human_name = "Input" + ("" if identifier == "" else (" " + identifier))
        self.identifier = identifier
        self.pin_count = 1
        self.pin_locations = {
            0: Point(0, 0),
        }
        self.outputs = [0]


class CircuitOutput(Component):
    """
    An output from the circuit
    """

    def __init__(self, identifier=""):
        """
        Creates a CircuitOutput
        :param identifier: The identifier of this output
        """
        super().__init__(identifier)
        self.human_name = "Output" + ("" if identifier == "" else (" " + identifier))
        self.identifier = identifier
        self.pin_count = 1
        self.pin_locations = {
            0: Point(0, 0),
        }
        self.inputs = [0]


class Resistor(Component):
    """
    A resistor inside the circuit
    """

    def __init__(self, netlist_id: str, resistance_ohms: float):
        """
        Create a Resistor
        :param resistance_ohms: The resistance of this resistor in ohms
        """
        super().__init__(netlist_id)
        self.human_name = "resistor"
        self.pin_count = 2
        self.pin_locations = {0: Point(-10, 0), 1: Point(10, 0)}
        self.inputs = [1]
        self.outputs = [0]
        self.resistance_ohms = resistance_ohms


class Diode(Component):
    """
    A diode inside the circuit
    """

    def __init__(self, netlist_id: str, model: str):
        """
        Create a Diode
        :param model: The model of this diode
        """
        super().__init__(netlist_id)
        self.human_name = "diode"
        self.pin_count = 2
        self.pin_locations = {0: Point(-10, 0), 1: Point(10, 0)}
        self.inputs = [1]
        self.outputs = [0]
        self.model = model


class Mosfet(Component):
    def __init__(self, netlist_id: str, fet_type: str):
        super().__init__(netlist_id)
        self.human_name = "MOSFET"
        self.pin_count = 2
        self.pin_locations = {0: Point(-10, 0), 1: Point(10, 0)}
        self.inputs = [1]
        self.outputs = [0]
        self.fet_type = fet_type


class Cell(Component):
    """
    A cell inside the circuit which is defined by a symbol
    """

    def __init__(self, netlist_id: str, cell_config: LibrarySymbol):
        """
        Create a Cell
        :param cell_config: Information from the library
        """
        super().__init__(netlist_id)
        self.human_name = cell_config.name
        self.pin_count = cell_config.pin_count
        self.inputs = cell_config.inputs
        self.outputs = cell_config.outputs
        self.pin_locations = cell_config.pin_locations
        self.raw_data = cell_config.raw_data
        self.bounding_box_backing = cell_config.bounding_box
