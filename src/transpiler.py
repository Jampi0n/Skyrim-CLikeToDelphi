from src.grammar import CLike
from src.syntax_tree import SyntaxTree
from src.intermediate_state import IntermediateState


def transpile_string(in_string):
    grammar = CLike()
    syntax_tree = SyntaxTree(grammar, in_string)
    intermediate_state = IntermediateState(syntax_tree)
    return intermediate_state.write_program()


def transpile_file(in_path, out_path):
    in_file = open(in_path, 'r')
    out_file = open(out_path, 'w')
    out_file.write(transpile_string(in_file.read()))
