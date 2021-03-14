from cursor import Cursor
from symbol_table import SymbolTable
from token import Token
from constants import reserved_words, delimiters, letter, digit, string_ascii, letter_digit_under, arithmetic_operators, relational_operators

""" This Class implements a Lexical Analyzer that recognizes tokens through finite automata """
class LexicalAnalyzer():

    def __init__(self, code):
        self.code = code
        self.tokens = []
        self.line_count = 0
        self.is_comment_open = False
        self.comment_token = None
        self.cursor = Cursor()
        self.symbol_table = SymbolTable(reserved_words)
        self.start_analyze()

    """ this function looks for the end of block comment: '*/',
    if it finds, returns True, else returns False """
    def find_end_block_comment(self, line):
        pos = (self.line_count, self.cursor.get_position())
        lexeme = ''
        while self.cursor.get_position() < len(line):
            char = line[self.cursor.get_position()]
            if (char == '*'):
                try:
                    look_ahead_char = line[self.cursor.get_look_ahead()]
                    if (look_ahead_char == '/'):
                        self.is_comment_open = False
                        self.cursor.forward()
                        return None
                    else:
                        self.is_comment_open = True
                except (IndexError):
                    self.is_comment_open = True          
            lexeme += char
            self.cursor.forward()
        return Token('CoMF', lexeme, pos)    

    """ analyze identifiers or reserved word lexemes """
    def analyze_id_or_word(self, line):
        pos = (self.line_count, self.cursor.get_position())
        lexeme = line[pos[1]]
        while self.cursor.get_look_ahead() < len(line):
            look_ahead_char = line[self.cursor.get_look_ahead()]
            if (letter_digit_under.match(look_ahead_char)):
                lexeme += look_ahead_char
            else:
                return self.symbol_table.get_token(lexeme, pos)
            self.cursor.forward()

        return self.symbol_table.get_token(lexeme, pos)

    def analyze_numbers(self,line):    
        pos = (self.line_count, self.cursor.get_position())
        lexeme = line[pos[1]]
        self.cursor.forward()
        while self.cursor.get_position() < len(line):
            char = line[self.cursor.get_position()]
            if (digit.match(char)):
                lexeme += char
            elif (char == '.'):
                lexeme += char
                try: 
                    look_ahead_char = line[self.cursor.get_look_ahead()]
                    if (digit.match(look_ahead_char)):
                        self.cursor.forward()  
                        while self.cursor.get_position() < len(line):
                            char = line[self.cursor.get_position()]
                            if (digit.match(char)):
                                lexeme += char
                            elif (char == '.'):
                                lexeme += char
                                return Token('NMF', lexeme, pos) 
                            else:
                                self.cursor.backward()
                                return Token('NRO', lexeme, pos)
                            self.cursor.forward()      
                    else:
                        return Token('NMF', lexeme, pos)
                except(IndexError):
                    return Token('NMF', lexeme, pos) 
            else:
                self.cursor.backward()
                return Token('NRO', lexeme, pos)    
            self.cursor.forward()
        return Token('NRO', lexeme, pos)        

    """ analyze strings """
    def analyze_string(self, line):
        pos = (self.line_count, self.cursor.get_position())
        lexeme = line[pos[1]]
        self.cursor.forward()
        while self.cursor.get_position() < len(line):
            char = line[self.cursor.get_position()]
            if (char == '\\'):  # if find \
                try:
                    look_ahead_char = line[self.cursor.get_look_ahead()]
                    if (look_ahead_char == '\"'):  # check if \"
                        lexeme += look_ahead_char
                        self.cursor.forward()
                    elif (look_ahead_char == '\\'):  # check if \\
                        lexeme += char
                        self.cursor.forward()
                except(IndexError):
                    return Token('CMF', lexeme, pos)
            elif (string_ascii.match(char)):  # check allowed ascii character
                lexeme += char
            elif (char == '\"'):  # check end of string
                lexeme += char
                return Token('CAD', lexeme, pos)
            else:
                return Token('CMF', lexeme, pos)
            self.cursor.forward()

    def analyze_next_char(self, line, next_char):
        pos = (self.line_count, self.cursor.get_position())
        lexeme = line[pos[1]]
        try:
            look_ahead_char = line[self.cursor.get_look_ahead()]
            if (look_ahead_char == next_char):
                self.cursor.forward()
                lexeme += look_ahead_char
                return Token(self.get_operator_type(lexeme), lexeme, pos)
            else:
                return Token(self.get_operator_type(lexeme), lexeme, pos)
        except(IndexError):
            return Token(self.get_operator_type(lexeme), lexeme, pos)

    def get_operator_type(self, lexeme):
        if (lexeme == '!'):
            return 'LOG'
        elif (arithmetic_operators.match(lexeme)):
            return 'ART'
        elif (relational_operators.match(lexeme)):
            return 'REL'

    def analyze_logical_operator(self, line, target_char):
        pos = (self.line_count, self.cursor.get_position())
        lexeme = line[pos[1]]
        try:
            look_ahead_char = line[self.cursor.get_look_ahead()]
            if (look_ahead_char == target_char):
                self.cursor.forward()
                lexeme += look_ahead_char
                return Token('LOG', lexeme, pos)
            else:
                return Token('OpMF', lexeme, pos)
        except(IndexError):
            return Token('OpMF', lexeme, pos)

    def analyze_divisor_operator_or_comment(self, line):
        pos = (self.line_count, self.cursor.get_position())
        lexeme = line[pos[1]]
        try:
            look_ahead_char = line[self.cursor.get_look_ahead()]
            if (look_ahead_char == '/'):
                self.cursor.set_position(len(line)) # ignores rest of the line
                return None 
            elif (look_ahead_char == '*'):
                self.comment_token = self.find_end_block_comment(line) # search for end block comment
                return None
            else: 
                return Token('ART', lexeme, pos)
        except:
            return Token('ART', lexeme, pos) 

    """ this method adds a new token to the token list """
    def add_token(self, token):
        if(token != None):
            self.tokens.append(token)
            return True

    """ this method returns token list """
    def get_tokens(self):
        return self.tokens

    """ this method returns symbol table dict """
    def get_symbol_table(self):
        return self.symbol_table

    def start_analyze(self):
        while self.line_count < len(self.code):  # iterate between lines indexes
            line = self.code[self.line_count] # get atual line
            if (not self.is_comment_open):  # checks if not have an open comment
                while self.cursor.get_position() < len(line):  # iterate between characters indexes             
                    pos = (self.line_count, self.cursor.get_position()) # save position L x C
                    char = line[pos[1]] # get atual character
                    if (letter.match(char)):  # identifiers or words
                        token = self.analyze_id_or_word(line)
                    elif (digit.match(char)):  # numbers
                        token = self.analyze_numbers(line)
                    elif (char == '\"'):  # strings
                        token = self.analyze_string(line)
                    elif (delimiters.match(char)):  # delimiters
                        token = Token('DEL', char, pos)
                    elif (char == '*'):  # * operator
                        token = Token('ART', char, pos)
                    elif (char == '+' or char == '-' or char == '='): # + or ++, - or --, = or == operators
                        token = self.analyze_next_char(line, char)
                    elif (char == '>' or char == '<' or char == '!'): # > or >=, < or <=, ! or != operators
                        token = self.analyze_next_char(line, '=')
                    elif (char == '&' or char == '|'):  # && or || operator
                        token = self.analyze_logical_operator(line, char)
                    elif (char == '/'):  #  / operator or comments delimiters
                        token = self.analyze_divisor_operator_or_comment(line)
                    elif (char == ' ' or char == '\t' or char == '\n'):  # space, tab and line break
                        token = None # no token is generated by these characters
                    else: # invalid symbols
                        token = Token('SIB', char, pos)

                    self.add_token(token)  # add resulting token 
                    self.cursor.forward()  # moves the cursor forward
                
                self.line_count += 1 # go to next line
                self.cursor.to_start() # set cursor to start of line
            
            else:
                self.find_end_block_comment(line) # search for the end of block comment
                if(self.is_comment_open): # if still open, keep search in next lines
                    self.line_count += 1
                    self.cursor.to_start() 
                else:
                    self.cursor.forward() # else, moves cursor forward to continue reading the rest of line

        self.add_token(self.comment_token)