import intermediate_lang


def il_to_xschem(
    inp: intermediate_lang.OutputIL, out, library: intermediate_lang.LibraryIL
):
    out.write(
        """
    v {xschem version=2.9.7 file_version=1.1}
    G {}
    V {}
    S {}
    E {}
    """
    )

    for line in inp.lines:
        for segment in line.line_segments:
            out.write(
                f"N {segment[0].x} {segment[0].y} {segment[1].x} {segment[1].y}\n"
            )

    for i, component in enumerate(inp.components):
        out.write(
            f"C {{{component.human_name}.sym}} {component.location.x} {component.location.y}"
            f"{1 if component.mirrored_over_x else 0} {1 if component.mirrored_over_y else 0}"
            f"{{name=x{i} VCCPIN=VCC VSSPIN=VSS}}"
        )
