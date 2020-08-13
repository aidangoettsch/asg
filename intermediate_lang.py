from entities import *


class InputIL:
    def __init__(self, components, connections):
        self.components = components
        self.connections = connections


class OutputIL:
    def __init__(self):
        self.components = []
        self.connections = []
        self.lines = []

    def create_lines(self):
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

                if (
                    start_pin_location.x == end_pin_location.x
                    or start_pin_location.y == end_pin_location.y
                ):
                    line.locations = [start_pin_location, end_pin_location]

                if not (
                    start_pin_location == line.locations[0]
                    and end_pin_location == line.locations[-1]
                ):
                    print(f"redrawing line from {start_component} to {end_component}")
                    x_midpoint = (start_pin_location.x + end_pin_location.x) / 2
                    bend_start = Point(x_midpoint, start_pin_location.y)
                    bend_end = Point(x_midpoint, end_pin_location.y)
                    bends = [bend_start, bend_end]
                    line.locations = [start_pin_location, *bends, end_pin_location]


class LibraryIL:
    def __init__(self):
        self.symbols = {}
