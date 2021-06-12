from constants import Errors
from token2 import Token

""" 
This Class implements a Semantic Analyzer.
"""


class Semantic ():

    def __init__(self, symbol_table):
        self.scope = 'global'
        self.semantic_tokens = []
        self.scope_table = symbol_table.get_scope_table()

    def set_scope(self, scope):
        self.scope = scope
        self.scope_table[scope] = {}

    def get_scope(self):
        return self.scope

    def add_var(self, token_type, token_id):
        key_id = token_id.get_attribute()
        if (key_id not in self.scope_table[self.scope]):
            self.scope_table[self.scope][key_id] = {'variant': 'var',
                                                    'type': token_type.get_attribute()}
        else:
            token_error = Token(Errors.SEMANTIC_ERROR.value, '- DUPLICIDADE DE IDENTIFICADOR: ' +
                                key_id + ' NO ESCOPO: ' + self.scope, token_id.get_pos())
            self.semantic_tokens.append(token_error)

    def add_const(self, token_type, token_id):
        key_id = token_id.get_attribute()
        if (key_id not in self.scope_table[self.scope]):
            self.scope_table[self.scope][token_id.get_attribute()] = {'variant': 'const',
                                                                      'type': token_type.get_attribute()}
        else:
            token_error = Token(Errors.SEMANTIC_ERROR.value, '- DUPLICIDADE DE IDENTIFICADOR: ' +
                                key_id + ' NO ESCOPO: ' + self.scope, token_id.get_pos())
            self.semantic_tokens.append(token_error)

    def get_tokens(self):
        return self.semantic_tokens
