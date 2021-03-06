from src.transpiler.syntax_tree import *


class Expression(Node):
    def write(self, int_state, block=None):
        for c in self.children:
            c.write(int_state, block)


Node.node_map['EXPRESSION'] = Expression


class ArgumentList(Node):
    def write(self, int_state, block=None):
        for c in self.children:
            c.write(int_state, block)


Node.node_map['ARGUMENT_LIST'] = ArgumentList
