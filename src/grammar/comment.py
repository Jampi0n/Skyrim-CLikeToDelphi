from src.syntax_tree import *


class Comment(Node):

    def __init__(self, parent, start, end, name, element, string):
        super().__init__(parent, start, end, name, element, string)

    def translated(self):
        if self.string[0:2] == '/*':
            return '{' + self.string[2:-2] + '}'
        return self.string

    def write(self, int_state, block):
        block.append_line(self.translated())


Node.node_map['COMMENT'] = Comment
