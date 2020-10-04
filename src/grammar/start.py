from src.syntax_tree import *


class Start(Node):
    def write(self, int_state, block=None):
        assert False


Node.node_map['START'] = Start
