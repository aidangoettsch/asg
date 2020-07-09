from intermediate_lang import *
from entities import *
import numpy


def asg_naive(inp, options_override={}):
    options = {
        "starting_x": 10,
        "starting_y": 10,
    }
    dict.update(options, options_override)

    res = OutputIL()
    x = options["starting_x"]
    y = options["starting_y"]

    for component in inp.components:
        component.location = Point(x, y)
        x += 50
        res.components.append(component)

    for connection in inp.connections:
        start_component = inp.components[connection.start_entity]
        end_component = inp.components[connection.end_entity]
        start_pin_location = (
            start_component.location
            + start_component.pin_locations[connection.start_pin]
        )
        end_pin_location = (
            end_component.location + end_component.pin_locations[connection.end_pin]
        )
        res.lines.append(Line(connection, start_pin_location, end_pin_location))

    return res


class LTRSorter:
    def __init__(self, adjacency, inputs):
        self.adjacency = adjacency
        self.cache = {}

        for input_idx in inputs:
            self.cache[input_idx] = 0

    def find_distance_from_input(self, component_idx, seen=[]):
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


def asg_ltr(inp, options_override={}):
    options = {
        "starting_x": 10,
        "starting_y": 10,
        "column_gap": 30,
        "row_gap": 30,
    }
    dict.update(options, options_override)

    res = OutputIL()

    n_components = len(inp.components)
    adjacency = numpy.zeros((n_components, n_components))

    for connection in inp.connections:
        start_i = connection.start_entity
        end_i = connection.end_entity
        adjacency[start_i][end_i] = 1
        adjacency[end_i][start_i] = -1

    ltr_sorter = LTRSorter(
        adjacency, [i for i, e in enumerate(inp.components) if e.inputs == []]
    )
    columns = [
        ltr_sorter.find_distance_from_input(i) for i, e in enumerate(inp.components)
    ]

    starting_x = options["starting_x"]
    y_indicies = [options["starting_y"]] * (max(columns) + 1)
    column_gap = options["column_gap"]
    row_gap = options["row_gap"]

    for component_idx, component in enumerate(inp.components):
        column = columns[component_idx]
        component.location = Point(starting_x + column * column_gap, y_indicies[column])

        y_indicies[column] += row_gap

        res.components.append(component)

    for connection in inp.connections:
        start_component = inp.components[connection.start_entity]
        end_component = inp.components[connection.end_entity]
        start_pin_location = (
            start_component.location
            + start_component.pin_locations[connection.start_pin]
        )
        end_pin_location = (
            end_component.location + end_component.pin_locations[connection.end_pin]
        )
        res.lines.append(Line(connection, start_pin_location, end_pin_location))

    return res
