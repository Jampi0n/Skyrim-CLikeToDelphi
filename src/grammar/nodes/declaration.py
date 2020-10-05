from src.transpiler.syntax_tree import *
from src.grammar.nodes.expression import Expression


class Declaration(Node):
    def is_init(self):
        """
        Returns true, if the declaration also contains an initialization.
        :return:
        """
        if len(self.children) == 4:
            return isinstance(self.children[3], Expression)
        return False

    def write(self, int_state, block=None):
        # Only write the initialization. Declaration is handled by top level objects.
        if self.is_init():
            block.append_line(self.children[1].string + ' := ')
            self.children[3].write(int_state, block)


Node.node_map['DECLARATION'] = Declaration


class GlobalVariable(Node):
    def write(self, int_state, block=None):
        # GLOBAL = seq(DECLARATION, ';')
        declaration = self.children[0]
        int_state.globals.append_line(declaration.children[1].string)

        # DECLARATION = seq(TYPE, VARIABLE_NAME, opt(Choice(seq('=', EXPRESSION), Repeat(seq(',', VARIABLE_NAME)))))
        # If the declaration contains at least 4 elements,
        # it has either an initialization or contains multiple variable names.
        if len(declaration.children) >= 4:
            if isinstance(declaration.children[3], Expression):  # Initialization.
                # seq(TYPE, VARIABLE_NAME, '=', EXPRESSION)
                int_state.init.append_line(declaration.children[1].string + ' := ')
                declaration.children[3].write(int_state, int_state.init)
                int_state.init.append(';')
            else:  # Multiple declarations.
                # seq(TYPE, VARIABLE_NAME, Repeat(seq(',', VARIABLE_NAME)))
                # additional names are at positions 3 + 2 * k
                for i in range(3, len(declaration.children), 2):
                    int_state.globals.append(', ' + declaration.children[i].string)

        # Type and semi colon.
        int_state.globals.append(' : ' + declaration.children[0].translated() + ';')


Node.node_map['GLOBAL'] = GlobalVariable


class Constant(Node):
    def write(self, int_state, block=None):
        # CONSTANT = seq(Keyword('const'), opt(TYPE), VARIABLE_NAME, '=', LITERAL, ';')
        name = self.children[1].translated()
        value = self.children[3].translated()
        if value == '=':  # opt(TYPE) is used.
            name = self.children[2].translated()
            value = self.children[4].translated()
        int_state.constants.append_line(name + ' = ' + value + ';')


Node.node_map['CONSTANT'] = Constant
