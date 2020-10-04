from src.transpiler.syntax_tree import *


class VariableName(Node):
    pass


Node.node_map['VARIABLE_NAME'] = VariableName


class FunctionName(Node):
    pass


Node.node_map['FUNCTION_NAME'] = FunctionName


class Type(Node):
    def translated(self):
        type_translation = {
            'int': 'Integer',
            'float': 'Real',
            'string': 'String',
            'bool': 'Boolean',
        }
        string = self.string
        if string in type_translation:
            string = type_translation[string]
        return string


Node.node_map['TYPE'] = Type
