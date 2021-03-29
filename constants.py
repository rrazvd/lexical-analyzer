"""
This file has all the constants used by the lexical analyzer.
"""

import re

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