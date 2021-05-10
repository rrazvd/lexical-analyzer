from enum import Enum

class Firsts(Enum):
    DECLS = ['function', 'procedure']
    PARAM_TYPE = ['int', 'real', 'boolean', 'string', 'struct', 'IDE']
    STRUCT_BLOCK = ['struct', 'typedef']
    VAR_DECLS = ['int', 'real', 'boolean', 'string', 'struct', 'typedef','id']
    TYPE = ['int', 'real', 'boolean', 'string', 'struct']
    VAR_LIST = [',', '=', ';']