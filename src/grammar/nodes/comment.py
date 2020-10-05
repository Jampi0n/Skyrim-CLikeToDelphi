from src.transpiler.syntax_tree import *
import re


class Comment(Node):
    def write(self, int_state, block=None):
        self.children[0].write(int_state, block)


Node.node_map['COMMENT'] = Comment


class CommentMulti(Node):
    def translated(self):
        string = self.string.replace('/*', '{', 1)
        string = (string[::-1].replace('/*', '}', 1))[::-1]
        return string

    def write(self, int_state, block=None):
        block.append(self.translated())


Node.node_map['COMMENT_MULTI'] = CommentMulti


class CommentSingle(Node):
    def translated(self):
        return self.string[:-1]

    def write(self, int_state, block=None):
        block.append(self.translated())


Node.node_map['COMMENT_SINGLE'] = CommentSingle


class Cmt(Node):
    def write(self, int_state, block=None):
        for c in self.children:
            c.write(int_state, block)


Node.node_map['CMT'] = Cmt


class LineEnd(Node):
    def translated(self):
        string = self.string
        string = re.sub('/\\*', '{', string)
        string = re.sub('\\*/', '}', string)
        return string

    def write(self, int_state, block=None):
        print('>> LINE_END >>')
        print(self.string)
        print('<< LINE_END <<')
        block.append(self.translated())


Node.node_map['LINE_END'] = LineEnd
