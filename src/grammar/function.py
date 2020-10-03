from src.syntax_tree import *
from src.grammar.declaration import Declaration


def search_declarations(node):
    result = []
    if isinstance(node, Declaration):
        result += [node]
    else:
        for c in node.children:
            result += search_declarations(c)

    return result


class Function(Node):

    def __init__(self, parent, start, end, name, element, string):
        super().__init__(parent, start, end, name, element, string)

    def write(self, int_state, block=None):
        block = int_state.functions
        void = self.children[0].string == 'void'
        block.append_line(('procedure ' if void else 'function ') + self.children[1].string + '(')

        block.append(')')
        if not void:
            block.append(' : ' + self.children[0].string)

        block.append(';')

        declarations = search_declarations(self.children[5])
        if len(declarations) > 0:
            block.append_line('var')
            block.indent()
            for d in declarations:
                assert len(d.children) == 4 or len(d.children) == 2
                block.append_line(d.children[1].string + ' : ' + d.children[0].string + ';')
            block.unindent()

        block.append_line('begin')
        block.indent()
        # for d in declarations:
        #     print(d.string)
        #     if len(d.children) == 4:
        #         block.append_line(d.children[1].string + ' := ')
        #         d.children[3].write(int_state, block)
        #         block.append(';')
        self.children[5].write(int_state, block)
        block.unindent()
        block.append_line('end;')


Node.node_map['FUNCTION'] = Function


class ParameterList(Node):

    def __init__(self, parent, start, end, name, element, string):
        super().__init__(parent, start, end, name, element, string)

    def write(self, int_state, block=None):
        assert False


Node.node_map['PARAMETER_LIST'] = ParameterList


class Parameter(Node):

    def __init__(self, parent, start, end, name, element, string):
        super().__init__(parent, start, end, name, element, string)

    def write(self, int_state, block=None):
        assert False


Node.node_map['PARAMETER'] = Parameter


class FunctionBody(Node):

    def __init__(self, parent, start, end, name, element, string):
        super().__init__(parent, start, end, name, element, string)

    def write(self, int_state, block=None):
        assert False


Node.node_map['FUNCTION_BODY'] = FunctionBody
