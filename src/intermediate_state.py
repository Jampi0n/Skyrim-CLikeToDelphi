from src.grammar import *
from src.syntax_tree import *


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
    def __init__(self, syntax_tree: SyntaxTree):
        self.syntax_tree = syntax_tree

        self.globals = TextBlock(1)
        self.constants = TextBlock(1)
        self.functions = TextBlock()
        self.init = TextBlock(1)

        self.has_init = False
        self.has_finalize = False
        self.has_process = False
        self.top_level()

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
                name = node.children[1].string
                if name == '__initialize__':
                    self.has_init = True
                elif name == '__finalize__':
                    self.has_finalize = True
                elif name == '__process__':
                    self.has_process = True

        for const in constants:
            const.write(self)

        for glob in global_variables:
            glob.write(self)

        for func in functions:
            func.write(self)

    def add_to_init(self):
        pass

    def write_program(self):
        result = ''
        if len(self.constants.lines) > 0:
            result += '\n\nconst\n'
            result += self.constants.write_program()

        if len(self.globals.lines) > 0:
            result += '\n\nvar\n'
            result += self.globals.write_program()

        if len(self.functions.lines) > 0:
            result += '\n\n// Functions\n\n'
            result += self.functions.write_program()

        if len(self.init.lines) > 0:
            result += '\n\n// InitGlobals\n'
            result += 'procedure __init_globals__();\nbegin\n'
            result += self.init.write_program()
            result += '\nend;'

        if self.has_process:
            result += '\n\n'
            result += 'function Process(e: IInterface): Integer;\nbegin\n'
            result += '    ' + '__process__(e);\n'
            result += 'end;\n'

        if len(self.init.lines) > 0 or self.has_init:
            result += '\n\n'
            result += 'function Initialize: Integer;\nbegin\n'
            if len(self.init.lines) > 0:
                result += '    ' + '__init_globals__();\n'
            if self.has_init:
                result += '    ' + '__initialize__();\n'
            result += 'end;\n'

        if self.has_finalize:
            result += '\n\n'
            result += 'function Finalize(): Integer;\nbegin\n'
            result += '    ' + '__finalize__();\n'
            result += 'end;\n'

        result += '\n\nend.'

        return result

    # def append_line(self, line):
    #     TextBlock.current.append_line(line)
    #
    # def append(self, string):
    #     TextBlock.current.append(string)
