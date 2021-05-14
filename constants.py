"""
This file has all the constants used by the compiler.
"""

import re
from enum import Enum

reserved_words = ['var', 'const', 'typedef', 'struct',
                  'extends', 'procedure', 'function', 'start',
                  'return', 'if', 'else', 'then', 'while', 'read',
                  'print', 'int', 'real', 'boolean', 'string', 'true',
                  'false', 'global', 'local']

delimiters = re.compile(r'[;\,\(\)\{\}\[\]\.]')  # ; , ( ) { } [ ] .
letter = re.compile(r'[a-zA-Z]')  # A - Z
digit = re.compile(r'[0-9]')  # 0 - 9
letter_digit_under = re.compile(r'[a-zA-Z0-9_]')  # letter | digit | _
# space, !, # - [, ] - ~
string_ascii = re.compile(r'[\x20\x21\x23-\x5B\x5D-\x7E]')
arithmetic_operators = re.compile(r'\+|\-|\*|\/')  # + - * /
relational_operators = re.compile(r'==|!=|>|>=|<|<=|=')  # == != > >= < <= =
errors_name = ['SIB', 'OpMF', 'CMF', 'NMF', 'CoMF']

'''
This enum contains tokens names.
'''


class Tokens(Enum):
    KEYWORD = 'PRE'
    IDENTIFIER = "IDE"
    NUMBER = 'NRO'
    DELIMITER = "DEL"
    OP_RELATIONAL = 'REL'
    OP_LOGICAL = 'LOG'
    OP_ARITHMETIC = 'ART'
    INVALID_SYMBOL = 'SIB'
    STRING = 'CAD'


'''
This enum contains errors tokens names.
'''


class Errors(Enum):
    MF_NUMBER = 'NMF'
    MF_COMMENT = 'CoMF'
    MF_OPERATOR = 'OpMF'
    MF_STRING = 'CMF'


class Firsts(Enum):
    DECLS = ['function', 'procedure']
    PARAM_TYPE = ['int', 'real', 'boolean', 'string', 'struct', 'IDE']
    STRUCT_BLOCK = ['struct', 'typedef']
    VAR_DECLS = ['int', 'real', 'boolean',
                 'string', 'struct', 'typedef', 'IDE']
    VAR_STM = ['local', 'global', 'IDE', 'print', 'read']
    STM_SCOPE = ['local', 'global']
    STM_CMD = ['print', 'read']
    STM_ID = ['=', '++', '--', '[', '.', '(']
    CONST_DECLS = VAR_DECLS
    TYPE = ['int', 'real', 'boolean', 'string', 'struct']
    VAR_LIST = [',', '=', ';']
    CONST_LIST = [',', ';']
    DECL_ATRIBUTE = ['{', '!', 'NRO', 'CAD',
                     'true', 'false', 'IDE', 'local', 'global' '(']
    EXPR = ['!', '-', 'NRO', 'CAD', 'true',
            'false', 'IDE', 'local', 'global', '(']
    VALUE = ['-', 'NRO', 'CAD', 'true', 'false', 'IDE', 'local', 'global', '(']
    LOG_EXPR = ['!', 'NRO', 'CAD', 'true',
                'false', 'IDE', 'local', 'global', '(']
    LOG_VALUE = ['NRO', 'CAD', 'true', 'false', 'IDE', 'local', 'global', '(']
    INDEX = ['IDE', 'NRO']
    ARRAY_DEF = EXPR
    FUNC_STM = ['if', 'while', '{', 'IDE', 'local',
                'global', 'print', 'read', 'return']
    FUNC_STMS = ['if', 'while', '{', 'IDE', 'local',
                 'global', 'print', 'read', 'return']
    FUNC_NORMAL_STM = ['{', 'IDE', 'local',
                       'global', 'print', 'read', ';', 'return']
    ASSIGN = ['=', '++', '--']
    ARGS = EXPR
    EQUATE_ = ['==', '!=']
    COMPARE_ = ['<', '>', '<=', '>=']
    ADD_ = ['+', '-']
    MULT_ = ['*', '/']
    ID_VALUE = ['[', '(', '.']


class Follows(Enum):
    START_BLOCK = ['function', 'procedure']
