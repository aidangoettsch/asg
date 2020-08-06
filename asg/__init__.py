from asg.constraints import *
from intermediate_lang import *
from entities import *
import numpy

constraint_weights = {
    LTRConstraint: 10,
    VerticalSortConstraint: 10,
    InputYDegridConstraint: 10,
    CreateLinesConstraint: 10,
    UntangleConstraint: 10,
}


def constraint_asg(inp):
    res = OutputIL()

    for component_idx, component in enumerate(inp.components):
        component.location = Point(0, 0)
        res.components.append(component)

    res.connections = inp.connections

    n_components = len(res.components)
    res.adjacency = numpy.zeros((n_components, n_components))

    for connection in res.connections:
        start_i = connection.start_entity
        end_i = connection.end_entity
        res.adjacency[start_i][end_i] = 1
        res.adjacency[end_i][start_i] = -1

    score = 0
    for constraint_type in constraint_weights:
        constraint = constraint_type(res)
        constraint.maximize()
        score += constraint_weights[constraint_type] * constraint.get_score()

    return res
