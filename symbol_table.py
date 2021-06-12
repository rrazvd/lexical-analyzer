from token2 import Token
from constants import Tokens
import json

"""
This class represents a Symbol Table that contains info about identifiers and reserved words.
"""


class SymbolTable():
    def __init__(self, words):
        self.__table = {}
        self.__scope_table = {}
        self.add_words(words)

    def add_words(self, words):  # add reserverd words
        for w in words:
            self.__table[w] = {
                "keyword": Tokens.KEYWORD.value, 'occurrence': []}

    def get_table(self):  # returns dict table
        return self.__table

    def get_scope_table(self):  # returns dict scope table
        return self.__scope_table

    def get_token(self, lexeme, pos):
        if lexeme in self.__table:  # if the lexeme in the table
            _type = self.__table[lexeme]['keyword']
            if _type == Tokens.KEYWORD.value:  # if a reserved word
                self.__table[lexeme]['occurrence'].append(
                    pos)  # append position
                return Token(_type, lexeme, pos)  # return reserved word token
            elif _type == Tokens.IDENTIFIER.value:  # elif a identifier
                self.__table[lexeme]['occurrence'].append(
                    {'pos': pos})  # append position
                return Token(_type, lexeme, pos)  # return identifier token
        else:  # create identifier token
            self.__table[lexeme] = {
                'keyword': Tokens.IDENTIFIER.value, 'occurrence': [{'pos': pos}]}
            # return identifier token
            return Token(self.__table[lexeme]['keyword'], lexeme, pos)

    def to_string(self):  # returns a json string
        return json.dumps(self.__scope_table, default=lambda x: x.__dict__, ensure_ascii=False, indent=4)
