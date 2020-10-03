from src.syntax_tree import *
from src.grammar.comment import Comment


class Statement(Node):

    def __init__(self, parent, start, end, name, element, string):
        super().__init__(parent, start, end, name, element, string)

    def write(self, int_state, block=None):
        for c in self.children:
            c.write(int_state, block)


Node.node_map['STATEMENT'] = Statement


class ExpressionStatement(Node):
    def write(self, int_state, block=None):
        block.append_line('')
        self.children[0].write(int_state, block)
        block.append(';')


Node.node_map['EXPRESSION_STATEMENT'] = ExpressionStatement


class AssignmentOp(Node):

    def write(self, int_state, block=None):
        pass


Node.node_map['ASSIGNMENT_OP'] = AssignmentOp


class Assignment(Node):

    def __init__(self, parent, start, end, name, element, string):
        super().__init__(parent, start, end, name, element, string)

    def write(self, int_state, block=None):
        block.append_line('')
        self.children[0].write(int_state, block)
        block.append(' := ')
        if self.children[1].string == '=':
            self.children[2].write(int_state, block)
        else:
            self.children[0].write(int_state, block)
            block.append(self.children[1].string[0])
            self.children[2].write(int_state, block)


Node.node_map['ASSIGNMENT'] = Assignment


class StatementBlock(Node):

    def __init__(self, parent, start, end, name, element, string):
        super().__init__(parent, start, end, name, element, string)

    def write(self, int_state, block=None):
        for c in self.children:
            if isinstance(c, Statement) or isinstance(c, Comment):
                c.write(int_state, block)


Node.node_map['STATEMENT_BLOCK'] = StatementBlock


class For(Node):

    def __init__(self, parent, start, end, name, element, string):
        super().__init__(parent, start, end, name, element, string)

    def write(self, int_state, block=None):
        self.children[2].write(int_state, block)
        block.append(';')
        block.append_line('while ')
        self.children[4].write(int_state, block)
        block.append(' do begin')
        block.indent()
        self.children[8].write(int_state, block)
        self.children[6].write(int_state, block)
        block.append(';')
        block.unindent()
        block.append_line('end;')


Node.node_map['FOR'] = For
