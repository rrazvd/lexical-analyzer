from cursor import Cursor
from symbol_table import SymbolTable
from token import Token
from constants import reserved_words, delimiters, letter, digit, string_ascii, letter_digit_under, arithmetic_operators, relational_operators


class LexicalAnalyzer():

    def __init__(self, code):
        self.code = code
        self.tokens = []
        self.line_count = 0
        self.is_comment_open = False
        self.cursor = Cursor()
        self.symbol_table = SymbolTable(reserved_words)
        self.start_analyze()

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

    """ analyze identifiers or reserved word lexemes """
    def analyze_id_or_word(self, line):
        start = self.cursor.get_position()
        lexeme = line[start]
        while self.cursor.get_look_ahead() < len(line):
            look_ahead_char = line[self.cursor.get_look_ahead()]
            if (letter_digit_under.match(look_ahead_char)):
                lexeme += look_ahead_char
            else:
                return self.symbol_table.get_token(
                    lexeme, (self.line_count, start))
            self.cursor.forward()

        return self.symbol_table.get_token(lexeme, (self.line_count, start))

    def analyze_numbers(self, line):
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
                return Token('NRO', lexeme, (self.line_count, start))
            self.cursor.forward()
        return Token('NRO', lexeme, (self.line_count, start))

    def analyze_string(self, line):
        start = self.cursor.get_position()
        lexeme = line[start]
        self.cursor.forward()
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
            elif (string_ascii.match(char)):  # check allowed ascii character
                lexeme += char
            elif (char == '\"'):  # check end of string
                lexeme += char
                return Token('CAD', lexeme, (self.line_count, start))
            else:
                return Token('CMF', lexeme, (self.line_count, start))
            self.cursor.forward()

    def analyze_next_char(self, line, next_char):
        start = self.cursor.get_position()
        lexeme = line[start]
        try:
            look_ahead_char = line[self.cursor.get_look_ahead()]
            if (look_ahead_char == next_char):
                self.cursor.forward()
                lexeme += look_ahead_char
                return Token(self.get_operator_type(lexeme), lexeme, (self.line_count, start))
            else:
                return Token(self.get_operator_type(lexeme), lexeme, (self.line_count, start))
        except(IndexError):
            return Token(get_operator_type(lexeme), lexeme, (self.line_count, start))

    def get_operator_type(self, lexeme):
        if (lexeme == '!'):
            return 'LOG'
        elif (arithmetic_operators.match(lexeme)):
            return 'ART'
        elif (relational_operators.match(lexeme)):
            return 'REL'

    def analyze_logical_operator(self, line, target_char):
        start = self.cursor.get_position()
        lexeme = line[start]
        try:
            look_ahead_char = line[self.cursor.get_look_ahead()]
            if (look_ahead_char == target_char):
                self.cursor.forward()
                lexeme += look_ahead_char
                return Token('LOG', lexeme, (self.line_count, start))
            else:
                return Token('OpMF', lexeme, (self.line_count, start))
        except(IndexError):
            return Token('OpMF', lexeme, (self.line_count, start))

    """ this method adds a new token to the token list """
    def add_token(self, token):
        if(token != None):
            self.tokens.append(token)

    """ this method returns token list """
    def get_tokens(self):
        return self.tokens

    """ this method returns symbol table dict """
    def get_symbol_table(self):
        return self.symbol_table

    def start_analyze(self):
        while self.line_count < len(self.code):  # iterate lines
            line = self.code[self.line_count]
            if (not self.is_comment_open):  # checks if not have an open comment
                while self.cursor.get_position() < len(line):  # iterate characters
                    flag = False
                    token = None
                    char = line[self.cursor.get_position()]
                    if (letter.match(char)):  # identifiers or words
                        token = self.analyze_id_or_word(line)
                    elif (digit.match(char)):  # numbers
                        token = self.analyze_numbers(line)
                    elif (char == '\"'):  # strings
                        token = self.analyze_string(line)
                    elif (char == '/'):  # comments delimiters or / operator
                        flag = self.analyze_comments_delimiters(line)
                    elif (delimiters.match(char)):  # delimiters
                        token = Token('DEL', char, (self.line_count, self.cursor.get_position()))
                    elif (char == '*'):  # * operator
                        token = Token('ART', char, (self.line_count, self.cursor.get_position()))
                    elif (char == '+' or char == '-' or char == '='): # + or ++, - or --, = or == operators
                        token = self.analyze_next_char(line, char)
                    elif (char == '>' or char == '<' or char == '!'): # > or >=, < or <=, ! or != operators
                        token = self.analyze_next_char(line, '=')
                    elif (char == '&' or char == '|'):  # && or || operator
                        token = self.analyze_logical_operator(line, char)
                    elif (char == ' ' or char == '\t' or char == '\n'):  # space, tab and line break
                        pass
                    else:
                        token = Token('SIB', char, (self.line_count, self.cursor.get_position()))

                    self.add_token(token)
                    self.cursor.forward()  # moves the cursor forward

                if (not flag):
                    self.line_count += 1
                    self.cursor.to_start()

            else:
                """ search for the end comment """
                if (not self.find_end_block_comment(line)):
                    self.line_count += 1
                    self.cursor.to_start()
