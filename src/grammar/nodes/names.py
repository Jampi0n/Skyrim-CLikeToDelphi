from src.transpiler.syntax_tree import *


class VariableName(Leaf):
    pass


Node.node_map['VARIABLE_NAME'] = VariableName


class FunctionName(Leaf):
    pass


Node.node_map['FUNCTION_NAME'] = FunctionName


class Type(Leaf):
    def translated(self):
        # Basic type translation.
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
