from src.syntax_tree import *


class Constant(Node):

    def __init__(self, parent, start, end, name, element, string):
        super().__init__(parent, start, end, name, element, string)

    def write(self, int_state, block=None):
        name = self.children[1].translated()
        value = self.children[3].translated()
        if value == '=':
            name = self.children[2].translated()
            value = self.children[4].translated()
        int_state.constants.append_line(name + ' = ' + value + ';')


Node.node_map['CONSTANT'] = Constant
