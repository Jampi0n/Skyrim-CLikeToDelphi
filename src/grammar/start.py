from src.syntax_tree import *


class Start(Node):

    def __init__(self, parent, start, end, name, element, string):
        super().__init__(parent, start, end, name, element, string)

    def write(self, int_state, block=None):
        assert False


Node.node_map['START'] = Start
