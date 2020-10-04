from src.grammar.grammar import CLike
from src.syntax_tree import SyntaxTree
from src.intermediate_state import IntermediateState
from src.pre_process import PreProcess


def transpile_string(in_string):
    grammar = CLike()
    pre_process = PreProcess(in_string)
    header, in_string = pre_process.pre_process()

    tmp_file = open('out/in.cs', 'w')
    tmp_file.write(in_string)

    syntax_tree = SyntaxTree(grammar, in_string)
    intermediate_state = IntermediateState(syntax_tree)
    return header + intermediate_state.write_program()


def transpile_file(in_path, out_path):
    in_file = open(in_path, 'r')
    out_file = open(out_path, 'w')
    out_file.write(transpile_string(in_file.read()))
