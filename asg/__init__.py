import asg.output as output
import asg.input
import asg.intermediate_lang as intermediate_lang
import asg.library_source as library_source
import asg.generation as generation

import argparse
import os
import sys


def main():
    # Collect arguments from CLI
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", metavar="input")
    parser.add_argument("library_file", metavar="library")
    parser.add_argument(
        "-f", "--format", help="output format - one of xschem, eeschema", type=str
    )
    parser.add_argument(
        "-d", "--depth", help="depth to unpack subcircuits", default=0, type=str
    )
    parser.add_argument("--vcc", help="vcc net name", default="vcc", type=str)
    parser.add_argument("--vss", help="vss net name", default="gnd", type=str)
    parser.add_argument(
        "-l",
        "--include-library-name",
        dest="include_library_name",
        action="store_true",
        help="include the library name in xschem output. "
        "should be used if xschem library env var is "
        "a directory instead of a list",
    )
    parser.add_argument(
        "-e",
        "--no-embed-symbols",
        dest="embed_symbols",
        action="store_false",
        help="don't embed symbols in xschem schematic output",
    )
    parser.add_argument(
        "-D",
        "--debug",
        help="output intermediate steps of the ASG to ./out/",
        dest="debug",
        action="store_true",
    )
    args = parser.parse_args()

    options = {
        "asg": {},
        "input": {"depth": args.depth, "filter_power": [args.vcc, args.vss]},
        "output": {
            "include_library_name": args.include_library_name,
            "vcc_pin": args.vcc,
            "vss_pin": args.vss,
            "embed_symbols": args.embed_symbols,
        },
    }

    if args.format is None:
        args.format = "xschem"
    if args.format == "eeschema":
        with open(args.library_file) as inf:
            library = library_source.kicad_symbol_lib.s_expression_to_il(inf)
        options["asg"] = {
            "starting_x": 25.4,
            "starting_y": 25.4,
            "column_gap": 25.4,
            "row_gap": 25.4,
            "min_line_spacing": 1.27,
            "bounding_box_extension": 0.127,
        }
    elif args.format == "xschem":
        library = library_source.xschem.xschem_to_il(os.scandir(args.library_file))

    # Detect input file format and read into IL
    root, ext = os.path.splitext(os.path.basename(args.input_file))
    if ext == ".spc":
        with open(args.input_file) as inf:
            inp = asg.input.spice_to_il(inf, root, library, options["input"])
    else:
        print(f"Unsupported filetype {ext}")
        sys.exit(-1)

    # Run the ASG on input data
    res, history = generation.constraint_asg(inp)

    # Output schematic
    if args.format == "json":
        with open("output.json", "w+") as out:
            output.il_to_json(res, out)
    elif args.format == "md":
        with open("output.md", "w+") as out:
            output.il_to_markdown(res, out)
    elif args.format == "eeschema":
        with open("output.kicad_sch", "w+") as out:
            output.il_to_eeschema(res, out, library)
    elif args.format == "xschem":
        with open("output.sch", "w+") as out:
            library_file = (
                args.library_file[:-1]
                if args.library_file[-1] == "/"
                else args.library_file
            )
            output.il_to_xschem(
                res, out, os.path.basename(library_file), options["output"]
            )
    else:
        print(f"Unknown output type {args.format}")

    # Output intermediate steps if debug is enabled
    if args.debug:
        if not os.path.isdir("out"):
            os.mkdir("out")
        for i, e in enumerate(history):
            if args.format == "json":
                with open(f"out/{i}_{type(e[0]).__name__}_{e[1]}.json", "w+") as out:
                    output.il_to_json(e[2], out)
            elif args.format == "md":
                with open(f"out/{i}_{type(e[0]).__name__}_{e[1]}.md", "w+") as out:
                    output.il_to_markdown(e[2], out)
            elif args.format == "eeschema":
                with open(
                    f"out/{i}_{type(e[0]).__name__}_{e[1]}.kicad_sch", "w+"
                ) as out:
                    output.il_to_eeschema(e[2], out, library)
            elif args.format == "xschem":
                with open(f"out/{i}_{type(e[0]).__name__}_{e[1]}.sch", "w+") as out:
                    output.il_to_xschem(
                        e[2], out, os.path.basename(library_file), options["output"]
                    )
