from intermediate_lang import *
from entities import *
from lark import Lark, Transformer, Tree
import os


class SPICEComponent:
    def __init__(self, inouts, params):
        self.inouts = inouts
        self.params = params


class SPICEMosfet(SPICEComponent):
    def __init__(self, inouts, params):
        fet_type = inouts[-1]
        inouts = inouts[:-1]
        super().__init__(inouts, params)
        self.fet_type = fet_type


class SPICEGate(SPICEComponent):
    def __init__(self, inouts, params):
        gate_fullname = inouts[-1]
        inouts = inouts[:-1]
        super().__init__(inouts, params)
        self.gate_fullname = gate_fullname


class SPICESubcircuit:
    def __init__(self, name: str, components: list):
        self.name = name
        self.components = components


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
            "pins": start_cmd[1:],
        }

    def subcircuit(self, subcircuit):
        return SPICESubcircuit(subcircuit[0]["name"], subcircuit)

    def component(self, component: list):
        component_types = {
            "mosfet_pf": SPICEMosfet,
            "subcircuit_pf": SPICEGate
        }

        inouts = []
        params = []
        for option in component[1:]:
            if type(option) == str:
                inouts.append(option)
            else:
                params.append(option)
        component_types[component[0].data](inouts, dict(params))


def spice_to_il(input_file, subircuit, options_override={}) -> InputIL:
    options = {
        "gate_level": True,
    }
    dict.update(options, options_override)

    # Get paths relative to the location of this file, not the root of the module
    script_dir = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(script_dir, "spice.lark")) as grammar:
        parser = Lark(grammar.read() + "\n")
    parsed = parser.parse(input_file.read())
    SPICETransformer().transform(parsed)

    return InputIL()
