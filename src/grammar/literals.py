from src.syntax_tree import *


class Literal(Leaf):

    def __init__(self, parent, start, end, name, element, string):
        super().__init__(parent, start, end, name, element, string)


Node.node_map['LITERAL'] = Literal
