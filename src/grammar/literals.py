from src.syntax_tree import *


class Literal(Leaf):

    def __init__(self, parent, start, end, name, element, string):
        super().__init__(parent, start, end, name, element, string)

    def translated(self):
        if self.string[0] == '"':
            return '\'' + self.string[1:-1] + '\''
        return self.string


Node.node_map['LITERAL'] = Literal
