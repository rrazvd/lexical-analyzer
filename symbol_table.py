from token import Token
import json


class SymbolTable():
    def __init__(self, words):
        self.__table = {}
        self.add_words(words)

    def add_words(self, words):
        for w in words:
            self.__table[w] = {"type": "PRE", 'pos': []}

    def get_table(self):
        return self.__table

    def get_token(self, lexeme, pos):
        if lexeme in self.__table:
            _type = self.__table[lexeme]['type']
            if _type == 'PRE':
                self.__table[lexeme]['pos'].append(pos)
                return Token(_type, lexeme, pos)
            elif _type == 'IDE':
                self.__table[lexeme]['pos'].append(pos)
                return Token(_type, lexeme, pos)
        else:  # create identifier token
            self.__table[lexeme] = {'type': 'IDE', 'pos': [pos]}
            return Token(self.__table[lexeme]['type'], lexeme, pos)

    def to_string(self):
        return json.dumps(self.__table, default=lambda x: x.__dict__, ensure_ascii=False, indent=4)
