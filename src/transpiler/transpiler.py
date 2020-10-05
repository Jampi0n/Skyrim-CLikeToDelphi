from src.grammar.grammar import CLike
from src.transpiler.syntax_tree import SyntaxTree
from src.transpiler.intermediate_state import IntermediateState
from src.transpiler.pre_process import pre_process
from pathlib import Path


def transpile_file(in_path, out_path):
    in_path = Path(in_path).absolute()
    out_path = Path(out_path).absolute()
    header, in_string_list, delphi_string_list = pre_process(in_path)

    for i in range(len(in_string_list)):
        tmp_path = Path(out_path).absolute().parent.joinpath(Path('tmp_source_' + str(i * 2) + '.cs'))
        tmp_file = open(tmp_path, 'w')
        tmp_file.write(in_string_list[i])

    for i in range(len(delphi_string_list)):
        tmp_path = Path(out_path).absolute().parent.joinpath(Path('tmp_delphi_' + str(i * 2 + 1) + '.pas'))
        tmp_file = open(tmp_path, 'w')
        tmp_file.write(delphi_string_list[i])

    grammar = CLike()

    syntax_tree_list = [SyntaxTree(grammar, in_string) for in_string in in_string_list]
    intermediate_state = IntermediateState(syntax_tree_list, delphi_string_list)
    out_string = header + intermediate_state.write_program()
    out_file = open(out_path, 'w')
    out_file.write(out_string)
