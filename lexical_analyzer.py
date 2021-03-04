from cursor import Cursor
from symbol_table import SymbolTable
from token import Token
import re

reserved_words = ['var', 'const', 'typedef', 'struct',
                  'extends', 'procedure', 'function', 'start',
                  'return', 'if', 'else', 'then', 'while', 'read',
                  'print', 'int', 'real', 'boolean', 'string', 'true',
                  'false', 'global', 'local']

delimiters = [';', ',', '(', ')', '{', '}', '[', ']', '.']
letter = re.compile(r'[a-zA-Z]')
letter_or_digit_or_under = re.compile(r'[a-zA-Z0-9_]')


class LexicalAnalyzer():
    def __init__(self, code):
        self.tokens = []
        self.errors = []
        self.code = code
        self.isCommentOpen = False
        self.cursor = Cursor()
        self.symbol_table = SymbolTable()
        self.symbol_table.add_words(reserved_words)

    def find_end_block_comment(self, line):
        lexeme = ''
        while self.cursor.get_position() < len(line):
            char = line[self.cursor.get_position()]
            if (char == '*'):
                lexeme += char
            elif (char == '/'):
                if (lexeme == '*'):
                    lexeme += char
            else:
                if (lexeme == '*/'):
                    self.isCommentOpen = False
                    return
                else:
                    self.isCommentOpen = True
                    lexeme = ''
            self.cursor.forward()

    def analyze_id_or_word(self, line, line_count):
        lexeme = ''
        start = self.cursor.get_position()
        while self.cursor.get_position() < len(line):
            char = line[self.cursor.get_position()]
            if (letter_or_digit_or_under.match(char)):
                lexeme += char
            else:
                return self.symbol_table.get_token(
                    lexeme, line_count, start, self.cursor.get_position())
            self.cursor.forward()

    def analyze_comments_delimiters(self, line):
        lexeme = ''
        start = self.cursor.get_position()
        while self.cursor.get_position() < len(line):
            char = line[self.cursor.get_position()]
            if (char == '/'):
                lexeme += char
            elif (char == '*'):
                lexeme += char
            else:
                if (lexeme == '/'):
                    return Token(lexeme, '')
                elif (lexeme == '//'):
                    self.cursor.set_position(len(line))
                    return
                elif (lexeme == '/*'):
                    self.find_end_block_comment(line)
            self.cursor.forward()

    def start_analyze(self):
        line_count = 1
        """ iterate lines  """
        for line in self.code:
            """ checks if not have an open comment """
            if (not self.isCommentOpen):
                while self.cursor.get_position() < len(line):
                    char = line[self.cursor.get_position()]
                    if (letter.match(char)):  # id or word
                        token = self.analyze_id_or_word(line, line_count)
                        if (token != None):
                            self.cursor.backward()
                            self.tokens.append(token)
                    elif (char == '/'):  # comments delimiters or / operator
                        token = self.analyze_comments_delimiters(line)
                        if (token != None):
                            self.tokens.append(token)
                    elif (char in delimiters):  # delimiters
                        self.tokens.append(Token(char, ''))

                    self.cursor.forward()
            else:
                """ search for the end comment """
                self.find_end_block_comment(line)

            """ next line count """
            line_count += 1
            """ set cursor to line begin """
            self.cursor.to_start()

        return self

    def get_tokens(self):
        return self.tokens

    def get_symbol_table(self):
        return self.symbol_table.get_table()
