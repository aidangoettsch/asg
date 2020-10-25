from abc import abstractmethod
from typing import Tuple
import numpy
from asg.intermediate_lang import *
from asg.entities import *
import itertools


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


def get_segment_length(segment):
    """
    Find the length of a line segment
    :param segment: A pair of points that represent a line segment
    :return: The length of segment
    """
    return (
        ((segment[0].y - segment[1].y) ** 2) + ((segment[0].x - segment[1].x) ** 2)
    ) ** 0.5


class Constraint:
    """
    A restriction to apply to a schematic in order to optimize it
    """

    def __init__(self, output: OutputIL, options):
        self.output = output
        self.options = options

    @abstractmethod
    def get_score(self):
        pass

    @abstractmethod
    def maximize(self):
        pass


class LTRConstraint(Constraint):
    def __init__(self, output, options_override=None):
        super().__init__(output, options_override)

        self.inputs = [i for i, e in enumerate(output.components) if e.inputs == []]

        self.cache = {}

        for input_idx in self.inputs:
            self.cache[input_idx] = 0

        self.optimal_columns = [
            self.find_distance_from_input(i)
            for i, e in enumerate(self.output.components)
        ]

    def find_distance_from_input(self, component_idx, seen=None):
        if seen is None:
            seen = []
        if component_idx in seen:
            return -1
        if component_idx in self.cache:
            return self.cache[component_idx]

        distances = [
            self.find_distance_from_input(i, seen + [component_idx])
            for i, x in enumerate(self.output.adjacency[component_idx])
            if x == -1
        ]
        if len(distances) == 0 or numpy.all(distances == -1):
            return -1
        res = max(distances) + 1

        self.cache[component_idx] = res
        return res

    def get_score(self):
        starting_x = self.options["starting_x"]
        column_gap = self.options["column_gap"]
        return sum(
            [
                1
                for component_idx, component in enumerate(self.output.components)
                if component.location.x
                == starting_x + self.optimal_columns[component_idx] * column_gap
            ]
        )

    def maximize(self):
        starting_x = self.options["starting_x"]
        y_indicies = [self.options["starting_y"]] * (max(self.optimal_columns) + 1)
        column_gap = self.options["column_gap"]
        row_gap = self.options["row_gap"]

        for component_idx, component in enumerate(self.output.components):
            column = self.optimal_columns[component_idx]
            component.location = Point(
                starting_x + column * column_gap, y_indicies[column]
            )

            y_indicies[column] += row_gap


class VerticalSortConstraint(Constraint):
    def find_avg_input_y(self, component_idx):
        input_component_indicies = [
            i for i, e in enumerate(self.output.adjacency[component_idx]) if e == -1
        ]
        res = 0
        for input_component_idx in input_component_indicies:
            res += self.output.components[input_component_idx].location.y
        n = len(input_component_indicies)
        if n == 0:
            return self.output.components[component_idx].location.y
        return res / n

    def get_score(self):
        components_by_x = list(enumerate(self.output.components))
        components_by_x.sort(key=lambda c: c[1].location.x)
        error = 0
        for component in components_by_x:
            optimal_y = self.find_avg_input_y(component[0])
            error += abs(component[1].location.y - optimal_y)
        return -error

    def maximize(self):
        components_by_x = list(enumerate(self.output.components))
        components_by_x.sort(key=lambda c: c[1].location.x)
        for component_and_idx in components_by_x:
            optimal_y = self.find_avg_input_y(component_and_idx[0])
            component_and_idx[1].location.y = optimal_y


class InputYDegridConstraint(Constraint):
    def find_optimal_y(self, inp_idx):
        input_to = [i for i, e in enumerate(self.output.adjacency[inp_idx]) if e == 1]
        max_x = 0
        optimal_y = self.output.components[inp_idx].location.y
        for component_idx in input_to:
            component = self.output.components[component_idx]
            if component.location.x > max_x:
                max_x = component.location.x
                for connection in self.output.connections:
                    if (
                        connection.end_entity == component_idx
                        and connection.start_entity == inp_idx
                    ):
                        optimal_y = (
                            component.location.y
                            + component.pin_locations[connection.end_pin].y
                        )
        return optimal_y

    def get_score(self):
        error = 0
        for i, inp in enumerate(self.output.components):
            if type(inp) == CircuitInput:
                error += abs(inp.location.y - self.find_optimal_y(i))
        return -error

    def maximize(self):
        for i, inp in enumerate(self.output.components):
            if type(inp) == CircuitInput:
                inp.location.y = self.find_optimal_y(i)


class UntangleConstraint(Constraint):
    def get_score(self):
        return -len(self.output.get_line_intersects_line())

    def maximize(self):
        for crossing in self.output.get_line_intersects_line():
            if crossing[0].connection.end_entity == crossing[1].connection.end_entity:
                prev_crosses = 0
                component = self.output.components[crossing[0].connection.end_entity]
                connecting_lines = []
                line_bin_loc = component.location // self.options["bin_size"]
                try:
                    connecting_lines += self.output.line_bins[line_bin_loc]
                except:
                    pass
                try:
                    connecting_lines += self.output.line_bins[
                        line_bin_loc + Point(1, 0)
                    ]
                except:
                    pass
                try:
                    connecting_lines += self.output.line_bins[
                        line_bin_loc + Point(0, 1)
                    ]
                except:
                    pass
                try:
                    connecting_lines += self.output.line_bins[
                        line_bin_loc + Point(-1, 0)
                    ]
                except:
                    pass
                try:
                    connecting_lines += self.output.line_bins[
                        line_bin_loc + Point(0, -1)
                    ]
                except:
                    pass
                for connection_pair in itertools.combinations(connecting_lines, 2):
                    line_segments = (
                        connection_pair[0].line_segments
                        + connection_pair[1].line_segments
                    )

                    for segment_pair in itertools.combinations(line_segments, 2):
                        if check_cross(segment_pair[0], segment_pair[1]):
                            prev_crosses += 1
                self.output.components[
                    crossing[0].connection.end_entity
                ].mirror_over_x()
                self.output.repair_lines()
                new_crosses = 0
                for connection_pair in itertools.combinations(connecting_lines, 2):
                    line_segments = (
                        connection_pair[0].line_segments
                        + connection_pair[1].line_segments
                    )

                    for segment_pair in itertools.combinations(line_segments, 2):
                        if check_cross(segment_pair[0], segment_pair[1]):
                            new_crosses += 1
                if new_crosses > prev_crosses:
                    self.output.components[
                        crossing[0].connection.end_entity
                    ].mirror_over_x()
                    self.output.repair_lines()


class LinesAvoidBoundingBoxes(Constraint):
    def find_intersections(self):
        self.output.get_line_intersects_line()
        for line in self.output.lines:
            connection = line.connection
            for i, component in enumerate(self.output.components):
                colliding_segments = []
                for segment in line.line_segments:
                    segment_bounding_box = BoundingBox.from_line_segment(segment)
                    if (
                        component.bounding_box.intersects(segment_bounding_box)
                        and connection.start_entity != i
                        and connection.end_entity != i
                    ):
                        colliding_segments.append(segment)
                if len(colliding_segments) > 0:
                    yield line, colliding_segments, component

    def get_score(self):
        return -len(list(self.find_intersections()))

    def maximize(self):
        bounding_box_extension = self.options["bounding_box_extension"]
        for line, colliding_segments, component in self.find_intersections():
            collision_start_point = colliding_segments[0][0]
            collision_start_point_idx = line.locations.index(collision_start_point) + 1
            collision_exit_point = colliding_segments[-1][-1]
            collision_exit_point_idx = line.locations.index(collision_exit_point)

            collision_avg_y = (collision_start_point.y + collision_exit_point.y) / 2

            edge_segment = (
                (
                    component.bounding_box.ul_corner
                    + Point(-bounding_box_extension, -bounding_box_extension),
                    Point(
                        component.bounding_box.lr_corner.x + bounding_box_extension,
                        component.bounding_box.ul_corner.y - bounding_box_extension,
                    ),
                )
                if collision_avg_y <= component.bounding_box.center.y
                else (
                    Point(
                        component.bounding_box.ul_corner.x - bounding_box_extension,
                        component.bounding_box.lr_corner.y + bounding_box_extension,
                    ),
                    component.bounding_box.lr_corner
                    + Point(bounding_box_extension, bounding_box_extension),
                )
            )

            line.locations = [
                *line.locations[:collision_start_point_idx],
                Point(
                    component.bounding_box.ul_corner.x - bounding_box_extension,
                    collision_start_point.y,
                ),
                *edge_segment,
                Point(
                    component.bounding_box.lr_corner.x + bounding_box_extension,
                    collision_exit_point.y,
                ),
                *line.locations[collision_exit_point_idx:],
            ]


class ComponentsAvoidOthers(Constraint):
    def find_intersections(self):
        res = []
        for component_pair in itertools.combinations(self.output.components, 2):
            if component_pair[0] == component_pair[1]:
                continue
            if component_pair[0].bounding_box.intersects(
                component_pair[1].bounding_box
            ):
                res.append(component_pair)
        return res

    def get_score(self):
        return -len(self.find_intersections())

    def maximize(self):
        while len(intersections := self.find_intersections()) != 0:
            for intersection in intersections:
                if intersection[0].location.y > intersection[1].location.y:
                    intersection[0].location += Point(0, self.options["row_gap"])
                else:
                    intersection[1].location += Point(0, self.options["row_gap"])


class LinesAvoidOthers(Constraint):
    def find_intersections(self):
        self.output.get_line_intersects_line()
        res = []
        for line_bin in self.output.line_bins.values():
            for line_pair in itertools.combinations(line_bin, 2):
                for i, segment_1 in enumerate(line_pair[0].line_segments):
                    segment_1_is_start = i == 0
                    segment_1_is_end = i == len(line_pair[0].line_segments) - 1
                    for segment_2 in line_pair[1].line_segments:
                        segment_2_is_start = i == 0
                        segment_2_is_end = i == len(line_pair[1].line_segments) - 1
                        if (
                            get_segment_slope(segment_1) == get_segment_slope(segment_2)
                            and BoundingBox.from_line_segment(segment_1).intersects(
                                BoundingBox.from_line_segment(segment_2)
                            )
                            and not (
                                segment_1_is_start
                                and segment_2_is_start
                                or segment_1_is_end
                                and segment_2_is_end
                            )
                        ):
                            res.append((*line_pair, segment_1, segment_2))
        return res

    def get_score(self):
        return -len(self.find_intersections())

    def maximize(self):
        for line_1, line_2, segment_1, segment_2 in self.find_intersections():
            if len(line_1.locations) == 2 or len(line_2.locations) == 2:
                continue
            if segment_1[0].y > segment_1[1].y != segment_2[0].y > segment_2[1].y:
                # TODO: handle crossover better when lines are mirror images
                line_1.locations[1] += Point(self.options["min_line_spacing"], 0)
                line_1.locations[2] += Point(self.options["min_line_spacing"], 0)
            elif segment_1[0].y > segment_1[1].y:
                if segment_1[1].y > segment_2[1].y:
                    # segment_2 is on the inside
                    segment_2[0].x += self.options["min_line_spacing"]
                    segment_2[1].x += self.options["min_line_spacing"]
                else:
                    # segment_1 is on the inside
                    segment_1[0].x += self.options["min_line_spacing"]
                    segment_1[1].x += self.options["min_line_spacing"]
            else:
                if segment_1[1].y < segment_2[1].y:
                    # segment_1 is on the inside
                    segment_1[0].x += self.options["min_line_spacing"]
                    segment_1[1].x += self.options["min_line_spacing"]
                else:
                    # segment_2 is on the inside
                    segment_2[0].x += self.options["min_line_spacing"]
                    segment_2[1].x += self.options["min_line_spacing"]
