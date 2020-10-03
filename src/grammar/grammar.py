from pyleri import *

WORD = '[a-zA-Z_][a-zA-Z_0-9]*'
STRING = '"(\\\\.|[^"\\\\])*"'
NUMBER = '[+-]?([0-9]*[.])?[0-9]+'

seq = Sequence
opt = Optional


class CLike(Grammar):
    VARIABLE_NAME = Regex(WORD)
    TYPE = Regex(WORD)
    STRING_LITERAL = Regex(STRING)
    NUMBER_LITERAL = Regex(NUMBER)
    LITERAL = Choice(STRING_LITERAL, NUMBER_LITERAL)
    EXPRESSION = Ref()
    STATEMENT = Ref()
    STATEMENT_BLOCK = seq('{', Repeat(seq(STATEMENT, ';')), '}')
    DECLARATION = seq(TYPE, VARIABLE_NAME, opt(seq('=', EXPRESSION)))
    GLOBAL = seq(DECLARATION, ';')
    CONSTANT = seq(Keyword('const'), VARIABLE_NAME, '=', LITERAL, ';')

    PARAMETER = seq(TYPE, VARIABLE_NAME)
    PARAMETER_LIST = opt(seq(Repeat(seq(PARAMETER, ',')), PARAMETER))
    FUNCTION_NAME = Regex(WORD)
    FUNCTION = seq(TYPE, FUNCTION_NAME, '(', PARAMETER_LIST, ')', STATEMENT_BLOCK)

    ARRAY = seq(VARIABLE_NAME, '[', EXPRESSION, ']')
    VARIABLE = Choice(ARRAY, VARIABLE_NAME)

    EXPRESSION = Prio(
        LITERAL,
        VARIABLE,
        seq('!', THIS),
        seq('-', THIS),
        seq('(', THIS, ')'),
        seq(THIS, '*', THIS),
        seq(THIS, '/', THIS),
        seq(THIS, '%', THIS),
        seq(THIS, '+', THIS),
        seq(THIS, '-', THIS),
        seq(THIS, '<', THIS),
        seq(THIS, '>', THIS),
        seq(THIS, '<=', THIS),
        seq(THIS, '>=', THIS),
        seq(THIS, '==', THIS),
        seq(THIS, '!=', THIS),
        seq(THIS, '&&', THIS),
        seq(THIS, '||', THIS),
        seq(FUNCTION_NAME, '(', opt(seq(Repeat(seq(THIS, ',')), THIS)), ')'),
    )

    ASSIGNMENT = seq(VARIABLE, '=', EXPRESSION)

    ELSE = seq(Keyword('else'), Choice(STATEMENT_BLOCK, seq(STATEMENT, ';')))
    IF = seq(Keyword('if'), EXPRESSION, Choice(STATEMENT_BLOCK, seq(STATEMENT, ';')), opt(ELSE))
    WHILE = seq(Keyword('while'), '(', EXPRESSION, ')', Choice(STATEMENT_BLOCK, seq(STATEMENT, ';')))
    FOR = seq(Keyword('for'), '(', STATEMENT, ';', EXPRESSION, ';', STATEMENT, ')',
              Choice(STATEMENT_BLOCK, seq(STATEMENT, ';')))

    STATEMENT = Choice(
        seq(FUNCTION_NAME, '(', opt(seq(Repeat(seq(EXPRESSION, ',')), EXPRESSION)), ')'),
        ASSIGNMENT, DECLARATION, IF, WHILE, FOR)

    PROGRAM_PART = Choice(CONSTANT, GLOBAL, FUNCTION)

    START = Repeat(PROGRAM_PART)
