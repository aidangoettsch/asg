from asg.entities import *
from typing import List
from bentley_ottmann.planar import segments_intersections
import numpy as np
import itertools


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


def get_segment_slope(segment: Tuple[Point]):
    """
    Find the slope of a line segment
    :param segment: A pair of points that represent a line segment
    :return: The slope of segment
    """
    return (
        (segment[0].y - segment[1].y) / (segment[0].x - segment[1].x)
        if (segment[0].x - segment[1].x) != 0
        else float("inf")
    )


def point_cross_product(point_1, point_2):
    return point_1.x * point_2.y - point_2.x * point_1.y


def point_loc_relative_to_line(segment, point):
    segment_second_prime = Point(
        segment[1].x - segment[0].x, segment[1].y - segment[0].y
    )
    point_prime = Point(point.x - segment[0].x, point.y - segment[0].y)
    r = point_cross_product(segment_second_prime, point_prime)
    return r if r == 0 else np.sign(r)


def a_sandwiches_b(segment_a, segment_b):
    b_0 = point_loc_relative_to_line(segment_b, segment_a[0])
    b_1 = point_loc_relative_to_line(segment_b, segment_a[1])

    return b_0 != b_1 and b_0 != 0 and b_1 != 0


def check_cross(segment_1, segment_2):
    slope_1 = get_segment_slope(segment_1)
    slope_2 = get_segment_slope(segment_2)
    if slope_1 == slope_2:
        return BoundingBox.from_line_segment(segment_1).intersects(
            BoundingBox.from_line_segment(segment_2)
        )

    return a_sandwiches_b(segment_1, segment_2) and a_sandwiches_b(segment_2, segment_1)


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
                bin_1 = segment[0] // bin_size
                bin_2 = segment[1] // bin_size
                if bin_1 == bin_2:
                    bins = [bin_1]
                else:
                    bins = []
                    for bin_x in range(bin_1.x, bin_2.x + 1):
                        for bin_y in range(bin_1.y, bin_2.y + 1):
                            bins.append(Point(bin_x, bin_y))
                for line_bin in bins:
                    if line_bin not in self.line_bins:
                        self.line_bins[line_bin] = set()
                    self.line_bins[line_bin].add(line)

    def get_line_intersects_line(self) -> List[List[Line]]:
        """
        Finds lines where two of their segments intersect each other.
        :return: A list of line segment pairs
        """
        intersections = []

        for line_bin in self.line_bins.values():
            for connection_pair in itertools.combinations(line_bin, 2):
                line_segments = (
                    connection_pair[0].line_segments + connection_pair[1].line_segments
                )

                for segment_pair in itertools.combinations(line_segments, 2):
                    if check_cross(segment_pair[0], segment_pair[1]):
                        intersections.append(connection_pair)
        # for line_bin in self.line_bins.values():
        #     segments = []
        #     line_idx_map = []
        #     for line_1, line_2 in itertools.combinations(line_bin, 2):
        #         for segment in line_1.line_segments:
        #             if segment[0] != segment[1]:
        #                 line_idx_map.append(line_1)
        #                 segments.append(((segment[0].x, segment[0].y), (segment[1].x, segment[1].y)))
        #         for segment in line_2.line_segments:
        #             if segment[0] != segment[1]:
        #                 line_idx_map.append(line_2)
        #                 segments.append(((segment[0].x, segment[0].y), (segment[1].x, segment[1].y)))
        #
        #     for collision_point in segments_intersections(segments).values():
        #         for intersection in collision_point:
        #             intersections.append([line_idx_map[i] for i in intersection])
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
