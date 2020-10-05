from src.grammar.grammar import CLike
from src.transpiler.syntax_tree import SyntaxTree
from src.transpiler.intermediate_state import IntermediateState
from src.transpiler.pre_process import pre_process
from pathlib import Path


def transpile_file(in_path, out_path):
    """
    Transpiles the file located at in_path to a delphi file located at out_path.
    :param in_path: The path of the source file which will be transpiled.
    :param out_path: The path of the delphi file which will be created.
    :return:
    """

    # Absolute paths
    in_path = Path(in_path).absolute()
    out_path = Path(out_path).absolute()

    # Pre-process the file.
    header, in_string_list, delphi_string_list = pre_process(in_path)

    # Save independent sections of the source file to temporary files for debugging.
    for i in range(len(in_string_list)):
        tmp_path = Path(out_path).absolute().parent.joinpath(Path('tmp_' + str(i * 2) + '_source.cs'))
        tmp_file = open(tmp_path, 'w')
        tmp_file.write(in_string_list[i])
    for i in range(len(delphi_string_list)):
        tmp_path = Path(out_path).absolute().parent.joinpath(Path('tmp_' + str(i * 2 + 1) + '_delphi.pas'))
        tmp_file = open(tmp_path, 'w')
        tmp_file.write(delphi_string_list[i])

    # Create grammar object
    grammar = CLike()

    # Create syntax tree for every section that needs to be transpiled
    syntax_tree_list = [SyntaxTree(grammar, in_string) for in_string in in_string_list]

    # Create intermediate state
    intermediate_state = IntermediateState(syntax_tree_list, delphi_string_list)

    # Create final result and save it
    out_string = header + intermediate_state.write_program()
    out_file = open(out_path, 'w')
    out_file.write(out_string)
