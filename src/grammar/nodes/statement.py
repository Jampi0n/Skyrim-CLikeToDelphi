from src.transpiler.syntax_tree import *
from src.grammar.nodes.declaration import Declaration
from src.grammar.nodes.expression import Expression


class Statement(Node):
    def write(self, int_state, block=None):
        # STATEMENT = Choice(RETURN, THROW, seq(ASSIGNMENT, ';'), seq(DECLARATION, ';'), IF, WHILE, FOR,
        #                    TRY, CONTINUE, BREAK, EXPRESSION_STATEMENT)
        declaration = self.children[0]
        # DECLARATION = seq(TYPE, VARIABLE_NAME, opt(Choice(seq('=', EXPRESSION), Repeat(seq(',', VARIABLE_NAME)))))
        if isinstance(declaration, Declaration):
            declaration.write(int_state, block)
            # Only write the semi colon of the declaration, if it contains an initialization.
            # If there is no initialization, the line does not appear in the block.
            if declaration.is_init():
                self.children[1].write(int_state, block)

        else:
            for c in self.children:
                c.write(int_state, block)


Node.node_map['STATEMENT'] = Statement


class ExpressionStatement(Node):
    def write(self, int_state, block=None):
        # EXPRESSION_STATEMENT = seq(EXPRESSION, ';')
        block.append_line('')
        self.children[0].write(int_state, block)
        block.append(';')


Node.node_map['EXPRESSION_STATEMENT'] = ExpressionStatement


class AssignmentOp(Node):
    def write(self, int_state, block=None):
        assert False


Node.node_map['ASSIGNMENT_OP'] = AssignmentOp


class Assignment(Node):
    def write(self, int_state, block=None):
        # ASSIGNMENT = seq(EXPRESSION, ASSIGNMENT_OP, EXPRESSION)
        block.append_line('')
        self.children[0].write(int_state, block)
        block.append(' := ')
        if self.children[1].string == '=':  # Standard assignment.
            self.children[2].write(int_state, block)
        else:  # Modifier assignment: +=, *=, ...
            # Convert x += y to x = x + y
            self.children[0].write(int_state, block)
            # Use first character of assignment operator as operator.
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
        # FOR = seq(Keyword('for'), '(', Choice(DECLARATION, ASSIGNMENT), ';', EXPRESSION, ';', ASSIGNMENT, ')',
        #               Choice(STATEMENT_BLOCK, STATEMENT))
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
        # IF = seq(Keyword('if'), '(', EXPRESSION, ')', Choice(STATEMENT_BLOCK, STATEMENT), opt(ELSE))
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
        # ELSE = seq(Keyword('else'), Choice(STATEMENT_BLOCK, STATEMENT))
        block.append_line('end else begin ')
        block.indent()
        self.children[1].write(int_state, block)
        block.unindent()
        block.append_line('end;')


Node.node_map['ELSE'] = Else


class While(Node):
    def write(self, int_state, block=None):
        # WHILE = seq(Keyword('while'), '(', EXPRESSION, ')', Choice(STATEMENT_BLOCK, STATEMENT))
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
        # TRY = seq(Keyword('try'), Choice(STATEMENT_BLOCK, STATEMENT), opt(CATCH), opt(FINALLY))
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
        # CATCH = seq(Keyword('catch'), '(', PARAMETER, ')', Choice(STATEMENT_BLOCK, STATEMENT))
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
        # FINALLY = seq(Keyword('finally'), Choice(STATEMENT_BLOCK, STATEMENT))
        block.append_line('finally')
        block.indent()
        self.children[1].write(int_state, block)
        block.unindent()


Node.node_map['FINALLY'] = Finally


class Throw(Node):
    def write(self, int_state, block=None):
        # THROW = seq(Keyword('throw'), EXPRESSION, ';')
        block.append_line('raise ')
        self.children[1].write(int_state, block)
        block.append(';')


Node.node_map['THROW'] = Throw


class Return(Node):

    def write(self, int_state, block=None):
        # RETURN = seq(Keyword('return'), Optional(EXPRESSION), ';')
        expr = self.children[1]
        if isinstance(expr, Expression):
            block.append_line('Result := ')
            expr.write(int_state, block)
            block.append(';')

        block.append_line('exit;')


Node.node_map['RETURN'] = Return


class Continue(Leaf):
    def write(self, int_state, block=None):
        # CONTINUE = seq(Keyword('continue'), ';')
        block.append_line('continue;')


Node.node_map['CONTINUE'] = Continue


class Break(Leaf):
    def write(self, int_state, block=None):
        # BREAK = seq(Keyword('break'), ';')
        block.append_line('break;')


Node.node_map['BREAK'] = Break
