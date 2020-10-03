from src.grammar import *
from src.syntax_tree import *


class IntermediateState:
    def __init__(self, syntax_tree: SyntaxTree):
        self.syntax_tree = syntax_tree
        self.lines = []
        self.indentation = 0
        self.indentation_string = ''

        self.top_level()

    def write_line(self, line):
        print(line)
        self.lines.append(self.indentation_string + line)

    def indent(self):
        self.indentation += 1
        self.update_indentation()

    def unindent(self):
        self.indentation -= 1
        assert self.indentation >= 0
        self.update_indentation()

    def update_indentation(self):
        self.indentation_string = ' ' * 4 * self.indentation

    def top_level(self):
        constants = []
        global_variables = []
        functions = []
        for node in self.syntax_tree.get_top_level():
            if isinstance(node, constant.Constant):
                constants.append(node)
            elif isinstance(node, global_variable.GlobalVariable):
                global_variables.append(node)
            elif isinstance(node, function.Function):
                functions.append(node)

        if len(constants) > 0:
            self.write_line('const')
            self.indent()
            for const in constants:
                self.write_line(const.write())
            self.unindent()

        if len(global_variables) > 0:
            self.write_line('var')
            self.indent()
            for glob in global_variables:
                self.write_line(glob.write())
            self.unindent()

    def write_program(self):
        return '\n'.join(self.lines)
