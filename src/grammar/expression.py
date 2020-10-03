from src.syntax_tree import *


class Expression(Node):

    def __init__(self, parent, start, end, name, element, string):
        super().__init__(parent, start, end, name, element, string)

    def write(self, int_state, block=None):
        for c in self.children:
            c.write(int_state, block)


Node.node_map['EXPRESSION'] = Expression


class Variable(Node):

    def __init__(self, parent, start, end, name, element, string):
        super().__init__(parent, start, end, name, element, string)

    def write(self, int_state, block=None):
        assert False


Node.node_map['VARIABLE'] = Variable


class ArgumentList(Node):

    def __init__(self, parent, start, end, name, element, string):
        super().__init__(parent, start, end, name, element, string)

    def write(self, int_state, block=None):
        for c in self.children:
            c.write(int_state, block)


Node.node_map['ARGUMENT_LIST'] = ArgumentList
