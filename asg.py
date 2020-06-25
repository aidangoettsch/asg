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
        start_pin_location = start_component.location + start_component.pin_locations[connection.start_pin]
        end_pin_location = end_component.location + end_component.pin_locations[connection.end_pin]
        res.lines.append(Line(connection, start_pin_location, end_pin_location))

    return res


def asg_ltr(inp, options_override={}):
    options = {
        "starting_x": 10,
        "starting_y": 10,
    }
    dict.update(options, options_override)

    res = OutputIL()
    x = options["starting_x"]
    y = options["starting_y"]

    max_pins = max([component.pin_count for component in inp.components])
    n_components = len(inp.components)
    matrix_size = max_pins * n_components

    adjacency = numpy.zeros((matrix_size, matrix_size))

    for connection in inp.connections:
        start_i = connection.start_entity * max_pins + connection.start_pin
        end_i = connection.end_entity * max_pins + connection.end_pin
        adjacency[start_i][end_i] = 1
        adjacency[end_i][start_i] = -1

    print(adjacency)
    exclude_rows = []
    for i, row in enumerate(adjacency):
        if len(numpy.where(row == 0)[0]) == len(row):
            exclude_rows.append(i)

    distance = adjacency
    print(exclude_rows)
    while len(set(numpy.where(adjacency == 0)[0])) > len(exclude_rows):
        distance *= distance
        print(distance)

    for connection in inp.connections:
        start_component = inp.components[connection.start_entity]
        end_component = inp.components[connection.end_entity]
        start_pin_location = start_component.location + start_component.pin_locations[connection.start_pin]
        end_pin_location = end_component.location + end_component.pin_locations[connection.end_pin]
        res.lines.append(Line(connection, start_pin_location, end_pin_location))

    return res
