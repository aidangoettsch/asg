from intermediate_lang import *
from entities import *
from lark import Lark, Transformer
import os
from s_expression import *


class SExpressionTransformer(Transformer):
    def string(self, string):
        if len(string) > 0:
            return string[0].value
        else:
            return ""

    def literal(self, literal):
        return SExpressionLiteral(literal[0].value)

    def number(self, num):
        if "." in num[0].value:
            return float(num[0].value)
        else:
            return int(num[0].value)

    def list(self, l):
        return SExpressionList(l[0], l[1:])


def symbol_to_il(symbol):
    name = ""
    pin_locations = {}
    inputs = []
    outputs = []
    properties = []
    for prop in symbol.children:
        if type(prop) != SExpressionList:
            continue
        if prop.name == "property":
            property_key = prop.children[0]
            property_value = prop.children[1]
            property_id = -1
            property_location = [0, 0, 0]
            property_effects = []

            for c in prop.children:
                if type(c) != SExpressionList:
                    continue
                if c.name == "id":
                    property_id = c.children[0]
                if c.name == "at":
                    property_location = c.children
                if c.name == "effects":
                    property_effects = c.children
            properties.append(
                LibraryProperty(
                    property_key,
                    property_value,
                    property_id,
                    property_location,
                    property_effects,
                )
            )
        if "Value" in prop.children:
            name = prop.children[1]
        if prop.name == "symbol":
            for element in prop.children:
                if type(element) != SExpressionList:
                    continue
                if element.name == "pin":
                    pin_idx = -1
                    pin_location = Point(0, 0)
                    pin_type = element.children[0]
                    for attr in element.children:
                        if type(attr) != SExpressionList:
                            continue
                        if attr.name == "at":
                            pin_location = Point(attr.children[0], -attr.children[1])
                        if attr.name == "number":
                            pin_idx = int(attr.children[0])
                    if pin_type == "input":
                        inputs.append(pin_idx)
                    else:
                        outputs.append(pin_idx)
                    pin_locations[pin_idx] = pin_location
    if name == "":
        raise Exception(f"Invalid symbol {symbol.children[0]}")
    return LibraryComponent(
        name, symbol.children[0], pin_locations, inputs, outputs, symbol, properties
    )


def s_expression_to_il(library_file, options_override={}):
    options = {
        "gate_level": True,
    }
    dict.update(options, options_override)

    # Get paths relative to the location of this file, not the root of the module
    script_dir = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(script_dir, "s_expression.lark")) as grammar:
        parser = Lark(
            grammar.read() + "\n",
            parser="lalr",
            transformer=SExpressionTransformer(),
            start="list",
        )
    parsed = parser.parse(library_file.read())

    symbols = [child for child in parsed.children if child.name == "symbol"]
    res = LibraryIL()
    for symbol in symbols:
        symbol_il = symbol_to_il(symbol)
        res.symbols[symbol_il.name] = symbol_il
    return res
