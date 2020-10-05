from src.transpiler.syntax_tree import *
from src.grammar.nodes.expression import Expression
from src.grammar.nodes.names import VariableName, Type
from src.grammar.nodes.comment import Cmt


class Declaration(Node):
    def get_expr(self):
        for c in self.children:
            if isinstance(c, Expression):
                return c
        return None

    def get_name(self):
        for c in self.children:
            if isinstance(c, VariableName):
                return c
        return None

    def get_type(self):
        for c in self.children:
            if isinstance(c, Type):
                return c
        return None

    def write(self, int_state, block=None):
        """
        Writes the assignment if it exists.
        :param int_state:
        :param block:
        :return:
        """
        if self.get_expr() is not None:
            block.append_line(self.get_name().string + ' := ')
            self.get_expr().write(int_state, block)

    @staticmethod
    def write_declarations(declarations, block, assignment_block=None):
        """
        Writes all declarations into the block, considering multiple declarations for the same name.
        If assignment_block is not none, assignments will be written to the block.
        Assignments are
        :param declarations:
        :param block:
        :param assignment_block:
        :return:
        """
        declared_names = []
        line_ends = []

        if assignment_block is not None:
            tmp = declarations
            declarations = [d.children[0] for d in tmp]
            line_ends = [d.children[1] for d in tmp]

        for i in range(len(declarations)):
            d = declarations[i]
            first_name = d.get_name().string
            added_declarations = 0
            if first_name not in declared_names:
                block.append_line('')
                before_name = d.children[d.get_name().index - 1]
                if isinstance(before_name, Cmt):
                    before_name.write(None, block)
                block.append(first_name)
                if d.get_name().index + 1 < len(d.children):
                    after_name = d.children[d.get_name().index + 1]
                    if isinstance(after_name, Cmt):
                        block.append(' ')
                        after_name.write(None, block)
                declared_names.append(first_name)
                added_declarations += 1
            if d.get_expr() is None:
                for c in d.children:
                    if isinstance(c, VariableName) and c != first_name:
                        name = c.string
                        if name not in declared_names:
                            if added_declarations == 0:
                                block.append_line('')
                            else:
                                block.append(', ')

                            before_name = d.children[c.index - 1]
                            if isinstance(before_name, Cmt):
                                before_name.write(None, block)
                            block.append(name)
                            if c.index + 1 < len(d.children):
                                after_name = d.children[c.index + 1]
                                if isinstance(after_name, Cmt):
                                    block.append(' ')
                                    after_name.write(None, block)

                            declared_names.append(name)
                            added_declarations += 1

            if added_declarations > 0:
                block.append(' : ' + d.get_type().translated())
                if assignment_block is not None:
                    line_ends[i].write(None, block)
                else:
                    block.append(';')
                # type_comment = d.children[d.get_type().get_index() + 1]
                # if isinstance(type_comment, Cmt):
                #     type_comment.write(None, block)

        if assignment_block is not None:
            for d in declarations:
                d.write(None, assignment_block)
                if d.get_expr() is not None:
                    assignment_block.append(';')


Node.node_map['DECLARATION'] = Declaration


class GlobalVariable(Node):
    def write(self, int_state, block=None):
        assert False


Node.node_map['GLOBAL'] = GlobalVariable


class Constant(Node):
    def write(self, int_state, block=None):
        name = self.children[1].translated()
        value = self.children[3].translated()
        if value == '=':
            name = self.children[2].translated()
            value = self.children[4].translated()
        int_state.constants.append_line(name + ' = ' + value + ';')


Node.node_map['CONSTANT'] = Constant
