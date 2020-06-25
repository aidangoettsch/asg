import asg
from intermediate_lang import *
import output.json
import output.xcircuit_ps
import output.text


def main():
    inp = InputIL()
    res = asg.asg_naive(inp)
    # res = asg.asg_ltr(inp)
    with open("output.json", "w+") as out:
        output.json.il_to_json(res, out)
    with open("output.ps", "w+") as out:
        output.xcircuit_ps.il_to_postscript(res, out)
    with open("output.md", "w+") as out:
        output.text.il_to_markdown(res, out)


if __name__ == "__main__":
    main()
