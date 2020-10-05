from src.grammar.grammar import CLike
from src.transpiler.syntax_tree import SyntaxTree
from src.transpiler.intermediate_state import IntermediateState
from src.transpiler.pre_process import pre_process
from pathlib import Path


class Transpile:
    def __init__(self, in_path, out_path):
        """
        Transpiles the file located at in_path to a delphi file located at out_path.
        :param in_path: The path of the source file which will be transpiled.
        :param out_path: The path of the delphi file which will be created.
        """
        self.in_path = in_path
        self.out_path = out_path

        # Absolute paths
        in_path = Path(in_path).absolute()
        out_path = Path(out_path).absolute()

        # Pre-process the file.
        self.header, self.in_string_list, self.delphi_string_list = pre_process(in_path)

        # Save independent sections of the source file to temporary files for debugging.
        for i in range(len(self.in_string_list)):
            tmp_path = Path(out_path).absolute().parent.joinpath(Path('tmp_' + str(i * 2) + '_source.cs'))
            tmp_file = open(tmp_path, 'w')
            tmp_file.write(self.in_string_list[i])
        for i in range(len(self.delphi_string_list)):
            tmp_path = Path(out_path).absolute().parent.joinpath(Path('tmp_' + str(i * 2 + 1) + '_delphi.pas'))
            tmp_file = open(tmp_path, 'w')
            tmp_file.write(self.delphi_string_list[i])

        # Create grammar object
        self.grammar = CLike()

        # Create syntax tree for every section that needs to be transpiled
        self.syntax_tree_list = [SyntaxTree(self.grammar, in_string) for in_string in self.in_string_list]

        # Create intermediate state
        self.intermediate_state = IntermediateState(self.syntax_tree_list, self.delphi_string_list)

        # Create final result and save it
        self.program = self.intermediate_state.write_program()
        self.out_string = self.header + self.program
        out_file = open(out_path, 'w')
        out_file.write(self.out_string)


def transpile_file(in_path, out_path):
    return Transpile(in_path, out_path)
