from src.syntax_tree import *


def translate_string(string):
    result = ''
    try:
        escape = False
        for char in string:
            if escape:
                escape = False
                if char == '\\':
                    result += char
                else:
                    escape_table = {
                        '"': '"',
                        '\\': '\\',
                        'n': '\'#13#10\''
                    }
                    result += escape_table[char]
            else:
                if char == '\\':
                    escape = True
                elif char == '\'':
                    result += '\'\''
                else:
                    result += char
    except KeyError:
        print('Could not translate string literal:')
        print(string)

    return result


class Literal(Leaf):
    def translated(self):
        if self.string[0] == '"':
            return '\'' + translate_string(self.string[1:-1]) + '\''
        return self.string


Node.node_map['LITERAL'] = Literal
