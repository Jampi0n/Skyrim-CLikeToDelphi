import re
from enum import Enum
from pathlib import Path


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


def resolve_import(import_path: str, start_dir: Path):
    import_path = import_path.strip()
    # relative paths
    if import_path[0:2] == './' or import_path[0:3] == '../':
        import_path = start_dir.joinpath(Path(import_path))
    return open(str(import_path), 'r').read() + '\n\n'


def pre_process(in_path):
    """
    Extracts the header and removes all comments.
    :return:
    """
    in_string = open(in_path, 'r').read()
    multi_line = '/\\*[^*]*\\*+(?:[^/*][^*]*\\*+)*/'
    description = re.search(multi_line, in_string).group(0)
    unit = re.search('\\n\\s*// unit .*', in_string).group(0)
    imports = re.findall('\\n\\s*// import .*', in_string)
    import_string = ''
    for i in imports:
        import_string += resolve_import(i.strip()[10:], in_path.parent)

    use_string = ''
    uses = re.findall('\\n\\s*// uses .*', in_string)
    for u in uses:
        use_string += 'uses ' + u.strip()[8:] + ';\n'
    if use_string != '':
        use_string += '\n\n'

    in_string = remove_comments(import_string + '\n\n' + in_string)

    header = '{' + description[2:-2] + '}\n\nunit ' + unit.strip()[8:] + ';\n\n' + use_string
    return header, in_string
