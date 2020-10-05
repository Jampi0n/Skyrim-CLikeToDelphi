from src.transpiler.syntax_tree import *


# These nodes are never written. Instead the top level nodes below them are accessed.


class ProgramPart(Node):
    def write(self, int_state, block=None):
        assert False


Node.node_map['PROGRAM_PART'] = ProgramPart


class Start(Node):
    def write(self, int_state, block=None):
        assert False


Node.node_map['START'] = Start
