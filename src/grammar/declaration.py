from src.syntax_tree import *


class Declaration(Node):

    def __init__(self, parent, start, end, name, element, string):
        super().__init__(parent, start, end, name, element, string)

    def init(self):
        if len(self.children) == 5:
            return ' := ' + self.children[3].string
        else:
            return ''

    def write(self, int_state, block=None):
        assert False


Node.node_map['DECLARATION'] = Declaration
