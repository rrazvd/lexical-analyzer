from token import Token


class SymbolTable():
    def __init__(self):
        self.__table = {}

    def add_words(self, words):
        for w in words:
            self.__table[w] = {"type": "word"}

    def get_table(self):
        return self.__table

    def get_token(self, lexeme, line_count, start, end):
        if lexeme in self.__table:
            _type = self.__table[lexeme]['type']
            if _type == 'word':
                return Token(lexeme, '')
            elif _type == 'identifier':
                return Token(_type, lexeme)
        else:
            self.__table[lexeme] = {'type': 'identifier',
                                    'line': line_count, 'start': start, 'end': end}
            return Token(self.__table[lexeme]['type'], lexeme)
