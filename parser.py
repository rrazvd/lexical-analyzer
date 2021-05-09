from cursor import Cursor
from firsts import Firsts
from constants import Tokens
from multipledispatch import dispatch
""" 
This Class implements a syntactic analyzer. 
"""
class Parser():

    def __init__(self, tokens):
        self.tokens = tokens
        self.parser_tokens = []
        self.cursor = Cursor() # create a cursor that will move inside the tokens list
        self.program() # then the analyze begins

    # <Program>
    def program(self): 

        if (self.check_firsts(Firsts.STRUCT_BLOCK)): # <Structs>
            self.structs()

        if (self.consume('const')): # <Const Block>
            self.const_block()

        if (self.consume('var')): # <Var Block>
            self.var_block()

        if (self.consume('procedure')): # <Start Block>
            self.start_block()
        else:
            self.handle_error('procedure')

        if(self.check_firsts(Firsts.DECLS)):  # <Decls>
            self.decls()

    # <Structs>
    def structs(self):
        self.struct_block()
        if(self.check_firsts(Firsts.STRUCT_BLOCK)):  # <Decls>
            self.structs()

    # <Struct Block>
    def struct_block(self):
        if(self.consume('struct')):
            if (self.consume(Tokens.IDENTIFIER)):
                if(self.consume('extends')):
                    self.extends()
                if (self.consume('{')):
                    if(self.consume('var')):
                        self.var_block()
                    if(not self.consume('}')):
                        self.handle_error('}')
                else:
                    self.handle_error('{')    
            else:
                self.handle_error(Tokens.IDENTIFIER.value)
        elif(self.consume('typedef')):
            if(self.consume('struct')):
                if(self.consume('extends')):
                    self.extends()
                if (self.consume('{')):
                    if(self.consume('var')):
                        self.var_block()
                    if(self.consume('}')):
                        if (self.consume(Tokens.IDENTIFIER)):
                            if (not self.consume(';')):
                                self.handle_error(';')
                        else:
                            self.handle_error(Tokens.IDENTIFIER.value)
                    else:
                        self.handle_error('}')   
                else:
                    self.handle_error('{')
            else:
                self.handle_error('struct')

    # <Extends>
    def extends(self):
        if (not self.consume(Tokens.IDENTIFIER)):
            self.handle_error(Tokens.IDENTIFIER.value)

    # <Const Block>
    def const_block(self):
        if (self.consume('{')):
            # <Const Decls>
            if (not self.consume('}')):
                self.handle_error('}')
        else:
            self.handle_error('{')

    # <Var Block>
    def var_block(self):
        if(self.consume('{')):
            #self.var_decls()
            if (not self.consume('}')):
                self.handle_error('}')
        else:
            self.handle_error('{')         

    # <Start Block>
    def start_block(self):
        if(self.consume('start')):
            self.func_block()
        else:
            self.handle_error('start')

    # <Decls>
    def decls(self):
        self.decl()
        if(self.check_firsts(Firsts.DECLS)):  # <Decls>
            self.decls()

    # <Decl>
    def decl(self):
        if(self.consume('function')):
            self.func_decl()
        elif(self.consume('procedure')):
            self.proc_decl()    

    # <Func decls>
    def func_decl(self):
        #<Param Type>
        if (self.consume(Tokens.IDENTIFIER)):
            if(self.consume('(')):
                #<Params>
                if(self.consume(')')):
                    self.func_block()
                else:    
                    self.handle_error(')')
            else:
                self.handle_error('(')
        else:
            self.handle_error(Tokens.IDENTIFIER.value)

    # <Proc Decl>
    def proc_decl(self):
        if (self.consume(Tokens.IDENTIFIER)):
            if(self.consume('(')):
                #<Params>
                if(self.consume(')')):
                    self.func_block()
                else:    
                    self.handle_error(')')
            else:
                self.handle_error('(')
        else:
            self.handle_error(Tokens.IDENTIFIER.value)

    # <Func Block>
    def func_block(self):
        if (self.consume('{')):
            #varblock
            #funcstms
            if (not self.consume('}')):
                self.handle_error('}')    
        else:
            self.handle_error('{')

    @dispatch(str)
    def consume(self, terminal):
        token = self.get_token()
        if (token != None):
            if (token.get_attribute() == terminal):
                self.parser_tokens.append(token)
                self.cursor.forward()
                return True
            else:
                return False
        else:
            return False
    
    @dispatch(Tokens)
    def consume(self, token_name):
        token = self.get_token()
        if (token != None):
            if (token.get_name() == token_name.value):
                self.parser_tokens.append(token)
                self.cursor.forward()
                return True
            else:
                return False
        else:
            return False        

    def check_firsts(self,firsts):
        token = self.get_token()
        if (token != None):
            if (token.get_attribute() in firsts.value):
                return True
            else:
                return False
        else:
            return False        

    def handle_error(self, expected):
        token = self.get_token()
        if (token != None):
            pos = token.get_pos()
            print('Synthatic Error: expected \'' + expected + '\', but received \'' + token.get_attribute() + '\' on line ' + str(pos[0] + 1))
        else:
            print('Synthatic Error: at the end of file expected \'' + expected + '\', but there are no more tokens.')
            exit()

    def get_token(self):
        pos = self.cursor.get_position()
        if (pos < len(self.tokens)):
            return self.tokens[pos]
        return None

    def get_parser_tokens(self):
        return self.parser_tokens