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
    SYNTAX_ERROR = 'ERRO SINTÁTICO'
    SEMANTIC_ERROR = 'ERRO SEMÂNTICO'


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
    STRUCTS = ['const', 'var', 'procedure']  # ok
    START_BLOCK = ['function', 'procedure']  # ok
    DECL = ['function', 'procedure']  # ok
    STRUCT_BLOCK = ['struct', 'typedef', 'const', 'var', 'procedure']  # ok
    EXTENDS = ['{']  # ok
    CONST_BLOCK = ['var', 'procedure']  # ok
    VAR_BLOCK = ['}', 'procedure', 'if', 'while', 'return',
                 'IDE', 'local', 'global', 'print', 'read']  # ok
    TYPE = ['IDE']  # ok
    TYPEDEF = ['int', 'real', 'boolean', 'string', 'struct',
               'IDE', 'typedef', '}']  # const decl e var decl
    VAR_DECLS = ['}']  # ok
    VAR_DECL = ['int', 'real', 'boolean', 'string',
                'struct', 'IDE', 'typedef', '}']  # ok
    VAR = [',', '=', ';']  # ok
    VAR_LIST = ['int', 'real', 'boolean', 'string',
                'struct', 'IDE', 'typedef', '}']  # ok
    CONST_DECLS = ['}']  # ok
    CONST_DECL = ['int', 'real', 'boolean', 'string',
                  'struct', 'IDE', 'typedef', '}']  # ok
    CONST = [',', ';']  # ok
    CONST_LIST = ['int', 'real', 'boolean', 'string',
                  'struct', 'IDE', 'typedef', '}']  # ok
    DECL_ATRIBUTE = [',', '=', ';']  # ok
    ARRAY_DECL = [',', '=', ';']  # ok
    ARRAY_DEF = ['}']  # ok
    ARRAY_EXPR = ['}']  # ok
    ARRAY = ['[', '.', '=', '++', '--']  # ok
    INDEX = [']']  # ok
    ARRAYS = ['=', ',', ';', '.', '>', '<', '>=', '<=', '==',
              '!=', '+', '-', '*', '/', '||', '&&']  # s(accessES
    ASSIGN = ['if', 'while', 'print', 'read',
              'global', 'local', 'IDE', 'return', '}']
    ACCESS = ['.', '=', '++', '--', ';']
    ARGS = [')']  # ok
    ARGS_LIST = [')']  # ok
    FUNC_DECL = ['function', 'procedure']  # ok
    PROC_DECL = ['function', 'procedure']  # ok
    PARAM_TYPE = ['IDE']  # ok
    PARAMS = [')']  # ok
    PARAM = [',', ')']  # ok
    PARAMS_LIST = [')']  # ok
    PARAMS_ARRAYS = [',', ')']  # ok
    PARAM_MULT_ARRAYS = [',', ')']  # ok
    FUNC_BLOCK = ['function', 'procedure']  # ok
    FUNC_STMS = ['}']  # ok
    FUNC_STM = ['if', 'while', 'local', 'global',
                'IDE', 'print', 'read', 'return']  # ok
    ELSE_STM = ['if', 'while', 'local', 'global',
                'IDE', 'print', 'read', 'return']  # ok
    IF_STM = ['if', 'while', 'local', 'global',
              'IDE', 'print', 'read', 'return']  # ok
    WHILE_STM = ['if', 'while', 'local', 'global',
                 'IDE', 'print', 'read', 'return']  # ok
    VAR_STM = ['if', 'while', 'local', 'global',
               'IDE', 'print', 'read', 'return']  # ok
    STM_ID = ['if', 'while', 'local', 'global',
              'IDE', 'print', 'read', 'return']  # ok
    STM_SCOPE = ['if', 'while', 'local', 'global',
                 'IDE', 'print', 'read', 'return']  # ok
    STM_CMD = ['if', 'while', 'local', 'global',
               'IDE', 'print', 'read', 'return']  # ok
    EXPR = [',', '=', ';', '}', '[', ')']  # ok
    ID_VALUE = ['*', '/', '+', '-', '>', '<', '<=', '>=',
                '==', '!=', '&&', '||', '}', ']', ')', ',', ';']
    VALUE = ['*', '/', '+', '-', '>', '<', '<=', '>=',
             '==', '!=', '&&', '||', '}', ']', ')', ',', ';']
    LOG_VALUE = ['!=', '==', '&&', '||', '>', '<', '>=', '<=', ')']
