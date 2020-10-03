from src.syntax_tree import *


class GlobalVariable(Node):

    def __init__(self, parent, start, end, name, element, string):
        super().__init__(parent, start, end, name, element, string)

    def declaration(self):
        return self.children[0]

    def write(self):
        return self.declaration().write()


Node.node_map['GLOBAL'] = GlobalVariable
