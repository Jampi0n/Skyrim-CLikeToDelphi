from src.syntax_tree import *


class Declaration(Node):

    def __init__(self, parent, start, end, name, element, string):
        super().__init__(parent, start, end, name, element, string)

    def write(self, int_state, block=None):
        if len(self.children) == 4:
            block.append_line(self.children[1].string + ' := ')
            self.children[3].write(int_state, block)


Node.node_map['DECLARATION'] = Declaration
