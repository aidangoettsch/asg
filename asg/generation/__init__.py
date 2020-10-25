from .constraints import *
from asg.intermediate_lang import *
from asg.entities import *
import numpy
import copy

constraint_weights = {
    LTRConstraint: 10,
    VerticalSortConstraint: 0,
    InputYDegridConstraint: 10,
    UntangleConstraint: 10,
    LinesAvoidOthers: 20,
    LinesAvoidBoundingBoxes: 20,
    ComponentsAvoidOthers: 100,
}


def calculate_score(constraint_instances):
    constraint_scores = [
        (
            type(constraint),
            constraint_weights[type(constraint)] * constraint.get_score(),
        )
        for constraint in constraint_instances
    ]
    return sum([score[1] for score in constraint_scores]), constraint_scores


def constraint_asg(inp, options_override=None):
    if options_override is None:
        options_override = {}

    options = {
        "starting_x": 250,
        "starting_y": 250,
        "column_gap": 250,
        "row_gap": 250,
        "min_line_spacing": 20,
        "bounding_box_extension": 30,
        "bin_size": 100,
        "epsilon": 0.1,
        "distance_from_peak": 10,
    }
    dict.update(options, options_override)

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

    constraint_instances = [
        constraint_type(res, options) for constraint_type in constraint_weights
    ]
    score_history = []
    distance_from_peak = 0
    distance_from_actual_peak = 0
    i = 0
    constraint_instances[0].maximize()
    res.repair_lines()
    res.create_line_bins(options["bin_size"])
    peak_score, peak_score_breakdown = calculate_score(constraint_instances)
    # for constraint in peak_score_breakdown:
    #     print(constraint[0].__name__, constraint[1])
    while distance_from_peak < options["distance_from_peak"]:
        constraint = constraint_instances[(i % (len(constraint_instances) - 1)) + 1]
        constraint.maximize()
        res.repair_lines()
        res.create_line_bins(options["bin_size"])
        score, score_breakdown = calculate_score(constraint_instances)
        if score - peak_score > options["epsilon"]:
            peak_score = score
            distance_from_peak = 1
            distance_from_actual_peak = 1
        elif score >= peak_score:
            distance_from_peak += 1
            distance_from_actual_peak = 1
        else:
            distance_from_peak += 1
            distance_from_actual_peak += 1
        print("Applied:", type(constraint).__name__, score)
        for e in score_breakdown:
            print(e[0].__name__, e[1])
        score_history.append((constraint, score, copy.deepcopy(res)))
        i += 1
    res = score_history[-distance_from_actual_peak]
    best_score = res[1]
    # print("Best:", type(res[0]).__name__, res[1])
    res = res[2]

    return res, score_history, best_score
