from src.grammar.nodes import *
from src.transpiler.syntax_tree import *


class TextBlock:
    current = None

    def __init__(self, indentation=0):
        self.lines = []
        self.indentation = indentation
        self.indentation_string = ''
        self.update_indentation()

    def append_line(self, line):
        self.lines.append(self.indentation_string + line)
        TextBlock.current = self

    def append(self, string):
        self.lines[len(self.lines) - 1] += string
        TextBlock.current = self

    def indent(self):
        self.indentation += 1
        self.update_indentation()
        TextBlock.current = self

    def unindent(self):
        self.indentation -= 1
        assert self.indentation >= 0
        self.update_indentation()
        TextBlock.current = self

    def update_indentation(self):
        self.indentation_string = ' ' * 4 * self.indentation

    def write_program(self):
        return '\n'.join(self.lines)


class IntermediateState:
    def __init__(self, syntax_tree_list: List[SyntaxTree], delphi_code_list: List[str]):
        self.syntax_tree_list = syntax_tree_list
        self.delphi_code_list = delphi_code_list

        # Create text blocks.
        self.globals = TextBlock(1)
        self.constants = TextBlock(1)
        self.functions = [TextBlock() for _ in range(len(syntax_tree_list))]
        self.init = TextBlock(1)

        # Special functions.
        self.has_init = False
        self.has_finalize = False
        self.has_process = False

        #
        self.top_level()

    def top_level(self):
        """
        Fills the text blocks with text.
        :return:
        """
        constants = []
        global_variables = []
        functions = []

        # Search top level for constants, global variables and functions.
        for i in range(len(self.syntax_tree_list)):
            # There is a function text block for every syntax tree.
            functions.append([])
            syntax_tree = self.syntax_tree_list[i]
            for node in syntax_tree.get_top_level():
                if isinstance(node, declaration.Constant):
                    constants.append(node)
                elif isinstance(node, declaration.GlobalVariable):
                    global_variables.append(node)
                elif isinstance(node, function.Function):
                    functions[i].append(node)
                    name = node.children[1].string
                    # Special functions.
                    if name == '__initialize__':
                        self.has_init = True
                    elif name == '__finalize__':
                        self.has_finalize = True
                    elif name == '__process__':
                        self.has_process = True

        # Fill text blocks with text generated by constants, global variables and functions.
        for const in constants:
            const.write(self)

        for glob in global_variables:
            glob.write(self)

        for i in range(len(self.syntax_tree_list)):
            for func in functions[i]:
                func.write(self, self.functions[i])

    def write_program(self):
        """
        Assembles the program from the text blocks.
        :return: transpiled code string
        """
        result = ''

        # Constants.
        if len(self.constants.lines) > 0:
            result += 'const\n'
            result += self.constants.write_program()
            result += '\n\n'

        # Global variables.
        if len(self.globals.lines) > 0:
            result += 'var\n'
            result += self.globals.write_program()
            result += '\n\n'

        # Functions.
        for i in range(len(self.syntax_tree_list)):
            result += self.functions[i].write_program() + '\n'
            if i != len(self.syntax_tree_list) - 1:
                delphi = self.delphi_code_list.pop(0) + '\n\n'
                result += delphi

        # Global variable initialization.
        if len(self.init.lines) > 0:
            result += '// InitGlobals\n'
            result += 'procedure __init_globals__();\nbegin\n'
            result += self.init.write_program()
            result += '\nend;\n\n'

        # Special functions.
        if self.has_process:
            result += ''
            result += 'function Process(e: IInterface): Integer;\nbegin\n'
            result += '    ' + '__process__(e);\n'
            result += 'end;\n\n'
        if len(self.init.lines) > 0 or self.has_init:
            result += ''
            result += 'function Initialize: Integer;\nbegin\n'
            if len(self.init.lines) > 0:
                result += '    ' + '__init_globals__();\n'
            if self.has_init:
                result += '    ' + '__initialize__();\n'
            result += 'end;\n\n'
        if self.has_finalize:
            result += ''
            result += 'function Finalize(): Integer;\nbegin\n'
            result += '    ' + '__finalize__();\n'
            result += 'end;\n\n'

        result += 'end.'

        return result
