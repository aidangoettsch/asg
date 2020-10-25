from asg.intermediate_lang import *
from asg.entities import *
from lark import Lark, Transformer
import os
from asg.grammar import *


class SExpressionTransformer(Transformer):
    """
    Transform the parsed tree to an SExpressionList object. Also handles strings and literals.
    """

    def string(self, string):
        if len(string) > 0:
            return string[0].value
        else:
            return ""

    def literal(self, literal):
        return Literal(literal[0].value)

    def number(self, num):
        if "." in num[0].value:
            return float(num[0].value)
        else:
            return int(num[0].value)

    def list(self, l):
        return Atom(l[0], l[1:])


def symbol_to_il(symbol):
    name = ""
    pin_locations = {}
    inputs = []
    outputs = []
    properties = []

    ul_corner = Point(0, 0)
    lr_corner = Point(0, 0)

    for prop in symbol.children:
        if type(prop) != Atom:
            continue
        if prop.name == "property":
            property_key = prop.children[0]
            property_value = prop.children[1]
            property_id = -1
            property_location = [0, 0, 0]
            property_effects = []

            for c in prop.children:
                if type(c) != Atom:
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
                if type(element) != Atom:
                    continue
                if element.name == "pin":
                    pin_name = -1
                    pin_location = Point(0, 0)

                    pin_type = element.children[0]
                    for attr in element.children:
                        if type(attr) != Atom:
                            continue
                        if attr.name == "at":
                            pin_location = Point(attr.children[0], -attr.children[1])
                        if attr.name == "name":
                            pin_name = attr.children[0]
                    if pin_type == "input":
                        inputs.append(pin_name)
                    else:
                        outputs.append(pin_name)

                    if pin_location.x < ul_corner.x:
                        ul_corner.x = pin_location.x
                    if pin_location.y < ul_corner.y:
                        ul_corner.y = pin_location.y
                    if pin_location.x > lr_corner.x:
                        lr_corner.x = pin_location.x
                    if pin_location.y > lr_corner.y:
                        lr_corner.y = pin_location.y
                    pin_locations[pin_name] = pin_location
    if name == "":
        raise Exception(f"Invalid symbol {symbol.children[0]}")
    bounding_box = BoundingBox(ul_corner, lr_corner)
    bounding_box.expand(2, 0.1)
    return LibrarySymbol(
        name,
        symbol.children[0],
        pin_locations,
        inputs,
        outputs,
        symbol,
        properties,
        bounding_box,
    )


def s_expression_to_il(library_file):
    """
    Convert an s-expression file to an internal representation
    :param library_file: A file descriptor
    :return:
    """

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
