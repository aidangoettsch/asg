from abc import abstractmethod

from intermediate_lang import *
from entities import *
from lark import Lark, Transformer
import os
import itertools
import sys


class SPICEComponent:
    def __init__(self, identifier, inouts, params):
        self.identifier = identifier
        self.inouts = inouts
        self.params = params

    @property
    @abstractmethod
    def entity(self) -> Component:
        pass


class SPICEMosfet(SPICEComponent):
    def __init__(self, identifier, inouts, params):
        fet_type = inouts[-1]
        inouts = inouts[:-1]
        super().__init__(identifier, inouts, params)
        self.fet_type = fet_type

    def __str__(self):
        return f"MOSFET connected to {', '.join(self.inouts)} with {str(self.params)}"


class SPICECell(SPICEComponent):
    def __init__(self, identifier, inouts, params, cell_configs):
        cell_fullname = inouts[-1]
        inouts = inouts[:-1]
        self.cell_fullname = cell_fullname
        super().__init__(identifier, inouts, params)
        self.cell_config = cell_configs[cell_fullname]

    def __str__(self):
        return f"Cell {self.cell_fullname} connected to {', '.join(self.inouts)} with {str(self.params)}"

    @property
    def entity(self) -> Component:
        return Cell(self.cell_config)


class SPICEResistor(SPICEComponent):
    def __init__(self, identifier, inouts, params):
        resistance_ohms = inouts[-1]
        inouts = inouts[:-1]
        self.resistance_ohms = resistance_ohms
        super().__init__(identifier, inouts, params)

    def __str__(self):
        return f"Resistor {self.resistance_ohms}Ω connected to {', '.join(self.inouts)} with {str(self.params)}"

    @property
    def entity(self) -> Component:
        return Resistor(self.resistance_ohms)


class SPICEDiode(SPICEComponent):
    def __init__(self, identifier, inouts, params):
        model = inouts[-1]
        inouts = inouts[:-1]
        self.model = model
        super().__init__(identifier, inouts, params)

    def __str__(self):
        return f"Diode model ${self.model} connected to {', '.join(self.inouts)} with {str(self.params)}"

    @property
    def entity(self) -> Component:
        return Diode(self.model)


class SPICEInout(SPICEComponent):
    def __init__(self, identifier):
        super().__init__(identifier, [identifier], [])
        self.type = None

    def __str__(self):
        return f"{self.type if self.type is not None else 'Inout'} {self.identifier} connected to {', '.join(self.inouts)} with {str(self.params)}"

    @property
    def entity(self) -> Component:
        if self.type == "Input":
            return CircuitInput(self.identifier)
        elif self.type == "Output":
            return CircuitOutput(self.identifier)
        return CircuitInout(self.identifier)


class SPICESubcircuit:
    def __init__(self, name, inouts, components):
        self.name = name
        self.inouts = inouts
        self.components = components + [
            SPICEInout(identifier) for identifier in self.inouts
        ]

    def __str__(self):
        children = "\n\t".join(str(x) for x in self.components)
        return f"{self.name} {', '.join(self.inouts)}\n\t{children}"


def spice_cell_factory(cell_configs):
    return lambda identifier, inouts, params: SPICECell(
        identifier, inouts, params, cell_configs
    )


class SPICETransformer(Transformer):
    def __init__(self, cell_configs, fill_subcircuits):
        super().__init__()
        self.cell_configs = cell_configs
        self.fill_subcircuits = fill_subcircuits
        for fill_subcircuit in fill_subcircuits:
            self.cell_configs[fill_subcircuit] = LibraryComponent(
                fill_subcircuit,
                fill_subcircuit,
                [],
                [],
                [],
                SExpressionList("", []),
                [],
                BoundingBox(Point(0, 0), Point(0, 0)),
            )

    def parameter(self, parameter):
        return parameter[0].value

    def component_name(self, component_name):
        return component_name[0].value

    def kv_option(self, kv_option):
        return (kv_option[0].value, kv_option[1].value)

    def subcircuit_start_command(self, start_cmd):
        return {
            "name": start_cmd[0],
            "inouts": start_cmd[1:],
        }

    def subcircuit(self, subcircuit):
        components = subcircuit[1:-1]
        components = filter(
            lambda component: type(component) != SPICECell
            or component.cell_fullname not in self.fill_subcircuits,
            components,
        )
        return SPICESubcircuit(
            subcircuit[0]["name"], subcircuit[0]["inouts"], list(components)
        )

    def component(self, component: list):
        component_types = {
            "mosfet_pf": SPICEMosfet,
            "subcircuit_pf": spice_cell_factory(self.cell_configs),
            "resistor_pf": SPICEResistor,
            "diode_pf": SPICEDiode,
        }

        inouts = []
        params = []
        for option in component[2:]:
            if type(option) == str:
                inouts.append(option)
            else:
                params.append(option)
        return component_types[component[0].data](component[1], inouts, dict(params))


def spice_to_il(input_file, subcircuit, library, options_override={}) -> InputIL:
    options = {
        "gate_level": True,
        "filter_power": ["vdd", "gnd"],
        "fill_subcircuit": ["FILL"],
    }
    dict.update(options, options_override)

    # Get paths relative to the location of this file, not the root of the module
    script_dir = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(script_dir, "spice.lark")) as grammar:
        parser = Lark(
            grammar.read() + "\n",
            parser="lalr",
            transformer=SPICETransformer(library.symbols, options["fill_subcircuit"]),
        )
    parsed = parser.parse(input_file.read())

    for statement in parsed.children:
        if isinstance(statement, SPICESubcircuit) and statement.name == subcircuit:
            components = list(
                filter(
                    lambda c: c.identifier not in options["filter_power"],
                    statement.components,
                )
            )

            nets = {}

            for i, component in enumerate(components):
                for j, inout in enumerate(component.inouts):
                    # Ignore pins that aren't I/O to remove Vdd and GND from the schematic
                    if (
                        isinstance(component, SPICEInout)
                        or j in component.entity.inputs
                        or j in component.entity.outputs
                    ):
                        nets.setdefault(inout, []).append((i, j))

            connections = []
            for net in nets.values():
                for src, dest in itertools.combinations(net, 2):
                    if not (
                        isinstance(components[src[0]], SPICEInout)
                        or isinstance(components[dest[0]], SPICEInout)
                    ):
                        if (
                            src[1] in components[src[0]].entity.inputs
                            and dest[1] in components[dest[0]].entity.inputs
                        ):
                            continue
                        if (
                            src[1] in components[src[0]].entity.outputs
                            and dest[1] in components[dest[0]].entity.outputs
                        ):
                            continue
                    if src[1] in components[src[0]].entity.inputs:
                        connections.append(Connection(*dest, *src))
                    else:
                        connections.append(Connection(*src, *dest))

            for connection in connections:
                component_start = components[connection.start_entity]
                component_end = components[connection.end_entity]
                if isinstance(component_start, SPICEInout) or isinstance(
                    component_end, SPICEInout
                ):
                    if (
                        not isinstance(component_start, SPICEInout)
                        and connection.start_pin in component_start.entity.inputs
                    ):
                        component_end.type = "Input"
                    if (
                        not isinstance(component_end, SPICEInout)
                        and connection.end_pin in component_end.entity.inputs
                    ):
                        component_start.type = "Input"
                    if (
                        not isinstance(component_start, SPICEInout)
                        and connection.start_pin in component_start.entity.outputs
                    ):
                        component_end.type = "Output"
                    if (
                        not isinstance(component_end, SPICEInout)
                        and connection.end_pin in component_end.entity.outputs
                    ):
                        component_start.type = "Output"
            return InputIL([component.entity for component in components], connections)

    print(
        "Error parsing SPICE file. Make sure a subcircuit with the same name as the file is present."
    )
    sys.exit(-1)
