from asg.constraints import LTRConstraint
from intermediate_lang import *
from entities import *

constraint_weights = {
    LTRConstraint: 10,
}


def constraint_asg(inp):
    res = OutputIL()

    for component_idx, component in enumerate(inp.components):
        component.location = Point(0, 0)
        res.components.append(component)

    res.connections = inp.connections

    score = 0
    for constraint_type in constraint_weights:
        constraint = constraint_type(res)
        constraint.maximize()
        score += constraint_weights[constraint_type] * constraint.get_score()

    for connection in res.connections:
        start_component = res.components[connection.start_entity]
        end_component = res.components[connection.end_entity]
        start_pin_location = (
            start_component.location
            + start_component.pin_locations[connection.start_pin]
        )
        end_pin_location = (
            end_component.location + end_component.pin_locations[connection.end_pin]
        )
        res.lines.append(Line(connection, start_pin_location, end_pin_location))
    return res
