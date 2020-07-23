from abc import abstractmethod
import numpy
from intermediate_lang import *
from entities import *


class Constraint:
    def __init__(self, output):
        self.output = output

    @abstractmethod
    def get_score(self):
        pass

    @abstractmethod
    def maximize(self):
        pass


class LTRConstraint(Constraint):
    def __init__(self, output, options_override={}):
        super().__init__(output)
        self.options = {
            "starting_x": 20,
            "starting_y": 20,
            "column_gap": 30,
            "row_gap": 30,
        }
        dict.update(self.options, options_override)

        self.inputs = [i for i, e in enumerate(output.components) if e.inputs == []]
        print(self.inputs)

        n_components = len(self.output.components)
        self.adjacency = numpy.zeros((n_components, n_components))

        for connection in self.output.connections:
            print(
                connection.start_entity,
                connection.end_entity,
                connection.start_pin,
                connection.end_pin,
            )
            start_i = connection.start_entity
            end_i = connection.end_entity
            self.adjacency[start_i][end_i] = 1
            self.adjacency[end_i][start_i] = -1
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
            for i, x in enumerate(self.adjacency[component_idx])
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
