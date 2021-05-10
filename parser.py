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

        if (self.check_firsts(Firsts.DECLS)):  # <Decls>
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
                self.handle_error(Tokens.IDENTIFIER)
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
                            self.handle_error(Tokens.IDENTIFIER)
                    else:
                        self.handle_error('}')   
                else:
                    self.handle_error('{')
            else:
                self.handle_error('struct')

    # <Extends>
    def extends(self):
        if (not self.consume(Tokens.IDENTIFIER)):
            self.handle_error(Tokens.IDENTIFIER)

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
            if(self.check_firsts(Firsts.VAR_DECLS)):
                self.var_decls()

            if (not self.consume('}')):
                self.handle_error('}')
        else:
            self.handle_error('{')         

    # <Var Decls>
    def var_decls(self):
        self.var_decl()
        if(self.check_firsts(Firsts.VAR_DECLS)):
            self.var_decls()

    # <Var Decl>
    def var_decl(self):
        if (self.check_firsts(Firsts.TYPE)):
            self._type()
            if (self.consume(Tokens.IDENTIFIER)):
                self.var()
                if (self.check_firsts(Firsts.VAR_LIST)):
                    self.var_list()
                else:
                    self.handle_error(Firsts.VAR_LIST)    
            else:
                self.handle_error(Tokens.IDENTIFIER)    
        elif (self.consume('typedef')):
            self.type_def()
        elif (self.consume(Tokens.IDENTIFIER)):
            self.var()    # dois ids??

    # <Type>
    def _type(self):
        self.consume(Firsts.TYPE)
        # struct id não eh tratado

    # <Typedef>
    def type_def(self):
        if (self.check_firsts(Firsts.TYPE)):
            self._type()
            if (self.consume(Tokens.IDENTIFIER)):
                if (not self.consume(';')):
                    self.handle_error(';')
            else:
                self.handle_error(Tokens.IDENTIFIER)  
        else:
            self.handle_error(Firsts.TYPE)        

    # <Var>
    def var(self):
        if (self.consume('[')):
            self.arrays()

    # <Var List>
    def var_list(self):
        if (self.consume(',')):
            if (self.consume(Tokens.IDENTIFIER)):
                self.var()
                if (self.check_firsts(Firsts.VAR_LIST)):
                    self.var_list()
            else:
                self.handle_error(Tokens.IDENTIFIER)        
        elif (self.consume('=')):
            print('=')
            # <Decl Atribute> <Var List>
        elif (self.consume(';')):
            pass

    # <Arrays>
    def arrays(self):
        self.array()
        if (self.consume('[')):
            self.arrays()

    # <Array>
    def array(self):
        # <Index>
        if (not self.consume(']')):
            self.handle_error(']')    

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
            self.handle_error(Tokens.IDENTIFIER)

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
            self.handle_error(Tokens.IDENTIFIER)

    # <Func Block>
    def func_block(self):
        if (self.consume('{')):
            if (self.consume('var')): # <Var Block>
                self.var_block()
            #funcstms
            if (not self.consume('}')):
                self.handle_error('}')    
        else:
            self.handle_error('{')

    def check_firsts(self,firsts):
        token = self.get_token()
        if (token != None):
            if (token.get_attribute() in firsts.value):
                return True
            else:
                return False
        else:
            return False  

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

    @dispatch(Firsts)
    def consume(self, firsts):
        token = self.get_token()
        if (token != None):
            if (token.get_attribute() in firsts.value):
                self.parser_tokens.append(token)
                self.cursor.forward()
                return True
            else:
                return False
        else:
            return False                   
      
    @dispatch(str)
    def handle_error(self, expected):
        token = self.get_token()
        if (token != None):
            pos = token.get_pos()
            print('Synthatic Error: expected \'' + expected + '\', but received \'' + token.get_attribute() + '\' on line ' + str(pos[0] + 1))
        else:
            print('Synthatic Error: at the end of file expected \'' + expected + '\', but there are no more tokens.')
            exit()

    @dispatch(Tokens)
    def handle_error(self, expected):
        token = self.get_token()
        if (token != None):
            pos = token.get_pos()
            print('Synthatic Error: expected ' + expected.value + ', but received \'' + token.get_attribute() + '\' on line ' + str(pos[0] + 1))
        else:
            print('Synthatic Error: at the end of file expected \'' + expected + '\', but there are no more tokens.')
            exit()   

    @dispatch(Firsts)
    def handle_error(self, expected):
        token = self.get_token()
        if (token != None):
            pos = token.get_pos()
            print('Synthatic Error: expected ' + str(expected.value) + ', but received \'' + token.get_attribute() + '\' on line ' + str(pos[0] + 1))
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