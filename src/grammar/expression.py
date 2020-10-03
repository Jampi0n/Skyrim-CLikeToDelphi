from src.syntax_tree import *


class Expression(Node):

    def __init__(self, parent, start, end, name, element, string):
        super().__init__(parent, start, end, name, element, string)

    def write(self):
        assert False


Node.node_map['EXPRESSION'] = Expression


class Variable(Node):

    def __init__(self, parent, start, end, name, element, string):
        super().__init__(parent, start, end, name, element, string)

    def write(self):
        assert False


Node.node_map['VARIABLE'] = Variable
