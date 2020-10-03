from src.syntax_tree import SyntaxTree, Node


class IntermediateState:
    def __init__(self, syntax_tree: SyntaxTree):
        self.syntax_tree = syntax_tree
        self.lines = []
        self.indentation = 0
        self.indentation_string = ''

        self.extract_constants()
        self.extract_globals()

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

    def extract_constants(self):
        constants = []
        for node in self.syntax_tree.get_top_level():
            if node.name == 'CONSTANT':
                constants.append(node)

        if len(constants) > 0:
            self.write_line('const')
            self.indent()
            for const in constants:
                const: Node
                self.write_line(const.children[1].string + ' := ' + const.children[3].string)
            self.unindent()

    def extract_globals(self):
        global_variables = []
        for node in self.syntax_tree.get_top_level():
            if node.name == 'GLOBAL':
                global_variables.append(node)

        if len(global_variables) > 0:
            self.write_line('var')
            self.indent()
            for glob in global_variables:
                glob: Node
                declaration = glob.children[0]
                if len(declaration.children) > 2:
                    self.write_line(
                        declaration.children[1].string + ' := ' + declaration.children[3].string + ' : ' +
                        declaration.children[0].string + ';')
                else:
                    self.write_line(declaration.children[1].string + ' : ' + declaration.children[0].string + ';')
            self.unindent()

    def write_program(self):
        return '\n'.join(self.lines)
