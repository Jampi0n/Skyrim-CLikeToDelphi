from src.syntax_tree import *


class Constant(Node):

    def __init__(self, parent, start, end, name, element, string):
        super().__init__(parent, start, end, name, element, string)

    def write(self):
        return self.children[1].string + ' := ' + self.children[3].string + ';'


Node.node_map['CONSTANT'] = Constant
