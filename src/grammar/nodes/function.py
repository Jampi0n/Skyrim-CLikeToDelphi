from src.transpiler.syntax_tree import *
from src.grammar.nodes.declaration import Declaration
from src.grammar.nodes.expression import Expression


def search_declarations(node):
    """
    Searches for sub nodes of type Declaration.
    :param node:
    :return: list of Declarations
    """
    result = []
    if isinstance(node, Declaration):
        result += [node]
    else:
        for c in node.children:
            result += search_declarations(c)

    return result


class Function(Node):
    def write(self, int_state, block=None):
        # FUNCTION = seq(TYPE, FUNCTION_NAME, '(', PARAMETER_LIST, ')', STATEMENT_BLOCK)

        # Function or Procedure.
        void = self.children[0].string == 'void'
        block.append_line(('procedure ' if void else 'function ') + self.children[1].string + '(')

        # If parameter list exists, it is at index 3.
        parameter_list = self.children[3]
        if isinstance(parameter_list, ParameterList):
            parameter_list.write(int_state, block)

        block.append(')')

        # Return type.
        if not void:
            block.append(' : ' + self.children[0].translated())

        block.append(';')

        # Handle declarations.
        declarations = search_declarations(self.children[len(self.children) - 1])
        declared_names = []  # Avoid multiple declarations of the same name.
        if len(declarations) > 0:
            block.append_line('var')
            block.indent()
            for d in declarations:
                name = d.children[1].string
                added_declarations = 0  # There is no ',' before the first declaration, but a new line.
                if name not in declared_names:
                    block.append_line(d.children[1].string)
                    declared_names.append(name)
                    added_declarations += 1
                # DECLARATION =
                # seq(TYPE, VARIABLE_NAME, opt(Choice(seq('=', EXPRESSION), Repeat(seq(',', VARIABLE_NAME)))))
                # If the declaration contains at least 4 elements,
                # it has either an initialization or contains multiple variable names.
                if len(d.children) >= 4:
                    if not isinstance(d.children[3], Expression):  # Multiple declarations.
                        # seq(TYPE, VARIABLE_NAME, Repeat(seq(',', VARIABLE_NAME)))
                        # additional names are at positions 3 + 2 * k
                        for i in range(3, len(d.children), 2):
                            name = d.children[i].string
                            if name not in declared_names:
                                if added_declarations == 0:
                                    block.append_line(name)
                                else:
                                    block.append(', ' + name)
                                declared_names.append(name)
                                added_declarations += 1
                # If there were declarations, the line ends with the type and semi colon.
                if added_declarations > 0:
                    block.append(' : ' + d.children[0].translated() + ';')
            block.unindent()

        # Function body.
        block.append_line('begin')
        block.indent()
        self.children[len(self.children) - 1].write(int_state, block)
        block.unindent()
        block.append_line('end;\n')


Node.node_map['FUNCTION'] = Function


class ParameterList(Node):
    def write(self, int_state, block=None):
        # PARAMETER_LIST = opt(seq(Repeat(seq(PARAMETER, ',')), PARAMETER))
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
        # PARAMETER = seq(TYPE, VARIABLE_NAME)
        block.append(self.children[1].string + ' : ' + self.children[0].translated())
        if not self.is_last:
            block.append('; ')


Node.node_map['PARAMETER'] = Parameter
