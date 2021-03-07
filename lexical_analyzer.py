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
                    return True
                else:
                    self.is_comment_open = True
                    lexeme = ''
            self.cursor.forward()

    def analyze_comments_delimiters(self, line):
        lexeme = ''
        start = self.cursor.get_position()
        while self.cursor.get_position() < len(line):
            char = line[self.cursor.get_position()]
            if (char == '/' or char == '*'):
                lexeme += char
            else:
                """ if (lexeme == '/'):
                    return Token(lexeme, '') """
                if (lexeme == '//'):
                    self.cursor.set_position(len(line))
                    return
                elif (lexeme == '/*'):
                    return self.find_end_block_comment(line)
            self.cursor.forward()

    def analyze_id_or_word(self, line, line_count):
        start = self.cursor.get_position()
        lexeme = line[start]
        while self.cursor.get_look_ahead() < len(line):
            look_ahead_char = line[self.cursor.get_look_ahead()]
            if (letter_digit_under.match(look_ahead_char)):
                lexeme += look_ahead_char
            else:
                return self.symbol_table.get_token(
                    lexeme, (line_count + 1, start))
            self.cursor.forward()

        return self.symbol_table.get_token(
            lexeme, (line_count + 1, start))

    def analyze_numbers(self, line, line_count):
        start = self.cursor.get_position()
        lexeme = line[start]
        while self.cursor.get_look_ahead() < len(line):
            look_ahead_char = line[self.cursor.get_look_ahead()]
            if (digit.match(look_ahead_char)):
                lexeme += look_ahead_char
            elif (look_ahead_char == '.'):
                double_look_ahead_char = line[(
                    self.cursor.get_double_look_ahead())]
                if (digit.match(double_look_ahead_char)):
                    lexeme += look_ahead_char
            else:
                return Token('number', lexeme)
            self.cursor.forward()
        return Token('number', lexeme)

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
        return self.symbol_table

    def start_analyze(self):
        line_count = 0
        """ iterate lines  """
        while line_count < len(self.code):
            line = self.code[line_count]
            """ checks if not have an open comment """
            if (not self.is_comment_open):
                while self.cursor.get_position() < len(line):
                    flag = False
                    char = line[self.cursor.get_position()]
                    if (letter.match(char)):  # identifiers or words
                        token = self.analyze_id_or_word(line, line_count)
                        self.add_token(token)
                    elif (digit.match(char)):  # numbers
                        token = self.analyze_numbers(line, line_count)
                        self.add_token(token)
                    elif (char == '\"'):  # strings
                        token = self.analyze_string(line)
                        self.add_token(token)
                    elif (char == '/'):  # comments delimiters or / operator
                        flag = self.analyze_comments_delimiters(line)
                    elif (delimiters.match(char)):  # delimiters
                        self.add_token(Token(char, ''))
                    elif (char == '*'):  # *
                        self.add_token(Token(char, ''))
                    elif (char == '+'):  # + or ++
                        self.add_token(Token(char, ''))
                    elif (char == '-'):  # - or --
                        self.add_token(Token(char, ''))
                    elif (char == '='):  # = or ==
                        self.add_token(Token(char, ''))
                    elif (char == '>'):  # > or >=
                        self.add_token(Token(char, ''))
                    elif (char == '<'):  # < or <=
                        self.add_token(Token(char, ''))
                    elif (char == '!'):  # ! or !=
                        self.add_token(Token(char, ''))
                    elif (char == ' ' or char == '\t' or char == '\n'):  # space, tab and line break
                        pass
                    else:
                        print('invalid character on line ' + str(line_count + 1) +
                              ' column ' + str(self.cursor.get_position()) + ': ' + char)

                    self.cursor.forward()

                if (not flag):
                    line_count += 1
                    self.cursor.to_start()

            else:
                """ search for the end comment """
                if (not self.find_end_block_comment(line)):
                    line_count += 1
                    self.cursor.to_start()

        return self
