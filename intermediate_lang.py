from entities import *
from typing import List


class InputIL:
    """
    Represents a circuit being input to the ASG
    """

    def __init__(
        self,
        components: List[Component],
        connections: List[Connection],
        inouts: List[str],
    ):
        """
        Create an InputIL
        :param components: Components in the circuit
        :param connections: Connections between components in the circuit
        """
        self.components = components
        self.connections = connections
        self.inouts = inouts


class OutputIL:
    """
    Represents a circuit being output from the ASG
    """

    def __init__(self):
        self.components = []
        self.connections = []
        self.lines = []

    def create_lines(self) -> None:
        """
        Draws an initial set of lines between components
        :return: None
        """
        res = []
        for connection in self.connections:
            start_component = self.components[connection.start_entity]
            end_component = self.components[connection.end_entity]
            start_pin_location = (
                start_component.location
                + start_component.pin_locations[connection.start_pin]
            )
            end_pin_location = (
                end_component.location + end_component.pin_locations[connection.end_pin]
            )

            x_midpoint = (start_pin_location.x + end_pin_location.x) / 2
            bend_start = Point(x_midpoint, start_pin_location.y)
            bend_end = Point(x_midpoint, end_pin_location.y)
            bends = [bend_start, bend_end]
            res.append(Line(connection, start_pin_location, *bends, end_pin_location))

        self.lines = res

    def repair_lines(self):
        """
        Draws an initial set of lines between components if they don't exist, shifts existing lines to match component locations
        :return: None
        """
        if len(self.lines) == 0:
            self.create_lines()
        else:
            for line in self.lines:
                connection = line.connection
                start_component = self.components[connection.start_entity]
                end_component = self.components[connection.end_entity]
                start_pin_location = (
                    start_component.location
                    + start_component.pin_locations[connection.start_pin]
                )
                end_pin_location = (
                    end_component.location
                    + end_component.pin_locations[connection.end_pin]
                )

                # If the line can be straight we do that
                if (
                    start_pin_location.x == end_pin_location.x
                    or start_pin_location.y == end_pin_location.y
                ):
                    line.locations = [start_pin_location, end_pin_location]

                if not (
                    start_pin_location == line.locations[0]
                    and end_pin_location == line.locations[-1]
                ):
                    # Change locations of lines when components move
                    print(f"redrawing line from {start_component} to {end_component}")
                    if len(line.locations) < 4:
                        # Add a bend if the line was previously straight
                        x_midpoint = (start_pin_location.x + end_pin_location.x) / 2
                        bend_start = Point(x_midpoint, start_pin_location.y)
                        bend_end = Point(x_midpoint, end_pin_location.y)
                        bends = [bend_start, bend_end]
                        line.locations = [start_pin_location, *bends, end_pin_location]
                    else:
                        # Otherwise, just change the y of the existing points to match
                        line.locations[0] = start_pin_location
                        line.locations[1].y = start_pin_location.y
                        line.locations[-2].y = end_pin_location.y
                        line.locations[-1] = end_pin_location


class LibraryIL:
    """
    Represents a symbol library, indexed by cell name
    """

    def __init__(self):
        """
        Create a LibraryIL
        """
        self.symbols = {}
