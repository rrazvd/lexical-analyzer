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

delimiters = re.compile(r'[;\,\(\)\{\}\[\]\.]') # ; , ( ) { } [ ] .
letter = re.compile(r'[a-zA-Z]') # A - Z
digit = re.compile(r'[0-9]')  # 0 - 9
letter_digit_under = re.compile(r'[a-zA-Z0-9_]') # letter | digit | _
string_ascii = re.compile(r'[\x20\x21\x23-\x5B\x5D-\x7E]') # space, !, # - [, ] - ~
arithmetic_operators = re.compile(r'\+|\-|\*|\/') # + - * /
relational_operators = re.compile(r'==|!=|>|>=|<|<=|=') # == != > >= < <= =
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
    VAR_DECLS = ['int', 'real', 'boolean', 'string', 'struct', 'typedef','IDE']
    CONST_DECLS = VAR_DECLS
    TYPE = ['int', 'real', 'boolean', 'string', 'struct']
    VAR_LIST = [',', '=', ';']
    CONST_LIST = [',', ';']
    DECL_ATRIBUTE = ['{', '!', 'NRO', 'CAD', 'LOG', 'IDE', '(' ]
    EXPR = ['!', 'NRO', 'CAD', 'LOG', 'IDE', '(' ] # need check
    ARRAY_DEF = EXPR
 
class Follows(Enum):
    START_BLOCK = ['function', 'procedure']    