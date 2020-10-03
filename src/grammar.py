from pyleri import *

WORD = '[a-zA-Z_][a-zA-Z_0-9]*'
STRING = '"(\\\\.|[^"\\\\])*"'
NUMBER = '[+-]?([0-9]*[.])?[0-9]+'


class CLike(Grammar):
    VARIABLE_NAME = Regex(WORD)
    TYPE = Regex(WORD)
    STRING_LITERAL = Regex(STRING)
    NUMBER_LITERAL = Regex(NUMBER)
    LITERAL = Choice(STRING_LITERAL, NUMBER_LITERAL)
    EXPRESSION = Ref()
    STATEMENT = Ref()
    STATEMENT_BLOCK = Sequence('{', Repeat(STATEMENT), '}')
    DECLARATION = Sequence(TYPE, VARIABLE_NAME, Optional(Sequence('=', EXPRESSION)))
    GLOBAL = Choice(DECLARATION)
    CONSTANT = Sequence(Keyword('const'), VARIABLE_NAME, '=', LITERAL)

    PARAMETER = Sequence(TYPE, VARIABLE_NAME)
    PARAMETER_LIST = Prio(Sequence(THIS, ',', PARAMETER), PARAMETER)
    FUNCTION_NAME = Regex(WORD)
    FUNCTION_BODY = Choice(STATEMENT_BLOCK)
    FUNCTION = Sequence(TYPE, FUNCTION_NAME, '(', Optional(PARAMETER_LIST), ')', FUNCTION_BODY)

    ARGUMENT = Choice(EXPRESSION)
    ARGUMENT_LIST = Ref()
    ARGUMENT_LIST = Choice(Sequence(ARGUMENT_LIST, ',', ARGUMENT), ARGUMENT)
    FUNCTION_CALL = Sequence(FUNCTION_NAME, '(', Optional(ARGUMENT_LIST), ')')

    ARRAY = Sequence(VARIABLE_NAME, '[', EXPRESSION, ']')
    VARIABLE = Choice(ARRAY, VARIABLE_NAME)
    EXPRESSION = Prio(Sequence('(', THIS, ')'), Sequence(Tokens('- !'), THIS),
                      Sequence(THIS, Tokens('<= >= == != > < + - * /'), THIS), LITERAL)
    ASSIGNMENT = Sequence(VARIABLE, '=', EXPRESSION)

    ELSE = Sequence(Keyword('else'), Choice(STATEMENT_BLOCK, STATEMENT))
    IF = Sequence(Keyword('if'), EXPRESSION, Choice(STATEMENT_BLOCK, STATEMENT), Optional(ELSE))
    WHILE = Sequence(Keyword('while'), '(', EXPRESSION, ')', Choice(STATEMENT_BLOCK, STATEMENT))
    FOR = Sequence(Keyword('for'), '(', STATEMENT, EXPRESSION, STATEMENT, ')', Choice(STATEMENT_BLOCK, STATEMENT))

    STATEMENT = Choice(FUNCTION_CALL, ASSIGNMENT, DECLARATION, IF, WHILE, FOR)

    PROGRAM_PART = Choice(CONSTANT, GLOBAL, FUNCTION)

    START = Repeat(PROGRAM_PART)
