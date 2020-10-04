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
    STATEMENT_BLOCK = seq('{', Repeat(STATEMENT), '}')
    DECLARATION = seq(TYPE, VARIABLE_NAME, opt(Choice(seq('=', EXPRESSION), Repeat(seq(',', VARIABLE_NAME)))))
    GLOBAL = seq(DECLARATION, ';')
    CONSTANT = seq(Keyword('const'), opt(TYPE), VARIABLE_NAME, '=', LITERAL, ';')

    # PREFIX = Repeat(seq(EXPRESSION, '.'))

    PARAMETER = seq(TYPE, VARIABLE_NAME)
    PARAMETER_LIST = opt(seq(Repeat(seq(PARAMETER, ',')), PARAMETER))

    FUNCTION_NAME = Regex(WORD)
    FUNCTION = seq(TYPE, FUNCTION_NAME, '(', PARAMETER_LIST, ')', STATEMENT_BLOCK)
    EXPRESSION = Prio(
        LITERAL,
        VARIABLE_NAME,
        seq('!', THIS),
        seq('-', THIS),

        seq(THIS, '[', THIS, ']'),
        seq(THIS, '(', opt(seq(Repeat(seq(THIS, ',')), THIS)), ')'),  # Repeat(seq(THIS, '.')),
        seq('(', THIS, ')'),
        seq(THIS, '.', THIS),
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
    )

    ASSIGNMENT_OP = Tokens('= += -= *= /=')
    ASSIGNMENT = seq(EXPRESSION, ASSIGNMENT_OP, EXPRESSION)

    ELSE = seq(Keyword('else'), Choice(STATEMENT_BLOCK, STATEMENT))
    IF = seq(Keyword('if'), '(', EXPRESSION, ')', Choice(STATEMENT_BLOCK, STATEMENT), opt(ELSE))
    WHILE = seq(Keyword('while'), '(', EXPRESSION, ')', Choice(STATEMENT_BLOCK, STATEMENT))
    FOR = seq(Keyword('for'), '(', Choice(DECLARATION, ASSIGNMENT), ';', EXPRESSION, ';', ASSIGNMENT, ')',
              Choice(STATEMENT_BLOCK, STATEMENT))

    CATCH = seq(Keyword('catch'), '(', PARAMETER, ')', Choice(STATEMENT_BLOCK, STATEMENT))
    FINALLY = seq(Keyword('finally'), Choice(STATEMENT_BLOCK, STATEMENT))
    TRY = seq(Keyword('try'), Choice(STATEMENT_BLOCK, STATEMENT), opt(CATCH), opt(FINALLY))

    EXPRESSION_STATEMENT = seq(EXPRESSION, ';')

    THROW = seq(Keyword('throw'), EXPRESSION, ';')

    CONTINUE = seq(Keyword('continue'), ';')
    BREAK = seq(Keyword('break'), ';')

    STATEMENT = Choice(THROW, EXPRESSION_STATEMENT, seq(ASSIGNMENT, ';'), seq(DECLARATION, ';'), IF, WHILE, FOR, TRY,
                       CONTINUE, BREAK)

    PROGRAM_PART = Choice(CONSTANT, GLOBAL, FUNCTION)

    START = Repeat(PROGRAM_PART)
