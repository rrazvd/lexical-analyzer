import re

reserved_words = ['var', 'const', 'typedef', 'struct',
                  'extends', 'procedure', 'function', 'start',
                  'return', 'if', 'else', 'then', 'while', 'read',
                  'print', 'int', 'real', 'boolean', 'string', 'true',
                  'false', 'global', 'local']

delimiters = re.compile(r'[;\,\(\)\{\}\[\]\.]')
letter = re.compile(r'[a-zA-Z]')
digit = re.compile(r'[0-9]')
letter_digit_under = re.compile(r'[a-zA-Z0-9_]')
string_ascii = re.compile(r'[\x20\x21\x23-\x5B\x5D-\x7E]')
