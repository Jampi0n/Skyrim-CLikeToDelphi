from src.syntax_tree import *


class Constant(Node):

    def __init__(self, parent, start, end, name, element, string):
        super().__init__(parent, start, end, name, element, string)

    def write(self, int_state, block=None):
        int_state.constants.append_line(self.children[1].string + ' = ' + self.children[3].translated() + ';')


Node.node_map['CONSTANT'] = Constant
