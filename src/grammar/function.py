from src.syntax_tree import *
from src.grammar.declaration import Declaration
from src.grammar.expression import Expression


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

        parameter_list = self.children[3]
        if isinstance(parameter_list, ParameterList):
            parameter_list.write(int_state, block)

        block.append(')')
        if not void:
            block.append(' : ' + self.children[0].translated())

        block.append(';')

        declarations = search_declarations(self.children[len(self.children) - 1])
        declared_names = []
        if len(declarations) > 0:
            block.append_line('var')
            block.indent()
            for d in declarations:
                print('declaration')
                name = d.children[1].string
                added_declarations = 0
                if name not in declared_names:
                    block.append_line(d.children[1].string)
                    declared_names.append(name)
                    added_declarations += 1
                if len(d.children) >= 4:
                    if not isinstance(d.children[3], Expression):
                        for i in range(3, len(d.children), 2):
                            name = d.children[i].string
                            print(name)
                            print(declared_names)
                            if name not in declared_names:
                                if added_declarations == 0:
                                    block.append_line(name)
                                else:
                                    block.append(', ' + name)
                                declared_names.append(name)
                                added_declarations += 1

                if added_declarations > 0:
                    block.append(' : ' + d.children[0].translated() + ';')
            block.unindent()

        block.append_line('begin')
        block.indent()
        # for d in declarations:
        #     print(d.string)
        #     if len(d.children) == 4:
        #         block.append_line(d.children[1].string + ' := ')
        #         d.children[3].write(int_state, block)
        #         block.append(';')
        self.children[len(self.children) - 1].write(int_state, block)
        block.unindent()
        block.append_line('end;\n')


Node.node_map['FUNCTION'] = Function


class ParameterList(Node):

    def __init__(self, parent, start, end, name, element, string):
        super().__init__(parent, start, end, name, element, string)

    def write(self, int_state, block=None):
        last_parameter = self.children[len(self.children) - 1]
        last_parameter.is_last = True
        for c in self.children:
            if isinstance(c, Parameter):
                c.write(int_state, block)


Node.node_map['PARAMETER_LIST'] = ParameterList


class Parameter(Node):

    def __init__(self, parent, start, end, name, element, string):
        super().__init__(parent, start, end, name, element, string)
        self.is_last = False

    def write(self, int_state, block=None):
        block.append(self.children[1].string + ' : ' + self.children[0].translated())
        if not self.is_last:
            block.append('; ')


Node.node_map['PARAMETER'] = Parameter


class FunctionBody(Node):

    def __init__(self, parent, start, end, name, element, string):
        super().__init__(parent, start, end, name, element, string)

    def write(self, int_state, block=None):
        assert False


Node.node_map['FUNCTION_BODY'] = FunctionBody
