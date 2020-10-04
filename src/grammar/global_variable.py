from src.syntax_tree import *
from src.grammar.expression import Expression


class GlobalVariable(Node):
    def write(self, int_state, block=None):
        declaration = self.children[0]
        int_state.globals.append_line(declaration.children[1].string)
        if len(declaration.children) >= 4:
            if isinstance(declaration.children[3], Expression):
                int_state.init.append_line(declaration.children[1].string + ' := ')
                declaration.children[3].write(int_state, int_state.init)
                int_state.init.append(';')
            else:
                for i in range(3, len(declaration.children), 2):
                    int_state.globals.append(', ' + declaration.children[i].string)

        int_state.globals.append(' : ' + declaration.children[0].translated() + ';')


Node.node_map['GLOBAL'] = GlobalVariable
