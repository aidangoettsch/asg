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
        self.entity = self.to_entity()

    def to_entity(self):
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
    def __init__(self, identifier, inouts, params):
        cell_fullname = inouts[-1]
        inouts = inouts[:-1]
        self.cell_fullname = cell_fullname
        super().__init__(identifier, inouts, params)

    def __str__(self):
        return f"Cell {self.cell_fullname} connected to {', '.join(self.inouts)} with {str(self.params)}"

    def to_entity(self):
        return Cell(self.cell_fullname)


class SPICEResistor(SPICEComponent):
    def __init__(self, identifier, inouts, params):
        resistance_ohms = inouts[-1]
        inouts = inouts[:-1]
        self.resistance_ohms = resistance_ohms
        super().__init__(identifier, inouts, params)

    def __str__(self):
        return f"Resistor {self.resistance_ohms}Ω connected to {', '.join(self.inouts)} with {str(self.params)}"

    def to_entity(self):
        return Resistor(self.resistance_ohms)


class SPICESubcircuit:
    def __init__(self, name, inouts, components):
        self.name = name
        self.inouts = inouts
        self.components = components

    def __str__(self):
        children = "\n\t".join(str(x) for x in self.components)
        return f"{self.name} {', '.join(self.inouts)}\n\t{children}"


class SPICETransformer(Transformer):
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
        return SPICESubcircuit(
            subcircuit[0]["name"], subcircuit[0]["inouts"], subcircuit[1:-1]
        )

    def component(self, component: list):
        component_types = {
            "mosfet_pf": SPICEMosfet,
            "subcircuit_pf": SPICECell,
            "resistor_pf": SPICEResistor,
        }

        inouts = []
        params = []
        for option in component[2:]:
            if type(option) == str:
                inouts.append(option)
            else:
                params.append(option)
        return component_types[component[0].data](component[1], inouts, dict(params))


def spice_to_il(input_file, subcircuit, options_override={}) -> InputIL:
    options = {
        "gate_level": True,
    }
    dict.update(options, options_override)

    # Get paths relative to the location of this file, not the root of the module
    script_dir = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(script_dir, "spice.lark")) as grammar:
        parser = Lark(
            grammar.read() + "\n", parser="lalr", transformer=SPICETransformer()
        )
    parsed = parser.parse(input_file.read())

    for statement in parsed.children:
        if isinstance(statement, SPICESubcircuit) and statement.name == subcircuit:
            components = statement.components

            nets = {}

            for i, component in enumerate(components):
                for j, inout in enumerate(component.inouts):
                    # Ignore pins that aren't I/O to remove Vdd and GND from the schematic
                    if j in component.entity.inputs or j in component.entity.outputs:
                        nets.setdefault(inout, []).append((i, j))

            connections = []
            for net in nets.values():
                connections += [
                    Connection(*src, *dest)
                    for src, dest in itertools.product(net, repeat=2)
                    if src != dest
                ]
            return InputIL([component.entity for component in components], connections)

    print(
        "Error parsing SPICE file. Make sure a subcircuit with the same name as the file is present."
    )
    sys.exit(-1)
