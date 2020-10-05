from src.grammar.grammar import CLike
from src.transpiler.syntax_tree import SyntaxTree
from src.transpiler.intermediate_state import IntermediateState
from src.transpiler.pre_process import pre_process
from pathlib import Path


def transpile_file(in_path, out_path):
    in_path = Path(in_path).absolute()
    out_path = Path(out_path).absolute()
    header, in_string = pre_process(in_path)

    tmp_path = Path(out_path).absolute().parent.joinpath(Path('tmp.cs'))
    tmp_file = open(tmp_path, 'w')
    tmp_file.write(in_string)

    grammar = CLike()

    syntax_tree = SyntaxTree(grammar, in_string)
    intermediate_state = IntermediateState(syntax_tree)
    out_string = header + intermediate_state.write_program()
    out_file = open(out_path, 'w')
    out_file.write(out_string)
