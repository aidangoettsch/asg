from asg.entities import *
from typing import List
from bentley_ottmann.planar import segments_intersections


class InputIL:
    """
    Represents a circuit being input to the ASG
    """

    def __init__(
        self,
        components: List[Component],
        connections: List[Connection],
        inouts: List[str],
    ):
        """
        Create an InputIL
        :param components: Components in the circuit
        :param connections: Connections between components in the circuit
        """
        self.components = components
        self.connections = connections
        self.inouts = inouts


class OutputIL:
    """
    Represents a circuit being output from the ASG
    """

    def __init__(self):
        self.components = []
        self.connections = []
        self.lines = []
        self.line_bins = {}

    def create_lines(self) -> None:
        """
        Draws an initial set of lines between components
        :return: None
        """
        res = []
        for connection in self.connections:
            start_component = self.components[connection.start_entity]
            end_component = self.components[connection.end_entity]
            start_pin_location = (
                start_component.location
                + start_component.pin_locations[connection.start_pin]
            )
            end_pin_location = (
                end_component.location + end_component.pin_locations[connection.end_pin]
            )

            x_midpoint = (start_pin_location.x + end_pin_location.x) / 2
            bend_start = Point(x_midpoint, start_pin_location.y)
            bend_end = Point(x_midpoint, end_pin_location.y)
            bends = [bend_start, bend_end]
            res.append(Line(connection, start_pin_location, *bends, end_pin_location))

        self.lines = res

    def repair_lines(self) -> None:
        """
        Draws an initial set of lines between components if they don't exist, shifts existing lines to match component locations
        :return: None
        """
        if len(self.lines) == 0:
            self.create_lines()
        else:
            for line in self.lines:
                connection = line.connection
                start_component = self.components[connection.start_entity]
                end_component = self.components[connection.end_entity]
                start_pin_location = (
                    start_component.location
                    + start_component.pin_locations[connection.start_pin]
                )
                end_pin_location = (
                    end_component.location
                    + end_component.pin_locations[connection.end_pin]
                )

                # If the line can be straight we do that
                if (
                    start_pin_location.x == end_pin_location.x
                    or start_pin_location.y == end_pin_location.y
                ):
                    line.locations = [start_pin_location, end_pin_location]

                if not (
                    start_pin_location == line.locations[0]
                    and end_pin_location == line.locations[-1]
                ):
                    # Change locations of lines when components move
                    if len(line.locations) < 4:
                        # Add a bend if the line was previously straight
                        x_midpoint = (start_pin_location.x + end_pin_location.x) / 2
                        bend_start = Point(x_midpoint, start_pin_location.y)
                        bend_end = Point(x_midpoint, end_pin_location.y)
                        bends = [bend_start, bend_end]
                        line.locations = [start_pin_location, *bends, end_pin_location]
                    else:
                        # Otherwise, just change the y of the existing points to match
                        line.locations[0] = start_pin_location
                        line.locations[1].y = start_pin_location.y
                        line.locations[-2].y = end_pin_location.y
                        line.locations[-1] = end_pin_location

    def create_line_bins(self, bin_size):
        self.line_bins = {}
        for line in self.lines:
            for segment in line.line_segments:
                bin_1 = segment[0] / bin_size
                bin_2 = segment[0] / bin_size
                if bin_1 == bin_2:
                    bins = [bin_1]
                else:
                    bins = [bin_2]
                    for bin_x in range(bin_1.x, bin_2.x):
                        for bin_y in range(bin_1.y, bin_2.y):
                            bins.append(Point(bin_x, bin_y))
                for line_bin in bins:
                    if bin_1 not in self.line_bins:
                        self.line_bins[line_bin] = []
                    self.line_bins[line_bin].append(line)

    def get_line_intersects_line(self) -> List[List[Line]]:
        """
        Finds lines where two of their segments intersect each other.
        :return: A list of line segment pairs
        """
        intersections = []
        for line_bin in self.line_bins.values():
            segments = []
            line_idx_map = []
            for line in line_bin:
                for segment in line.line_segments:
                    if segment[0] != segment[1]:
                        segments.append((segment[0].as_tuple(), segment[1].as_tuple()))
                        line_idx_map.append(line)

            for collision_point in segments_intersections(segments).values():
                for intersection in collision_point:
                    intersections.append([line_idx_map[i] for i in intersection])
        return intersections


class LibraryIL:
    """
    Represents a symbol library, indexed by cell name
    """

    def __init__(self):
        """
        Create a LibraryIL
        """
        self.symbols = {}
