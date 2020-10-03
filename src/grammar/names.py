from src.syntax_tree import *


class VariableName(Node):

    def __init__(self, parent, start, end, name, element, string):
        super().__init__(parent, start, end, name, element, string)


Node.node_map['VARIABLE_NAME'] = VariableName


class FunctionName(Node):

    def __init__(self, parent, start, end, name, element, string):
        super().__init__(parent, start, end, name, element, string)


Node.node_map['FUNCTION_NAME'] = FunctionName


class Type(Node):

    def __init__(self, parent, start, end, name, element, string):
        super().__init__(parent, start, end, name, element, string)


Node.node_map['TYPE'] = Type
