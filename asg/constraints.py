from abc import abstractmethod
import numpy
from intermediate_lang import *
from entities import *
import itertools


def get_segment_slope(segment):
    return (
        (segment[0].y - segment[1].y) / (segment[0].x - segment[1].x)
        if (segment[0].x - segment[1].x) != 0
        else float("inf")
    )


def get_segment_length(segment):
    return (
        ((segment[0].y - segment[1].y) ** 2) + ((segment[0].x - segment[1].x) ** 2)
    ) ** 0.5


class Constraint:
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
            error += component[1].location.y - optimal_y
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
                error += inp.location.y - self.find_optimal_y(i)
        return -error

    def maximize(self):
        for i, inp in enumerate(self.output.components):
            if type(inp) == CircuitInput:
                inp.location.y = self.find_optimal_y(i)


class UntangleConstraint(Constraint):
    @staticmethod
    def point_cross_product(point_1, point_2):
        return point_1.x * point_2.y - point_2.x * point_1.y

    @staticmethod
    def point_loc_relative_to_line(segment, point):
        segment_second_prime = Point(
            segment[1].x - segment[0].x, segment[1].y - segment[0].y
        )
        point_prime = Point(point.x - segment[0].x, point.y - segment[0].y)
        r = UntangleConstraint.point_cross_product(segment_second_prime, point_prime)
        return r if r == 0 else numpy.sign(r)

    @staticmethod
    def a_sandwiches_b(segment_a, segment_b):
        b_0 = UntangleConstraint.point_loc_relative_to_line(segment_b, segment_a[0])
        b_1 = UntangleConstraint.point_loc_relative_to_line(segment_b, segment_a[1])

        return b_0 != b_1 and b_0 != 0 and b_1 != 0

    @staticmethod
    def check_cross(segment_1, segment_2):
        slope_1 = get_segment_slope(segment_1)
        slope_2 = get_segment_slope(segment_2)
        if slope_1 == slope_2:
            return BoundingBox.from_line_segment(segment_1).intersects(
                BoundingBox.from_line_segment(segment_2)
            )

        return UntangleConstraint.a_sandwiches_b(
            segment_1, segment_2
        ) and UntangleConstraint.a_sandwiches_b(segment_2, segment_1)

    def find_crossings(self):
        crossings = []
        for connection_pair in itertools.combinations(self.output.lines, 2):
            line_segments = (
                connection_pair[0].line_segments + connection_pair[1].line_segments
            )

            for segment_pair in itertools.combinations(line_segments, 2):
                if self.check_cross(segment_pair[0], segment_pair[1]):
                    crossings.append(connection_pair)

        return crossings

    def get_score(self):
        crossings = self.find_crossings()
        return -len(crossings)

    def maximize(self):
        for crossing in self.find_crossings():
            prev_score = self.get_score()
            if crossing[0].connection.end_entity == crossing[1].connection.end_entity:
                self.output.components[
                    crossing[0].connection.end_entity
                ].mirror_over_x()
                self.output.repair_lines()
            if prev_score > self.get_score():
                self.output.components[
                    crossing[0].connection.end_entity
                ].mirror_over_x()
                self.output.repair_lines()


class LinesAvoidBoundingBoxes(Constraint):
    def find_intersections(self):
        res = []
        for line in self.output.lines:
            connection = line.connection
            for segment in line.line_segments:
                segment_bounding_box = BoundingBox.from_line_segment(segment)
                for i, component in enumerate(self.output.components):
                    if (
                        component.bounding_box.intersects(segment_bounding_box)
                        and connection.start_entity != i
                        and connection.end_entity != i
                    ):
                        res.append((line, component))
        return res

    def get_score(self):
        return -len(self.find_intersections())

    def maximize(self):
        for intersection in self.find_intersections():
            pass


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
        for intersection in self.find_intersections():
            pass


class LinesAvoidOthers(Constraint):
    def find_intersections(self):
        res = []
        for line_pair in itertools.combinations(self.output.lines, 2):
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
                        res.append(
                            (
                                *line_pair,
                                get_segment_slope(segment_1),
                                get_segment_length(segment_1),
                                get_segment_length(segment_2),
                            )
                        )
        return res

    def get_score(self):
        return -len(self.find_intersections())

    def maximize(self):
        for intersection in self.find_intersections():
            if intersection[2] == 0:
                intersection[0].locations[1] += Point(
                    0, -self.options["min_line_spacing"]
                )
                intersection[0].locations[2] += Point(
                    0, -self.options["min_line_spacing"]
                )
                intersection[1].locations[1] += Point(
                    0, self.options["min_line_spacing"]
                )
                intersection[1].locations[2] += Point(
                    0, self.options["min_line_spacing"]
                )
            elif intersection[3] > intersection[4]:
                intersection[0].locations[1] += Point(
                    -self.options["min_line_spacing"], 0
                )
                intersection[0].locations[2] += Point(
                    -self.options["min_line_spacing"], 0
                )
                intersection[1].locations[1] += Point(
                    self.options["min_line_spacing"], 0
                )
                intersection[1].locations[2] += Point(
                    self.options["min_line_spacing"], 0
                )
            else:
                intersection[0].locations[1] += Point(
                    self.options["min_line_spacing"], 0
                )
                intersection[0].locations[2] += Point(
                    self.options["min_line_spacing"], 0
                )
                intersection[1].locations[1] += Point(
                    -self.options["min_line_spacing"], 0
                )
                intersection[1].locations[2] += Point(
                    -self.options["min_line_spacing"], 0
                )
