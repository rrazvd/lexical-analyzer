from token2 import Token
from constants import Tokens
import json

"""
This class represents a Symbol Table that contains info about identifiers and reserved words.
"""
class SymbolTable():
    def __init__(self, words):
        self.__table = {}
        self.add_words(words)

    def add_words(self, words): # add reserverd words
        for w in words:
            self.__table[w] = {"type": Tokens.KEYWORD, 'pos': []}

    def get_table(self): # returns dict table
        return self.__table

    def get_token(self, lexeme, pos):
        if lexeme in self.__table: # if the lexeme in the table
            _type = self.__table[lexeme]['type']
            if _type == Tokens.KEYWORD: # if a reserved word
                self.__table[lexeme]['pos'].append(pos) # append position
                return Token(_type, lexeme, pos) # return reserved word token
            elif _type == Tokens.IDENTIFIER: # elif a identifier
                self.__table[lexeme]['pos'].append(pos) # append position
                return Token(_type, lexeme, pos) # return identifier token
        else:  # create identifier token
            self.__table[lexeme] = {'type': Tokens.IDENTIFIER, 'pos': [pos]}
            return Token(self.__table[lexeme]['type'], lexeme, pos) # return identifier token

    def to_string(self): # returns a json string
        return json.dumps(self.__table, default=lambda x: x.__dict__, ensure_ascii=False, indent=4)
