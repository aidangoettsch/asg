import asg
import output.json
import output.xcircuit_ps
import output.text
import output.eeschema
import input.spice
import library_source.kicad_symbol_lib
import library_source.xschem
import argparse
import os
import sys
import inspect
import shutil

# Add this directory to python path so that we can import from submodules
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0, current_dir)


def main():
    # Collect arguments from CLI
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", metavar="input")
    parser.add_argument("library_file", metavar="library")
    parser.add_argument("-f", "--format", help="output format", type=str)
    parser.add_argument(
        "-d", "--debug", help="output intermediate steps of the ASG to ./out/", type=str
    )
    args = parser.parse_args()

    if args.format is None:
        args.format = "xschem"
    if args.format == "eeschema":
        with open(args.library_file) as inf:
            library = library_source.kicad_symbol_lib.s_expression_to_il(inf)
    elif args.format == "xschem":
        library = library_source.xschem.xschem_to_il(os.scandir(args.library_file))

    # Detect input file format and read into IL
    root, ext = os.path.splitext(os.path.basename(args.input_file))
    if ext == ".spc":
        with open(args.input_file) as inf:
            inp = input.spice.spice_to_il(inf, root, library)
    else:
        print(f"Unsupported filetype {ext}")
        sys.exit(-1)

    # Run the ASG on input data
    res, history = asg.constraint_asg(inp)

    # Output schematic
    if args.format == "json":
        with open("output.json", "w+") as out:
            output.json.il_to_json(res, out)
    elif args.format == "md":
        with open("output.md", "w+") as out:
            output.text.il_to_markdown(res, out)
    elif args.format == "eeschema":
        with open("output.kicad_sch", "w+") as out:
            output.eeschema.il_to_eeschema(res, out, library)
    elif args.format == "xschem":
        with open("output.sch", "w+") as out:
            pass

    # Output intermediate steps if debug is enabled
    if args.debug:
        if not os.path.isdir("out"):
            os.mkdir("out")
        for i, e in enumerate(history):
            if args.format == "json":
                with open(f"out/{i}_{type(e[0]).__name__}_{e[1]}.json", "w+") as out:
                    output.json.il_to_json(e[2], out)
            elif args.format == "md":
                with open(f"out/{i}_{type(e[0]).__name__}_{e[1]}.md", "w+") as out:
                    output.text.il_to_markdown(e[2], out)
            elif args.format == "eeschema":
                with open(
                    f"out/{i}_{type(e[0]).__name__}_{e[1]}.kicad_sch", "w+"
                ) as out:
                    output.eeschema.il_to_eeschema(e[2], out, library)
            elif args.format == "xschem":
                with open(f"out/{i}_{type(e[0]).__name__}_{e[1]}.sch", "w+") as out:
                    pass
    else:
        print(f"Unknown output type {args.format}")


if __name__ == "__main__":
    main()
