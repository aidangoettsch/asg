from intermediate_lang import *
from entities import *
from lark import Lark, Transformer, Tree, Token
import os
from grammar import *


class XSchemSymbolTransformer(Transformer):
    """
    Transform the parsed tree to an SExpressionList object. Also handles strings and literals.
    """

    def __init__(self, name):
        super().__init__()
        self.name = name

    def string(self, string: List[Token]) -> str:
        if len(string) > 0:
            return string[0].value
        else:
            return ""

    def literal(self, literal: List[Token]) -> Literal:
        return Literal(literal[0].value)

    def number(self, num: List[Token]) -> float or int:
        if "." in num[0].value:
            return float(num[0].value)
        else:
            return int(num[0].value)

    def value(self, value: List[Token]):
        if type(value[0]) == Token:
            return value[0].value
        else:
            return value[0]

    def key(self, value: List[Token]):
        if type(value[0]) == Token:
            return value[0].value
        else:
            return value[0]

    def key_value_pair(self, pair):
        return tuple(pair)

    def block(self, block: List[Tree or Token]):
        res = []
        for block_member in block:
            if type(block_member) == Tree:
                res += block_member.children
        return res

    def file(self, file: List[Tree]):
        pin_locations = {}
        inputs = []
        outputs = []

        ul_corner = Point(0, 0)
        lr_corner = Point(0, 0)
        for statement in file:
            if type(statement) == Tree:
                if type(statement.children[0]) == Tree:
                    if statement.children[0].data == "pin":
                        body = statement.children[1].children
                        properties = body[-1]
                        properties_dict = {}
                        for prop in properties:
                            if type(prop) == tuple:
                                properties_dict[prop[0].value] = prop[1].value

                        body = body[:-1]
                        pin_corner_1 = Point(body[1], body[2])
                        pin_corner_2 = Point(body[3], body[4])
                        pin_location = Point(
                            pin_corner_1.x
                            if abs(pin_corner_1.x) > abs(pin_corner_2.x)
                            else pin_corner_2.x,
                            (pin_corner_1.y + pin_corner_2.y) / 2,
                        )
                        pin_locations[properties_dict["name"]] = pin_location

                        if properties_dict["dir"] == "in":
                            inputs.append(properties_dict["name"])
                        if properties_dict["dir"] == "out":
                            outputs.append(properties_dict["name"])

                        if pin_location.x < ul_corner.x:
                            ul_corner.x = pin_location.x
                        if pin_location.y < ul_corner.y:
                            ul_corner.y = pin_location.y
                        if pin_location.x > lr_corner.x:
                            lr_corner.x = pin_location.x
                        if pin_location.y > lr_corner.y:
                            lr_corner.y = pin_location.y

        return LibrarySymbol(
            self.name,
            self.name,
            pin_locations,
            inputs,
            outputs,
            SExpressionList("", []),
            [],
            BoundingBox(ul_corner, lr_corner),
        )


def xschem_to_il(library_dir: List[os.DirEntry], options_override: Dict = None):
    """
    Convert a directory of Xschem symbol files to an internal representation
    :param library_dir: A list of directory entries for a directory which contains Xschem symbol files
    :param options_override: Additional options for the parser
    :return: A representation of the library as [LibraryComponent]s
    """
    if options_override is None:
        options_override = {}
    options = {}
    dict.update(options, options_override)

    # Get paths relative to the location of this file, not the root of the module
    script_dir = os.path.dirname(os.path.realpath(__file__))
    res = LibraryIL()
    for file in library_dir:
        if file.is_file() and os.path.splitext(file.path)[-1] == ".sym":
            symbol_name = os.path.splitext(os.path.split(file.path)[-1])[0]
            with open(os.path.join(script_dir, "xschem.lark")) as grammar:
                parser = Lark(
                    grammar.read() + "\n",
                    parser="lalr",
                    transformer=XSchemSymbolTransformer(symbol_name),
                    start="file",
                )
            with open(file.path) as sym_file:
                res.symbols[symbol_name] = parser.parse(sym_file.read())
    return res