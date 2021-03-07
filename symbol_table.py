from token import Token
import json


class SymbolTable():
    def __init__(self):
        self.__table = {}

    def add_words(self, words):
        for w in words:
            self.__table[w] = {"type": "word", 'pos': []}

    def get_table(self):
        return self.__table

    def get_token(self, lexeme, pos):
        if lexeme in self.__table:
            _type = self.__table[lexeme]['type']
            if _type == 'word':
                self.__table[lexeme]['pos'].append(pos)
                return Token(lexeme, '')
            elif _type == 'identifier':
                self.__table[lexeme]['pos'].append(pos)
                return Token(_type, lexeme)
        else:
            self.__table[lexeme] = {'type': 'identifier', 'pos': [pos]}
            return Token(self.__table[lexeme]['type'], lexeme)

    def to_string(self):
        return json.dumps(self.__table, default=lambda x: x.__dict__, ensure_ascii=False, indent=4)
