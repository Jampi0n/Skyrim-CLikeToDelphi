from src.syntax_tree import *


class Expression(Node):
    def write(self, int_state, block=None):
        for c in self.children:
            c.write(int_state, block)


Node.node_map['EXPRESSION'] = Expression


class Variable(Node):
    def write(self, int_state, block=None):
        self.children[0].write(int_state, block)


Node.node_map['VARIABLE'] = Variable


class ArgumentList(Node):
    def write(self, int_state, block=None):
        for c in self.children:
            c.write(int_state, block)


Node.node_map['ARGUMENT_LIST'] = ArgumentList


class Prefix(Node):
    def write(self, int_state, block=None):
        for c in self.children:
            c.write(int_state, block)


Node.node_map['PREFIX'] = Prefix
