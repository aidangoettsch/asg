import asg.intermediate_lang as intermediate_lang
import asg.entities as entities


def round_to_nearest(n, to=10):
    return to * round(n / to)


def escape(s):
    forbidden = ["{", "}", "\\"]
    for c in forbidden:
        s = s.replace(c, f"\\{c}")
    return s


def il_to_xschem(
    inp: intermediate_lang.OutputIL, out, library_name: str, options_override=None
):
    if options_override is None:
        options_override = {}
    options = {
        "vcc_pin": "vcc",
        "vss_pin": "gnd",
        "include_library_name": False,
        "grid_size": 10,
    }
    dict.update(options, options_override)
    out.write(
        "v {xschem version=2.9.7 file_version=1.1}\n"
        "G {}\n"
        "V {}\n"
        "S {}\n"
        "E {}\n"
    )

    def gridify(n):
        return round_to_nearest(n, to=options["grid_size"])

    for line in inp.lines:
        for segment in line.line_segments:
            out.write(
                f"N {gridify(segment[0].x)} {gridify(segment[0].y)} {gridify(segment[1].x)} "
                f"{gridify(segment[1].y)} {{lab={escape(line.connection.net_name)}}}\n"
            )
        out.write(
            f"C {{devices/lab_wire.sym}} {gridify(line.line_segments[0][0].x)} "
            f"{gridify(line.line_segments[0][0].y)} 0 0 {{lab={escape(line.connection.net_name)}}}\n"
        )

    library_prefix = f"{library_name}/" if options["include_library_name"] else ""

    for i, component in enumerate(inp.components):
        # |component                      |output            |
        # |mirrored_over_x|mirrored_over_y|flip|orientation|
        # |              0|              0|     0|          0|
        # |              0|              1|     1|          0|
        # |              1|              0|     1|          2|
        # |              1|              1|     0|          2|
        # https://xschem.sourceforge.io/stefan/xschem_man/developer_info_03.png

        flip = (1 if component.mirrored_over_x else 0) ^ (
            1 if component.mirrored_over_y else 0
        )
        rotation = 2 if component.mirrored_over_x else 0

        embedded_symbols = set()

        if type(component) == entities.CircuitInput:
            out.write(
                f"C {{devices/ipin.sym}} {gridify(component.location.x)} {gridify(component.location.y)} "
                f"{rotation} {flip} "
                f"{{lab={escape(component.identifier)}}}\n"
            )
        elif type(component) == entities.CircuitOutput:
            out.write(
                f"C {{devices/opin.sym}} {gridify(component.location.x)} {gridify(component.location.y)} "
                f"{rotation} {flip} "
                f"{{lab={escape(component.identifier)}}}\n"
            )
        elif type(component) == entities.Cell:
            if (
                options["embed_symbols"]
                and component.human_name not in embedded_symbols
            ):
                embedded_symbols.add(component.human_name)
                out.write(
                    f"C {{{library_prefix}{component.human_name}.sym}} {gridify(component.location.x)} {gridify(component.location.y)} "
                    f"{rotation} {flip} "
                    f"{{name={escape(component.netlist_id)} VCCPIN={options['vcc_pin']} VSSPIN={options['vss_pin']} "
                    f"embed=true}}\n"
                    f"[\n{component.raw_data}\n]\n"
                )
            else:
                out.write(
                    f"C {{{library_prefix}{component.human_name}.sym}} {gridify(component.location.x)} {gridify(component.location.y)} "
                    f"{rotation} {flip} "
                    f"{{name={escape(component.netlist_id)} VCCPIN={options['vcc_pin']} VSSPIN={options['vss_pin']}\n"
                )
