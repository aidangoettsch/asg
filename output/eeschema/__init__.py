import uuid
import intermediate_lang
import entities
from s_expression import *


class SchematicElement(SExpressionList):
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
    def __init__(self, line: entities.Line):
        super().__init__(
            "wire",
            [
                SchematicElement(
                    "pts", [SchematicElement("xy", [p.x, p.y]) for p in line.locations]
                )
            ],
        )


class SchematicComponent(SchematicElement):
    def __init__(self, library_component, location):
        self.uuid = uuid.uuid1()
        children = [
            SchematicElement("lib_id", [library_component.full_name]),
            SchematicElement("at", [location.x, location.y, 0]),
            SchematicElement("unit", [1]),
            SchematicElement("in_bom", [SExpressionLiteral("yes")]),
            SchematicElement("on_board", [SExpressionLiteral("yes")]),
            SchematicElement("uuid", [str(self.uuid)]),
        ]
        super().__init__("symbol", children + library_component.properties)


def il_to_eeschema(
    inp: intermediate_lang.OutputIL, out, library: intermediate_lang.LibraryIL
):
    symbols_used = set(
        library.symbols[component.human_name].s_expression
        for component in inp.components
        if type(component) == entities.Cell
    )
    lib_symbols = SchematicElement("lib_symbols", symbols_used)

    components = [
        SchematicComponent(library.symbols[component.human_name], component.location)
        for component in inp.components
        if type(component) == entities.Cell
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
        ],
    )

    out.write(
        str(
            Schematic(
                [lib_symbols]
                + components
                + [SchematicWire(line) for line in inp.lines]
                + [symbol_instances]
            )
        )
    )
