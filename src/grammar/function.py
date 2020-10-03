from src.syntax_tree import *


class Function(Node):

    def __init__(self, parent, start, end, name, element, string):
        super().__init__(parent, start, end, name, element, string)

    def write(self):
        assert False


Node.node_map['FUNCTION'] = Function


class ParameterList(Node):

    def __init__(self, parent, start, end, name, element, string):
        super().__init__(parent, start, end, name, element, string)

    def write(self):
        assert False


Node.node_map['PARAMETER_LIST'] = ParameterList


class Parameter(Node):

    def __init__(self, parent, start, end, name, element, string):
        super().__init__(parent, start, end, name, element, string)

    def write(self):
        assert False


Node.node_map['PARAMETER'] = Parameter


class FunctionBody(Node):

    def __init__(self, parent, start, end, name, element, string):
        super().__init__(parent, start, end, name, element, string)

    def write(self):
        assert False


Node.node_map['FUNCTION_BODY'] = FunctionBody
