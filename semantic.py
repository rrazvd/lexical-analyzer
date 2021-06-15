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
            token_error = Token(Errors.SEMANTIC_ERROR.value, '- DUPLICIDADE DE IDENTIFICADOR: \'' +
                                key_id + '\'', token_id.get_pos())
            self.semantic_tokens.append(token_error)

    def add_const(self, token_type, token_id):
        key_id = token_id.get_attribute()
        if (key_id not in self.scope_table[self.scope]):
            self.scope_table[self.scope][token_id.get_attribute()] = {'variant': 'const',
                                                                      'type': token_type.get_attribute()}
        else:
            token_error = Token(Errors.SEMANTIC_ERROR.value, '- DUPLICIDADE DE IDENTIFICADOR: \'' +
                                key_id + '\'', token_id.get_pos())
            self.semantic_tokens.append(token_error)

    def add_struct(self, token_id):
        key_id = token_id.get_attribute()
        if (key_id not in self.scope_table):
            self.set_scope(key_id)
        else:
            self.set_scope("@repeated_" + key_id)
            token_error = Token(Errors.SEMANTIC_ERROR.value, '- DUPLICIDADE DE IDENTIFICADOR: \'' +
                                key_id + '\'', token_id.get_pos())
            self.semantic_tokens.append(token_error)

    def add_typedef_struct(self, token_id, extends_id):
        key_id = token_id.get_attribute()
        if (key_id not in self.scope_table):
            self.set_scope(key_id)
            if(extends_id != None):
                key_extends_id = extends_id.get_attribute()
                if (key_extends_id in self.scope_table):
                    self.scope_table[key_id] = self.scope_table[key_extends_id]
            self.scope_table[key_id].update(
                self.scope_table['@temporary_scope'])
            self.scope_table.pop('@temporary_scope', None)
        else:
            self.scope_table.pop('@temporary_scope', None)
            token_error = Token(Errors.SEMANTIC_ERROR.value, '- DUPLICIDADE DE IDENTIFICADOR: \'' +
                                key_id + '\'', token_id.get_pos())
            self.semantic_tokens.append(token_error)

    def add_func(self, token_id, params):
        if (token_id != None):
            scope_name = token_id.get_attribute()
            if (params != None):
                for param in params:
                    scope_name += '@' + param[0].get_attribute()

            if (scope_name not in self.scope_table):
                self.set_scope(scope_name)
                if (params != None):
                    for param in params:
                        self.add_var(param[0], param[1])
            else:
                self.set_scope("@repeated_" + scope_name)
                token_error = Token(Errors.SEMANTIC_ERROR.value, '- DUPLICIDADE DE IDENTIFICADOR: \'' +
                                    scope_name + '\'', token_id.get_pos())
                self.semantic_tokens.append(token_error)

    def add_proc(self, token_id, params):
        if (token_id != None):
            scope_name = token_id.get_attribute()
            if (params != None):
                for param in params:
                    scope_name += '@' + param[0].get_attribute()

            if (scope_name not in self.scope_table):
                self.set_scope(scope_name)
                if (params != None):
                    for param in params:
                        self.add_var(param[0], param[1])
            else:
                self.set_scope("@repeated_" + scope_name)
                token_error = Token(Errors.SEMANTIC_ERROR.value, '- DUPLICIDADE DE IDENTIFICADOR: \'' +
                                    scope_name + '\'', token_id.get_pos())
                self.semantic_tokens.append(token_error)

    def check_identifier(self, token_id):
        key_id = token_id.get_attribute()
        if (key_id not in self.scope_table and not self.check_partial_keys(self.scope_table, (key_id + '@'))):
            if (key_id not in self.scope_table[self.scope] and key_id not in self.scope_table['global']):
                token_error = Token(Errors.SEMANTIC_ERROR.value, '- IDENTIFICADOR NÃO DECLARADO: \'' +
                                    key_id + '\'', token_id.get_pos())
                self.semantic_tokens.append(token_error)

    def check_identifier_access(self, token_id, token_access):
        key_access = token_access.get_attribute()
        key_id = token_id.get_attribute()

        if (key_access == 'local'):
            if (key_id not in self.scope_table[self.scope]):
                token_error = Token(Errors.SEMANTIC_ERROR.value, '- IDENTIFICADOR NÃO DECLARADO: \'' +
                                    key_id + '\'', token_id.get_pos())
                self.semantic_tokens.append(token_error)
        elif (key_access == 'global'):
            if (key_id not in self.scope_table[key_access]):
                token_error = Token(Errors.SEMANTIC_ERROR.value, '- IDENTIFICADOR NÃO DECLARADO: \'' +
                                    key_id + '\'', token_id.get_pos())
                self.semantic_tokens.append(token_error)
        else:
            if (key_id not in self.scope_table[key_access]):
                token_error = Token(Errors.SEMANTIC_ERROR.value, '- IDENTIFICADOR NÃO DECLARADO: \'' +
                                    key_id + '\'', token_id.get_pos())
                self.semantic_tokens.append(token_error)

    def check_partial_keys(self, _dict, sbstr):
        for key in _dict.keys():
            if (sbstr in key):
                return True
        return False

    def get_tokens(self):
        return self.semantic_tokens
