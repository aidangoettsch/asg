import os


def il_to_postscript(output_il, output_file):
    # Get paths relative to the location of this file, not the root of the module
    script_dir = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(script_dir, "header.ps")) as header:
        header_text = header.read().format("title", "day", 1, 200, 200)
        output_file.write(header_text + "\n")
    with open(os.path.join(script_dir, "xcircps2.pro")) as prolog:
        prolog_text = prolog.read()
        output_file.write(prolog_text + "\n")
    with open(os.path.join(script_dir, "trailer.ps")) as trailer:
        trailer_text = trailer.read().format("title", "day", 1, 200, 200)
        output_file.write(trailer_text + "\n")
