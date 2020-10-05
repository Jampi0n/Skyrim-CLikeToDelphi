import re
from enum import Enum


class ReadState(Enum):
    NORMAL = 1
    STRING = 2
    SINGLE_COMMENT = 3
    MULTI_COMMENT = 4


def remove_comments(code):
    state = ReadState.NORMAL
    escape = False
    result = ''
    i = 0
    while i < (len(code)):
        c = code[i]
        if state == ReadState.NORMAL:
            if c == '"':
                state = ReadState.STRING
                escape = False
            if i + 1 < len(code):
                if c + code[i + 1] == '//':
                    state = ReadState.SINGLE_COMMENT
                    i += 2
                    continue
                if c + code[i + 1] == '/*':
                    state = ReadState.MULTI_COMMENT
                    i += 2
                    continue
            result += c
        elif state == ReadState.STRING:
            if escape:
                escape = False
            else:
                if c == '"':
                    state = ReadState.NORMAL
                if c == '\\':
                    escape = True
            result += c
        elif state == ReadState.SINGLE_COMMENT:
            if c == '\n':
                state = ReadState.NORMAL
                result += c
        elif state == ReadState.MULTI_COMMENT:
            if i + 1 < len(code):
                if c + code[i + 1] == '*/':
                    state = ReadState.NORMAL
                    i += 1
        i += 1
    return result


class PreProcess:
    def __init__(self, in_string):
        self.string = in_string

    def pre_process(self):
        """
        Extracts the header and removes all comments.
        :return:
        """
        multi_line = '/\\*[^*]*\\*+(?:[^/*][^*]*\\*+)*/'
        description = re.search(multi_line, self.string).group(0)
        unit = re.search('\\n\\s*// unit .*', self.string).group(0)

        self.string = remove_comments(self.string)

        header = '{' + description[2:-2] + '}\n\n' + unit[5:] + ';\n\n'
        return header, self.string
