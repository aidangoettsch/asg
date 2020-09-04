import asg.intermediate_lang as intermediate_lang


def il_to_markdown(output_il: intermediate_lang.OutputIL, output_file) -> None:
    output_file.write("# Components\n")
    for component in output_il.components:
        output_file.write(f"- {component}\n")
    output_file.write("\n# Lines\n")
    for line in output_il.lines:
        component_start = output_il.components[line.connection.start_entity]
        start_pin = line.connection.start_pin
        component_end = output_il.components[line.connection.end_entity]
        end_pin = line.connection.end_pin
        output_file.write(
            f"- Line from {component_start} pin #{start_pin} to {component_end} pin #{end_pin}\n"
        )
