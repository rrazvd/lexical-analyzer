from cursor import Cursor
from symbol_table import SymbolTable
from token import Token
from constants import reserved_words, delimiters, letter, digit, string_ascii, letter_digit_under


class LexicalAnalyzer():
    def __init__(self, code):
        self.tokens = []
        self.errors = []
        self.code = code
        self.is_comment_open = False
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
                    self.is_comment_open = False
                    return
                else:
                    self.is_comment_open = True
                    lexeme = ''
            self.cursor.forward()

    def analyze_id_or_word(self, line, line_count):
        lexeme = ''
        start = self.cursor.get_position()
        while self.cursor.get_position() < len(line):
            char = line[self.cursor.get_position()]
            if (letter_digit_under.match(char)):
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
            if (char == '/' or char == '*'):
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

    def analyze_string(self, line):
        lexeme = ''
        self.cursor.forward()
        start = self.cursor.get_position()
        while self.cursor.get_position() < len(line):
            char = line[self.cursor.get_position()]
            if (char == '\\'):  # if find \
                look_ahead_char = line[(self.cursor.get_position() + 1)]
                if (look_ahead_char == '\"'):  # check if \"
                    lexeme += look_ahead_char
                    self.cursor.forward()
                elif (look_ahead_char == '\\'):  # check if \\
                    lexeme += char
                    self.cursor.forward()
            elif (string_ascii.match(char)):
                lexeme += char
            elif (char == '\"'):
                return Token('literal', "\"" + lexeme + "\"")
            self.cursor.forward()

    def add_token(self, token):
        if(token != None):
            self.tokens.append(token)

    def get_tokens(self):
        return self.tokens

    def get_symbol_table(self):
        return self.symbol_table.get_table()

    def start_analyze(self):
        line_count = 1
        """ iterate lines  """
        for line in self.code:
            """ checks if not have an open comment """
            if (not self.is_comment_open):
                while self.cursor.get_position() < len(line):
                    char = line[self.cursor.get_position()]
                    if (letter.match(char)):  # id or word
                        token = self.analyze_id_or_word(line, line_count)
                        self.add_token(token)
                        self.cursor.backward()
                    elif (char == '/'):  # comments delimiters or / operator
                        token = self.analyze_comments_delimiters(line)
                        self.add_token(token)
                    elif (delimiters.match(char)):  # delimiters
                        self.add_token(Token(char, ''))
                    elif (digit.match(char)):
                        self.add_token(Token('digit', char))
                    elif (char == '\"'):  # strings
                        token = self.analyze_string(line)
                        self.add_token(token)

                    self.cursor.forward()
            else:
                """ search for the end comment """
                self.find_end_block_comment(line)

            """ next line count """
            line_count += 1
            """ set cursor to line begin """
            self.cursor.to_start()

        return self
