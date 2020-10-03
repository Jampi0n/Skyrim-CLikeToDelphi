from src.syntax_tree import *


class GlobalVariable(Node):

    def __init__(self, parent, start, end, name, element, string):
        super().__init__(parent, start, end, name, element, string)

    def write(self, int_state, block=None):
        declaration = self.children[0]
        assert len(declaration.children) == 2 or len(declaration.children) == 4
        int_state.globals.append_line(declaration.children[1].string + ' : ' + declaration.children[0].string + ';')
        if len(declaration.children) == 4:
            int_state.init.append_line(declaration.children[1].string + ' := ')
            declaration.children[3].write(int_state, int_state.init)
            int_state.init.append(';')


Node.node_map['GLOBAL'] = GlobalVariable
