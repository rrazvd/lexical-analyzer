from cursor import Cursor
from symbol_table import SymbolTable
from token import Token
from constants import reserved_words, delimiters, letter, digit, string_ascii, letter_digit_under, arithmetic_operators, relational_operators, errors_name

""" This Class implements a Lexical Analyzer that recognizes tokens through finite automata """
class LexicalAnalyzer():

    def __init__(self, code):
        self.code = code # input code array per line
        self.line_count = 0 # line counter
        self.tokens, self.errors  = [], [] # create token list and error token list
        self.is_open_comment = False # boolean to know if there is an open comment
        self.comment_token = None  # used for store the comment token
        self.cursor = Cursor() # create a cursor that will move inside the code
        self.symbol_table = SymbolTable(reserved_words) # adds reserved words in symbol table
        self.start_analyze() # then the analyze begins

    """ this function looks for the end of block comment: '*/',
    if it finds, set is_open_comment to True, else set is_open_comment to False """
    def find_end_block_comment(self, line):
        pos = (self.line_count, self.cursor.get_position())
        lexeme = '' # set first lexeme character
        while self.cursor.get_position() < len(line):
            char = line[self.cursor.get_position()]
            if (char == '*'): # if atual char is '*'
                try:
                    look_ahead_char = line[self.cursor.get_look_ahead()] # get next char
                    if (look_ahead_char == '/'): # if the next char is / so we have */
                        self.is_open_comment = False # the end of block comment was found, so set to False
                        self.cursor.forward() # moves the cursor forward
                        return None
                    else:
                        self.is_open_comment = True # the end of block comment was not found, so set to True
                except (IndexError):
                    self.is_open_comment = True       
            lexeme += char # increases lexeme
            self.cursor.forward() # moves the cursor forward
        return Token('CoMF', lexeme, pos) # if the comment was not been closed, return malformed comment 

    """ this funcion analyze identifiers or reserved word lexemes """
    def analyze_id_or_word(self, line, pos):
        lexeme = line[pos[1]] # set first lexeme character
        while self.cursor.get_look_ahead() < len(line):
            look_ahead_char = line[self.cursor.get_look_ahead()]
            if (letter_digit_under.match(look_ahead_char)): # if the next char is letter, digit or _
                lexeme += look_ahead_char # so increases lexeme
            else:
                return self.symbol_table.get_token(lexeme, pos) # fetch token from symbol table
            self.cursor.forward() # moves the cursor forward

        return self.symbol_table.get_token(lexeme, pos) # fetch token from symbol table

    """ this funcion analyze numbers lexemes """
    def analyze_numbers(self,line, pos):    
        lexeme = line[pos[1]] # set first lexeme character
        self.cursor.forward() # moves the cursor forward
        while self.cursor.get_position() < len(line):
            char = line[self.cursor.get_position()] # get atual character
            if (digit.match(char)): # if it is a digit
                lexeme += char # increases lexeme
            elif (char == '.'): # if it is a dot
                lexeme += char # increases lexeme
                try: 
                    look_ahead_char = line[self.cursor.get_look_ahead()] # get next character
                    if (digit.match(look_ahead_char)): # if it is a digit
                        self.cursor.forward()   # moves the cursor forward
                        while self.cursor.get_position() < len(line): # iterar through next characters
                            char = line[self.cursor.get_position()] # get atual character
                            if (digit.match(char)): # if it is a digit
                                lexeme += char # increases lexeme
                            elif (char == '.'): # elif it is other dot
                                lexeme += char # increases lexeme
                                return Token('NMF', lexeme, pos) # return a malformed number
                            else:
                                self.cursor.backward() # moves the cursor backward
                                return Token('NRO', lexeme, pos) # return a token number
                            self.cursor.forward() # moves the cursor forward      
                    else:
                        return Token('NMF', lexeme, pos) # return a malformed number
                except(IndexError):
                    return Token('NMF', lexeme, pos)  # return a malformed number
            else:
                self.cursor.backward() # moves the cursor backward
                return Token('NRO', lexeme, pos) # return a token number   
            self.cursor.forward()  # moves the cursor forward     
        return Token('NRO', lexeme, pos)  # return a token number   

    """ this function analyze strings lexemes"""
    def analyze_string(self, line, pos):
        lexeme = line[pos[1]] # set first lexeme character
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
        return Token('CMF', lexeme, pos)

    """ this function analyze arithmetic, relational and '!' operators"""
    def analyze_next_char(self, line, target_char, pos):
        lexeme = line[pos[1]]  # set first lexeme character
        try:
            look_ahead_char = line[self.cursor.get_look_ahead()] # get next char
            if (look_ahead_char == target_char): # if the next char is the same
                self.cursor.forward() # move cursor forward 
                lexeme += look_ahead_char # increses lexeme
                return Token(self.get_operator_type(lexeme), lexeme, pos) # return corresponding token
            else:
                return Token(self.get_operator_type(lexeme), lexeme, pos) # return corresponding token
        except(IndexError):
            return Token(self.get_operator_type(lexeme), lexeme, pos) # return corresponding token

    """ this function check the type of operators"""
    def get_operator_type(self, lexeme):
        if (lexeme == '!'):
            return 'LOG'
        elif (arithmetic_operators.match(lexeme)):
            return 'ART'
        elif (relational_operators.match(lexeme)):
            return 'REL'

    """ this function analyzes if the lexeme found is logical operator """
    def analyze_logical_operator(self, line, target_char, pos):
        lexeme = line[pos[1]] # set first lexeme character
        try:
            look_ahead_char = line[self.cursor.get_look_ahead()]
            if (look_ahead_char == target_char): # if the next char is the same, so it is && or ||
                self.cursor.forward()
                lexeme += look_ahead_char
                return Token('LOG', lexeme, pos)
            else: # else it is a malformed operator
                return Token('OpMF', lexeme, pos)
        except(IndexError):
            return Token('OpMF', lexeme, pos)

    """ this function analyzes if the lexeme found is a division operator or comment symbol """
    def analyze_divisor_operator_or_comment(self, line, pos):
        lexeme = line[pos[1]] # set first lexeme character
        try:
            look_ahead_char = line[self.cursor.get_look_ahead()]
            if (look_ahead_char == '/'): # if //
                self.cursor.set_position(len(line)) # ignores rest of the line
                return None 
            elif (look_ahead_char == '*'): # if /*
                self.comment_token = self.find_end_block_comment(line) # search for end block comment
                return None
            else: # else is / operator
                return Token('ART', lexeme, pos) # return an arithmetic operator token
        except: 
            return Token('ART', lexeme, pos)  # return an arithmetic operator token

    """ this method adds a new token to the token list """
    def add_token(self, token):
        if(token != None):
            if(token.get_name() in errors_name):
                self.errors.append(token) # add to token error list
            else:
                self.tokens.append(token) # add to token list

    """ this method returns token list and token error list """
    def get_tokens(self):
        return (self.tokens, self.errors)

    """ this method returns symbol table dict """
    def get_symbol_table(self):
        return self.symbol_table

    def start_analyze(self):
        while self.line_count < len(self.code):  # iterate between lines indexes
            line = self.code[self.line_count] # get atual line
            if (not self.is_open_comment):  # checks if not have an open comment
                while self.cursor.get_position() < len(line):  # iterate between characters indexes             
                    pos = (self.line_count, self.cursor.get_position()) # save position L x C
                    char = line[pos[1]] # get atual character
                    if (letter.match(char)):  # identifiers or words
                        token = self.analyze_id_or_word(line, pos)
                    elif (digit.match(char)):  # numbers
                        token = self.analyze_numbers(line, pos)
                    elif (char == '\"'):  # strings
                        token = self.analyze_string(line, pos)
                    elif (delimiters.match(char)):  # delimiters
                        token = Token('DEL', char, pos)
                    elif (char == '*'):  # * operator
                        token = Token('ART', char, pos)
                    elif (char == '+' or char == '-' or char == '='): # + or ++, - or --, = or == operators
                        token = self.analyze_next_char(line, char, pos)
                    elif (char == '>' or char == '<' or char == '!'): # > or >=, < or <=, ! or != operators
                        token = self.analyze_next_char(line, '=', pos)
                    elif (char == '&' or char == '|'):  # && or || operator
                        token = self.analyze_logical_operator(line, char, pos)
                    elif (char == '/'):  #  / operator or comments delimiters
                        token = self.analyze_divisor_operator_or_comment(line, pos)
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
                if(self.is_open_comment): # if still open, keep search in next lines
                    self.line_count += 1
                    self.cursor.to_start() 
                else:
                    self.cursor.forward() # else, moves cursor forward to continue reading the rest of line

        self.add_token(self.comment_token) #if at the end of code there is an open comment, thus add it to the token list