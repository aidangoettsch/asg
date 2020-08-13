import asg
import output.json
import output.xcircuit_ps
import output.text
import output.eeschema
import input.spice
import library_source.kicad_symbol_lib
import argparse
import os
import sys
import inspect
import shutil

# Add this directory to python path so that we can import from submodules
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0, current_dir)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", metavar="input")
    parser.add_argument("library_file", metavar="library")
    parser.add_argument("-f", "--format", help="output format", type=str)
    args = parser.parse_args()
    with open(args.library_file) as inf:
        library = library_source.kicad_symbol_lib.s_expression_to_il(inf)

    root, ext = os.path.splitext(os.path.basename(args.input_file))
    if ext == ".spc":
        with open(args.input_file) as inf:
            inp = input.spice.spice_to_il(inf, root, library)
    else:
        print(f"Unsupported filetype {ext}")
        sys.exit(-1)
    res, history = asg.constraint_asg(inp)
    if args.format is None:
        args.format = "eeschema"
    if args.format == "json":
        with open("output.json", "w+") as out:
            output.json.il_to_json(res, out)
    elif args.format == "md":
        with open("output.md", "w+") as out:
            output.text.il_to_markdown(res, out)
    elif args.format == "eeschema":
        with open("output.kicad_sch", "w+") as out:
            output.eeschema.il_to_eeschema(res, out, library)

        shutil.rmtree("out")
        os.mkdir("out")
        for i, e in enumerate(history):
            with open(f"out/{i}_{type(e[0]).__name__}_{e[1]}.kicad_sch", "w+") as out:
                output.eeschema.il_to_eeschema(e[2], out, library)
    else:
        print(f"Unknown output type {args.format}")


if __name__ == "__main__":
    main()
