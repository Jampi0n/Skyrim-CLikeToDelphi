from src.transpiler.syntax_tree import *
from src.grammar.nodes.declaration import Declaration
from src.grammar.nodes.expression import Expression
from src.grammar.nodes.comment import Cmt


class Statement(Node):
    def write(self, int_state, block=None):

        print('statement')
        for c in self.children:
            print(c.string)

        for c in self.children:
            if isinstance(c, Cmt):
                block.append_line('')
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
    def write(self, int_state, block=None):
        for c in self.children:
            if isinstance(c, Statement):
                c.write(int_state, block)


Node.node_map['STATEMENT_BLOCK'] = StatementBlock


class For(Node):
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


class If(Node):
    def write(self, int_state, block=None):
        block.append_line('if ')
        self.children[2].write(int_state, block)
        block.append(' then begin')
        block.indent()
        self.children[4].write(int_state, block)
        block.unindent()
        if len(self.children) < 6:
            block.append_line('end;')
        else:
            self.children[5].write(int_state, block)


Node.node_map['IF'] = If


class Else(Node):
    def write(self, int_state, block=None):
        block.append_line('end else begin ')
        block.indent()
        self.children[1].write(int_state, block)
        block.unindent()
        block.append_line('end;')


Node.node_map['ELSE'] = Else


class While(Node):
    def write(self, int_state, block=None):
        block.append_line('while ')
        self.children[2].write(int_state, block)
        block.append(' do begin')
        block.indent()
        self.children[4].write(int_state, block)
        block.unindent()
        block.append_line('end;')


Node.node_map['WHILE'] = While


class Try(Node):
    def write(self, int_state, block=None):
        block.append_line('try ')
        block.indent()
        self.children[1].write(int_state, block)
        block.unindent()

        for i in range(2, len(self.children)):
            self.children[i].write(int_state, block)

        block.append_line('end;')


Node.node_map['TRY'] = Try


class Catch(Node):
    def write(self, int_state, block=None):
        block.append_line('except')
        block.indent()
        block.append_line('on ')
        parameter = self.children[2]
        parameter.is_last = True
        parameter.write(int_state, block)
        block.append(' do begin')
        block.indent()
        self.children[4].write(int_state, block)
        block.unindent()
        block.append_line('end;')
        block.unindent()


Node.node_map['CATCH'] = Catch


class Finally(Node):
    def write(self, int_state, block=None):
        block.append_line('finally')
        block.indent()
        self.children[1].write(int_state, block)
        block.unindent()


Node.node_map['FINALLY'] = Finally


class Throw(Node):
    def write(self, int_state, block=None):
        block.append_line('raise ')
        self.children[1].write(int_state, block)
        block.append(';')


Node.node_map['THROW'] = Throw


class Return(Node):

    def write(self, int_state, block=None):
        expr = self.children[1]
        if isinstance(expr, Expression):
            block.append_line('Result := ')
            expr.write(int_state, block)
            block.append(';')

        block.append_line('exit;')


Node.node_map['RETURN'] = Return


class Continue(Leaf):
    def write(self, int_state, block=None):
        block.append_line('continue;')


Node.node_map['CONTINUE'] = Continue


class Break(Leaf):
    def write(self, int_state, block=None):
        block.append_line('break;')


Node.node_map['BREAK'] = Break
