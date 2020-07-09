import asg
from intermediate_lang import *
import output.json
import output.xcircuit_ps
import output.text
import input.spice
import argparse
import os
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", metavar="input")
    args = parser.parse_args()

    root, ext = os.path.splitext(os.path.basename(args.input_file))
    if ext == ".spc":
        with open(args.input_file) as inf:
            inp = input.spice.spice_to_il(inf, root)
    else:
        print(f"Unsupported filetype {ext}")
        sys.exit(-1)
    # res = asg.asg_naive(inp)
    res = asg.asg_ltr(inp)
    with open("output.json", "w+") as out:
        output.json.il_to_json(res, out)
    with open("output.ps", "w+") as out:
        output.xcircuit_ps.il_to_postscript(res, out)
    with open("output.md", "w+") as out:
        output.text.il_to_markdown(res, out)


if __name__ == "__main__":
    main()
