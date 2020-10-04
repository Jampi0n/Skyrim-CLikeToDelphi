import re


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

        self.string = re.sub(multi_line, '', self.string)
        self.string = re.sub('\\n\\s*//.*', '', self.string)

        header = '{' + description[2:-2] + '}\n\n' + unit[5:] + ';\n\n'
        return header, self.string
