class Atom:
    def __init__(self, name, children):
        self.name = name
        self.children = children
        if None in children:
            raise Exception("none in lisp atom")

    def __str__(self):
        child_string = " ".join(
            [str(e) if type(e) != str else f'"{e}"' for e in self.children]
        )
        return f"({self.name} {child_string})"


class Literal:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value

    def __eq__(self, other):
        return self.value == other
