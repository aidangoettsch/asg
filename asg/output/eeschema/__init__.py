import uuid
from typing import Tuple

import asg.intermediate_lang as intermediate_lang
import asg.entities as entities
from asg.grammar import *


class SchematicElement(Atom):
    def __init__(self, name, children):
        super().__init__(name, children)


class Schematic(SchematicElement):
    def __init__(self, children, project_name="test", project_uuid=uuid.uuid1()):
        super().__init__(
            "kicad_sch",
            [
                SchematicElement("version", [20200714]),
                SchematicElement("host", ["asg", "0.1.0"]),
                SchematicElement("page", [1, 1]),
                SchematicElement("paper", ["A4"]),
            ]
            + children,
        )


class SchematicWire(SchematicElement):
    def __init__(self, line_segment: Tuple[entities.Point]):
        super().__init__(
            "wire",
            [
                SchematicElement(
                    "pts", [SchematicElement("xy", [p.x, p.y]) for p in line_segment]
                )
            ],
        )


class SchematicComponent(SchematicElement):
    def __init__(self, library_component, component):
        self.uuid = uuid.uuid1()
        children = [
            SchematicElement("lib_id", [library_component.full_name]),
            SchematicElement("at", [component.location.x, component.location.y, 0]),
            *(
                [SchematicElement("mirror", [Literal("x")])]
                if component.mirrored_over_x
                else []
            ),
            SchematicElement("unit", [1]),
            SchematicElement("in_bom", [Literal("yes")]),
            SchematicElement("on_board", [Literal("yes")]),
            SchematicElement("uuid", [str(self.uuid)]),
            *[
                prop.to_s_expression(component.location)
                for prop in library_component.properties
            ],
        ]
        super().__init__("symbol", children)


class SchematicLabel(SchematicElement):
    def __init__(self, name, direction, location):
        super().__init__(
            "global_label",
            [
                name,
                SchematicElement("shape", [Literal(direction)]),
                SchematicElement(
                    "at", [location.x, location.y, 180 if direction == "input" else 0]
                ),
                SchematicElement(
                    "effects",
                    [
                        SchematicElement(
                            "font", [SchematicElement("size", [1.27, 1.27])]
                        ),
                        SchematicElement(
                            "justify",
                            [Literal("right" if direction == "input" else "left")],
                        ),
                    ],
                ),
            ],
        )


def component_to_eeschema(component, library):
    if type(component) == entities.Cell:
        return SchematicComponent(library.symbols[component.human_name], component)
    if type(component) == entities.CircuitInput:
        return SchematicLabel(component.identifier, "input", component.location)
    if type(component) == entities.CircuitOutput:
        return SchematicLabel(component.identifier, "output", component.location)


def il_to_eeschema(
    inp: intermediate_lang.OutputIL, out, library: intermediate_lang.LibraryIL
):
    symbols_used = set(
        library.symbols[component.human_name].raw_data
        for component in inp.components
        if type(component) == entities.Cell
    )
    lib_symbols = SchematicElement("lib_symbols", symbols_used)

    components = [
        component_to_eeschema(component, library) for component in inp.components
    ]
    symbol_instances = SchematicElement(
        "symbol_instances",
        [
            SchematicElement(
                "path",
                [
                    f"/{c.uuid}",
                    SchematicElement("reference", ["U?"]),
                    SchematicElement("unit", [1]),
                ],
            )
            for c in components
            if type(c) == SchematicComponent
        ],
    )

    out.write(
        str(
            Schematic(
                [lib_symbols]
                + [e for e in components if e is not None]
                + [
                    SchematicWire(segment)
                    for line in inp.lines
                    for segment in line.line_segments
                ]
                + [symbol_instances]
            )
        )
    )
