from cursor import Cursor
from constants import Tokens, Firsts, Follows, Errors
from multipledispatch import dispatch
from token2 import Token

"""
This Class implements a syntactic analyzer.
"""


class Parser():

    def __init__(self, tokens, semantic, symbol_table):
        self.tokens = tokens
        self.parser_tokens = []
        self.semantic = semantic
        self.symbol_table = symbol_table
        self.cursor = Cursor()  # create a cursor that will move inside the tokens list
        self.program()  # then the analyze begins

    # <Program>
    def program(self):
        self.semantic.set_scope('global')
        if (self.check_firsts(Firsts.STRUCT_BLOCK)):  # <Structs>
            self.structs()
        self.semantic.set_scope('global')
        if (self.consume('const')):  # <Const Block>
            self.const_block()

        if (self.consume('var')):  # <Var Block>
            self.var_block()

        if (self.check_firsts(Firsts.DECLS)):  # <Decls>
            self.decls()

        if (self.consume('start')):  # <Start Block>
            self.semantic.set_scope('start')
            self.start_block()
        else:
            self.handle_errorf('start', Follows.START_BLOCK)

    # <Structs>
    def structs(self):
        self.struct_block()
        if(self.check_firsts(Firsts.STRUCT_BLOCK)):
            self.structs()

    # <Struct Block>
    def struct_block(self):
        if(self.consume('struct')):
            if (self.consume(Tokens.IDENTIFIER)):
                token_id = self.get_previous_token(1)
                self.semantic.add_struct(token_id)
                if(self.consume('extends')):
                    self.extends()
                if (self.consume('{')):
                    if(self.consume('var')):
                        self.var_block()
                    if(not self.consume('}')):
                        self.handle_errorf('}', Follows.STRUCT_BLOCK)
                else:
                    self.handle_errorf('{', Follows.STRUCT_BLOCK)
            else:
                self.handle_errorf(Tokens.IDENTIFIER, Follows.STRUCT_BLOCK)
        elif(self.consume('typedef')):
            extends_id = None
            if(self.consume('struct')):
                if(self.consume('extends')):
                    self.extends()
                    extends_id = self.get_previous_token(1)
                    self.semantic.check_identifier(extends_id)
                if (self.consume('{')):
                    if(self.consume('var')):
                        self.semantic.set_scope('@temporary_scope')
                        self.var_block()
                    if(self.consume('}')):
                        if (self.consume(Tokens.IDENTIFIER)):
                            token_id = self.get_previous_token(1)
                            self.semantic.add_typedef_struct(
                                token_id, extends_id)
                            if (not self.consume(';')):
                                self.handle_errorf(';', Follows.STRUCT_BLOCK)
                        else:
                            self.handle_errorf(
                                Tokens.IDENTIFIER, Follows.STRUCT_BLOCK)
                    else:
                        self.handle_errorf('}', Follows.STRUCT_BLOCK)
                else:
                    self.handle_errorf('{', Follows.STRUCT_BLOCK)
            else:
                self.handle_errorf('struct', Follows.STRUCT_BLOCK)

    # <Extends>
    def extends(self):
        if (not self.consume(Tokens.IDENTIFIER)):
            self.handle_errorf(Tokens.IDENTIFIER, Follows.EXTENDS)

    # <Const Block>
    def const_block(self):
        if (self.consume('{')):
            if(self.check_firsts(Firsts.CONST_DECLS)):
                self.const_decls()

            if (not self.consume('}')):
                self.handle_errorf('}', Follows.CONST_BLOCK)
        else:
            self.handle_errorf('{', Follows.CONST_BLOCK)

    # <Const Decls>
    def const_decls(self):
        self.const_decl()
        if(self.check_firsts(Firsts.CONST_DECLS)):
            self.const_decls()

    # <Const Decl>
    def const_decl(self):
        if (self.check_firsts(Firsts.TYPE)):
            self._type()
            if (self.consume(Tokens.IDENTIFIER)):
                token_type = self.get_previous_token(2)
                token_identifier = self.get_previous_token(1)
                self.semantic.add_const(token_type,
                                        token_identifier)
                self.const()
                if (self.check_firsts(Firsts.CONST_LIST)):
                    self.const_list(token_type)
                else:
                    self.handle_errorf(Firsts.CONST_LIST, Follows.CONST_DECL)
            else:
                self.handle_errorf(Tokens.IDENTIFIER, Follows.CONST_DECL)
        elif (self.consume('typedef')):
            self.type_def()
        elif (self.consume(Tokens.IDENTIFIER)):
            if (self.consume(Tokens.IDENTIFIER)):
                token_type = self.get_previous_token(2)
                token_identifier = self.get_previous_token(1)
                self.semantic.add_const(token_type,
                                        token_identifier)
                self.const()
                if (self.check_firsts(Firsts.CONST_LIST)):
                    self.const_list(token_type)
                else:
                    self.handle_errorf(Firsts.CONST_LIST, Follows.CONST_DECL)
            else:
                self.handle_errorf(Tokens.IDENTIFIER, Follows.CONST_DECL)

    # <Const>
    def const(self):
        if (self.consume('[')):
            self.arrays()

        if (self.consume('=')):
            if (self.check_firsts(Firsts.DECL_ATRIBUTE)):
                self.decl_atribute()
            else:
                self.handle_errorf(Firsts.DECL_ATRIBUTE, Follows.CONST)
        else:
            self.handle_errorf('=', Follows.CONST)

    # <Const List>
    def const_list(self, token_type):
        if (self.consume(',')):
            if (self.consume(Tokens.IDENTIFIER)):
                token_identifier = self.get_previous_token(1)
                self.semantic.add_const(token_type,
                                        token_identifier)
                self.const()
                if (self.check_firsts(Firsts.CONST_LIST)):
                    self.const_list(token_type)
                else:
                    self.handle_errorf(Firsts.CONST_LIST, Follows.CONST_LIST)
            else:
                self.handle_errorf(Tokens.IDENTIFIER, Follows.CONST_LIST)
        elif (self.consume(';')):
            pass

    # <Var Block>
    def var_block(self):
        if(self.consume('{')):
            if(self.check_firsts(Firsts.VAR_DECLS)):
                self.var_decls()

            if (not self.consume('}')):
                self.handle_errorf('}', Follows.VAR_BLOCK)
        else:
            self.handle_errorf('{', Follows.VAR_BLOCK)

    # <Var Decls>
    def var_decls(self):
        self.var_decl()
        if(self.check_firsts(Firsts.VAR_DECLS)):
            self.var_decls()

    # <Var Decl>
    def var_decl(self):
        if (self.check_firsts(Firsts.TYPE)):
            self._type()
            if (self.consume(Tokens.IDENTIFIER)):      # var id
                token_type = self.get_previous_token(2)
                token_identifier = self.get_previous_token(1)
                self.semantic.add_var(token_type,
                                      token_identifier)
                self.var()
                if (self.check_firsts(Firsts.VAR_LIST)):
                    self.var_list(token_type)
                else:
                    self.handle_errorf(Firsts.VAR_LIST, Follows.VAR_DECL)
            else:
                self.handle_errorf(Tokens.IDENTIFIER, Follows.VAR_DECL)
        elif (self.consume('typedef')):
            self.type_def()
        elif (self.consume(Tokens.IDENTIFIER)):
            if (self.consume(Tokens.IDENTIFIER)):
                token_type = self.get_previous_token(2)
                token_identifier = self.get_previous_token(1)
                self.semantic.add_var(token_type,
                                      token_identifier)
                self.var()
                if (self.check_firsts(Firsts.VAR_LIST)):
                    self.var_list(token_type)
                else:
                    self.handle_errorf(Firsts.VAR_LIST, Follows.VAR_DECL)
            else:
                self.handle_errorf(Tokens.IDENTIFIER, Follows.VAR_DECL)

    # <Type>
    def _type(self):
        if (self.consume('struct')):
            if (not self.consume(Tokens.IDENTIFIER)):
                self.handle_errorf(Tokens.IDENTIFIER, Follows.TYPE)
        else:
            self.consume(Firsts.TYPE)

    # <Typedef>
    def type_def(self):
        if (self.check_firsts(Firsts.TYPE)):
            self._type()
            if (self.consume(Tokens.IDENTIFIER)):
                if (not self.consume(';')):
                    self.handle_errorf(';', Follows.TYPEDEF)
            else:
                self.handle_errorf(Tokens.IDENTIFIER, Follows.TYPEDEF)
        else:
            self.handle_errorf(Firsts.TYPE, Follows.TYPEDEF)

    # <Var>
    def var(self):
        if (self.consume('[')):
            self.arrays()

    # <Var List>
    def var_list(self, token_type):
        if (self.consume(',')):
            if (self.consume(Tokens.IDENTIFIER)):
                token_identifier = self.get_previous_token(1)
                self.semantic.add_var(token_type,
                                      token_identifier)
                self.var()
                if (self.check_firsts(Firsts.VAR_LIST)):
                    self.var_list(token_type)
                else:
                    self.handle_errorf(Firsts.VAR_LIST, Follows.VAR_LIST)
            else:
                self.handle_errorf(Tokens.IDENTIFIER, Follows.VAR_LIST)
        elif (self.consume('=')):
            if (self.check_firsts(Firsts.DECL_ATRIBUTE)):
                self.decl_atribute()
                if (self.check_firsts(Firsts.VAR_LIST)):
                    self.var_list(token_type)
                else:
                    self.handle_errorf(Firsts.VAR_LIST, Follows.VAR_LIST)
            else:
                self.handle_errorf(Firsts.DECL_ATRIBUTE, Follows.VAR_LIST)
        elif (self.consume(';')):
            pass

    # <Arrays>
    def arrays(self):
        self.array()
        if (self.consume('[')):
            self.arrays()

    # <Assign>
    def assign(self):
        if (self.consume('=')):
            if(self.check_firsts(Firsts.EXPR)):
                self.expr()
                if(not self.consume(';')):
                    self.handle_errorf(';', Follows.ASSIGN)
            else:
                self.handle_errorf(Firsts.EXPR, Follows.ASSIGN)
        elif(self.consume('++')):
            if(not self.consume(';')):
                self.handle_errorf(';', Follows.ASSIGN)
        elif(self.consume('--')):
            if(not self.consume(';')):
                self.handle_errorf(';', Follows.ASSIGN)

    # <Accesses>
    def accesses(self):
        self.access()
        if (self.consume('.')):
            self.accesses()

    # <Access>
    def access(self):
        if(self.consume(Tokens.IDENTIFIER)):
            token_access = self.get_previous_token(3)
            token_id = self.get_previous_token(1)
            self.semantic.check_identifier_access(token_id, token_access)
            if (self.consume('[')):
                self.arrays()
        else:
            self.handle_errorf(Tokens.IDENTIFIER, Follows.ACCESS)

    # <Args>
    def args(self):
        if (self.check_firsts(Firsts.EXPR)):
            self.expr()
            if(self.consume(',')):
                self.args_list()

    # <Args List>
    def args_list(self):
        if (self.check_firsts(Firsts.EXPR)):
            self.expr()
            if(self.consume(',')):
                self.args_list()
        else:
            self.handle_errorf(Firsts.EXPR, Follows.ARGS_LIST)

    # <Array>
    def array(self):
        if (self.check_firsts(Firsts.INDEX)):
            self.index()
        if (not self.consume(']')):
            self.handle_errorf(']', Follows.ARRAY)

    # <Index>
    def index(self):
        if (self.consume(Tokens.IDENTIFIER)):
            pass
        elif(self.consume(Tokens.NUMBER)):
            pass

    # <Start Block>
    def start_block(self):
        if(self.consume('procedure')):
            self.func_block()
        else:
            self.handle_errorf('procedure', Follows.START_BLOCK)

    # <Decls>
    def decls(self):
        self.decl()
        if(self.check_firsts(Firsts.DECLS)):
            self.decls()

    # <Decl>
    def decl(self):
        if(self.consume('function')):
            self.func_decl()
        elif(self.consume('procedure')):
            self.proc_decl()

    # <Decl Atribute>
    def decl_atribute(self):
        if (self.consume('{')):
            self.array_decl()
        elif(self.check_firsts(Firsts.EXPR)):
            self.expr()

    # <Array Decl>
    def array_decl(self):
        if (self.check_firsts(Firsts.ARRAY_DEF)):
            self.array_def()
            if (not self.consume('}')):
                self.handle_errorf('}', Follows.ARRAY_DECL)
        else:
            self.handle_errorf(Firsts.ARRAY_DEF, Follows.ARRAY_DECL)

    # <Array Def>
    def array_def(self):
        if (self.check_firsts(Firsts.EXPR)):
            self.expr()
            if (self.consume(',')):
                self.array_expr()

    # <Array Expr>
    def array_expr(self):
        if (self.check_firsts(Firsts.ARRAY_DEF)):
            self.array_def()
        else:
            self.handle_errorf(Firsts.ARRAY_DEF, Follows.ARRAY_EXPR)

    # <Func decls>
    def func_decl(self):
        token_id = None
        params = None
        if (self.check_firsts(Firsts.PARAM_TYPE)):
            self.param_type()
            if (self.consume(Tokens.IDENTIFIER)):
                token_id = self.get_previous_token(1)
                if(self.consume('(')):
                    if (self.check_firsts(Firsts.PARAM_TYPE)):
                        self.params()
                        params = self.get_params()
                    if(self.consume(')')):
                        self.semantic.add_func(token_id, params)
                        self.func_block()
                    else:
                        self.handle_errorf(')', Follows.FUNC_DECL)
                else:
                    self.handle_errorf('(', Follows.FUNC_DECL)
            else:
                self.handle_errorf(Tokens.IDENTIFIER, Follows.FUNC_DECL)
        else:
            self.handle_errorf(Firsts.PARAM_TYPE, Follows.FUNC_DECL)

    # <Proc Decl>
    def proc_decl(self):
        token_id = None
        params = None
        if (self.consume(Tokens.IDENTIFIER)):
            token_id = self.get_previous_token(1)
            if(self.consume('(')):
                if (self.check_firsts(Firsts.PARAM_TYPE)):
                    self.params()
                    params = self.get_params()
                if(self.consume(')')):
                    self.semantic.add_proc(token_id, params)
                    self.func_block()
                else:
                    self.handle_errorf(')', Follows.PROC_DECL)
            else:
                self.handle_errorf('(', Follows.PROC_DECL)
        else:
            self.handle_errorf(Tokens.IDENTIFIER, Follows.PROC_DECL)

    def get_params(self):
        params = []
        n = 1
        while(self.get_previous_token(n).get_attribute() != '('):
            token_id = self.get_previous_token(n)
            if (token_id.get_name() == Tokens.IDENTIFIER.value):
                token_type = self.get_previous_token(n + 1)
                params.append((token_type, token_id))
            n += 1
        params.reverse()
        return params

    # <Params>
    def params(self):
        self.param()
        if (self.consume(',')):
            self.params_list()

    # <Param>
    def param(self):
        self.param_type()
        if (self.consume(Tokens.IDENTIFIER)):
            if (self.consume('[')):
                self.param_arrays()
        else:
            self.handle_errorf(Tokens.IDENTIFIER, Follows.PARAM)

    # <Params list>
    def params_list(self):
        if (self.check_firsts(Firsts.PARAM_TYPE)):
            self.param()
            if (self.consume(',')):
                self.params_list()
        else:
            self.handle_errorf(Firsts.PARAM_TYPE, Follows.PARAMS_LIST)

    # <Param Type>
    def param_type(self):
        if (self.check_firsts(Firsts.TYPE)):
            self._type()
        elif (self.consume(Tokens.IDENTIFIER)):
            pass

    # <Param Arrays>
    def param_arrays(self):
        if (self.consume(']')):
            if (self.consume('[')):
                self.param_mult_arrays()
        else:
            self.handle_errorf(']', Follows.PARAMS_ARRAYS)

    # <Param Mult Arrays>
    def param_mult_arrays(self):
        if(self.consume(Tokens.NUMBER)):
            if(self.consume(']')):
                if (self.consume('[')):
                    self.param_mult_arrays()
            else:
                self.handle_errorf(']', Follows.PARAM_MULT_ARRAYS)
        else:
            self.handle_errorf(Tokens.NUMBER, Follows.PARAM_MULT_ARRAYS)

    # <Func Block>
    def func_block(self):
        if (self.consume('{')):
            if (self.consume('var')):
                self.var_block()
            if (self.check_firsts(Firsts.FUNC_STMS)):
                self.func_stms()
            if (not self.consume('}')):
                self.handle_errorf('}', Follows.FUNC_BLOCK)
        else:
            self.handle_errorf('{', Follows.FUNC_BLOCK)

    # <Func Stms>
    def func_stms(self):
        self.func_stm()
        if (self.check_firsts(Firsts.FUNC_STMS)):
            self.func_stms()

    # <Func Stm>
    def func_stm(self):
        if(self.consume('if')):
            self.if_stm()
        elif(self.consume('while')):
            self.while_stm()
        elif(self.check_firsts(Firsts.VAR_STM)):
            self.var_stm()
        elif(self.consume('return')):
            if (self.check_firsts(Firsts.EXPR)):
                self.expr()
                if (not self.consume(';')):
                    self.handle_errorf(';', Follows.FUNC_STM)
            else:
                self.handle_errorf(Firsts.EXPR, Follows.FUNC_STM)

    # <Else Stm>
    def else_stm(self):
        if(self.consume('{')):
            if (self.check_firsts(Firsts.FUNC_STMS)):
                self.func_stms()
            if (not self.consume('}')):
                self.handle_errorf('}', Follows.ELSE_STM)
        else:
            self.handle_errorf('{', Follows.ELSE_STM)

    # <If Stm>
    def if_stm(self):
        if(self.consume('(')):
            if (self.check_firsts(Firsts.LOG_EXPR)):
                self.log_expr()
                if(self.consume(')')):
                    if(self.consume('then')):
                        if(self.consume('{')):
                            if (self.check_firsts(Firsts.FUNC_STMS)):
                                self.func_stms()
                            if(self.consume('}')):
                                if (self.consume('else')):
                                    self.else_stm()
                            else:
                                self.handle_errorf('}', Follows.IF_STM)
                        else:
                            self.handle_errorf('{', Follows.IF_STM)
                    else:
                        self.handle_errorf('then', Follows.IF_STM)
                else:
                    self.handle_errorf(')', Follows.IF_STM)
            else:
                self.handle_errorf(Firsts.LOG_EXPR, Follows.IF_STM)

    # <While Stm>
    def while_stm(self):
        if(self.consume('(')):
            if (self.check_firsts(Firsts.LOG_EXPR)):
                self.log_expr()
                if(self.consume(')')):
                    if(self.consume('{')):
                        if (self.check_firsts(Firsts.FUNC_STMS)):
                            self.func_stms()
                        if(not self.consume('}')):
                            self.handle_errorf('}', Follows.WHILE_STM)
                    else:
                        self.handle_errorf('{', Follows.WHILE_STM)
                else:
                    self.handle_errorf(')', Follows.WHILE_STM)
            else:
                self.handle_errorf(Firsts.LOG_EXPR, Follows.WHILE_STM)

    # <Var Stm>
    def var_stm(self):
        if(self.check_firsts(Firsts.STM_SCOPE)):
            self.stm_scope()
        elif(self.consume(Tokens.IDENTIFIER)):
            token_id = self.get_previous_token(1)
            self.semantic.check_identifier(token_id)
            if(self.check_firsts(Firsts.STM_ID)):
                self.stm_id()
            else:
                self.handle_errorf(Firsts.STM_ID, Follows.VAR_STM)
        elif(self.check_firsts(Firsts.STM_CMD)):
            self.stm_cmd()

    # <Stm Id>
    def stm_id(self):
        if(self.check_firsts(Firsts.ASSIGN)):
            self.assign()
        elif (self.consume('[')):
            self.array()
            if(self.consume('[')):
                self.arrays()
            if (self.consume('.')):
                self.accesses()
            if(self.check_firsts(Firsts.ASSIGN)):
                self.assign()
            else:
                self.handle_errorf(Firsts.ASSIGN, Follows.STM_ID)
        elif(self.consume('.')):
            self.access()
            if (self.consume('.')):
                self.accesses()
            if(self.check_firsts(Firsts.ASSIGN)):
                self.assign()
            else:
                self.handle_errorf(Firsts.ASSIGN, Follows.STM_ID)
        elif(self.consume('(')):
            if(self.check_firsts(Firsts.ARGS)):
                self.args()
            if (self.consume(')')):
                if(not self.consume(';')):
                    self.handle_errorf(';', Follows.STM_ID)
            else:
                self.handle_errorf(')', Follows.STM_ID)

    # <Stm Scope>
    def stm_scope(self):
        if(self.consume('local')):
            if(self.consume('.')):
                self.access()
                if (self.consume('.')):
                    self.accesses()
                if(self.check_firsts(Firsts.ASSIGN)):
                    self.assign()
                else:
                    self.handle_errorf(Firsts.ASSIGN, Follows.STM_SCOPE)
            else:
                self.handle_errorf('.', Follows.STM_SCOPE)
        elif(self.consume('global')):
            if(self.consume('.')):
                self.access()
                if (self.consume('.')):
                    self.accesses()
                if(self.check_firsts(Firsts.ASSIGN)):
                    self.assign()
                else:
                    self.handle_errorf(Firsts.ASSIGN, Follows.STM_SCOPE)
            else:
                self.handle_errorf('.', Follows.STM_SCOPE)

    # <Stm Cmd>
    def stm_cmd(self):
        if(self.consume('print')):
            if(self.consume('(')):
                if(self.check_firsts(Firsts.ARGS)):
                    self.args()
                if(self.consume(')')):
                    if(not self.consume(';')):
                        self.handle_errorf(';', Follows.STM_CMD)
                else:
                    self.handle_errorf(')', Follows.STM_CMD)
            else:
                self.handle_errorf('(', Follows.STM_CMD)
        elif(self.consume('read')):
            if(self.consume('(')):
                if(self.check_firsts(Firsts.ARGS)):
                    self.args()
                if(self.consume(')')):
                    if(not self.consume(';')):
                        self.handle_errorf(';', Follows.STM_CMD)
                else:
                    self.handle_errorf(')', Follows.STM_CMD)
            else:
                self.handle_errorf('(', Follows.STM_CMD)

    # <Expr>
    def expr(self):
        self._or()

    # <Or>
    def _or(self):
        self._and()
        if (self.consume('||')):
            self._or_()

    # <Or_>
    def _or_(self):
        self._and()
        if (self.consume('||')):
            self._or_()

    # <And>
    def _and(self):
        self.equate()
        if (self.consume('&&')):
            self._and_()

    # <And_>
    def _and_(self):
        self.equate()
        if (self.consume('&&')):
            self._and_()

    # <Equate>
    def equate(self):
        self.compare()
        self.equate_()

    # <Equate_>
    def equate_(self):
        if(self.consume('==')):
            self.compare()
            self.equate_()
        elif (self.consume('!=')):
            self.compare()
            self.equate_()

    # <Compare>
    def compare(self):
        self.add()
        self.compare_()

    # <Compare_>
    def compare_(self):
        if(self.consume('<')):
            self.add()
            self.compare_()
        elif (self.consume('>')):
            self.add()
            self.compare_()
        elif (self.consume('<=')):
            self.add()
            self.compare_()
        elif (self.consume('>=')):
            self.add()
            self.compare_()

    # <Add>
    def add(self):
        self.mult()
        self.add_()

    # <Add_>
    def add_(self):
        if(self.consume('+')):
            self.mult()
            self.add_()
        elif (self.consume('-')):
            self.mult()
            self.add_()

    # <Mult>
    def mult(self):
        self.unary()
        self.mult_()

    # <Mult_>
    def mult_(self):
        if(self.consume('*')):
            self.unary()
            self.mult_()
        elif (self.consume('/')):
            self.unary()
            self.mult_()

    # <Unary>
    def unary(self):
        if(self.consume('!')):
            self.unary()
        else:
            self.value()

    # <Value>
    def value(self):
        if (self.consume('-')):
            if (self.check_firsts(Firsts.VALUE)):
                self.value()
            else:
                self.handle_errorf(Firsts.VALUE, Follows.VALUE)
        elif (self.consume(Tokens.NUMBER)):
            pass
        elif(self.consume(Tokens.STRING)):
            pass
        elif(self.consume('true') or self.consume('false')):
            pass
        elif(self.consume('local')):
            if(self.consume('.')):
                self.access()
            else:
                self.handle_errorf('.', Follows.VALUE)
            if(self.consume('.')):
                self.accesses()
        elif(self.consume('global')):
            if(self.consume('.')):
                self.access()
            else:
                self.handle_errorf('.', Follows.VALUE)
            if(self.consume('.')):
                self.accesses()
        elif(self.consume(Tokens.IDENTIFIER)):
            token_id = self.get_previous_token(1)
            self.semantic.check_identifier(token_id)
            if(self.check_firsts(Firsts.ID_VALUE)):
                self.id_value()
        elif(self.consume('(')):
            if(self.check_firsts(Firsts.EXPR)):
                self.expr()
                if(not self.consume(')')):
                    self.handle_errorf(')', Follows.VALUE)
            else:
                self.handle_errorf(Firsts.EXPR, Follows.VALUE)
        else:
            self.handle_errorf(Firsts.EXPR, Follows.VALUE)

    # <Id Value>
    def id_value(self):
        if(self.consume('[')):
            self.arrays()
        elif (self.consume('.')):
            self.accesses()
        elif (self.consume('(')):
            if(self.check_firsts(Firsts.ARGS)):
                self.args()
            if (not self.consume(')')):
                self.handle_errorf(')', Follows.ID_VALUE)

    # <Log Expr>
    def log_expr(self):
        self.log_or()

    # <Log or>
    def log_or(self):
        self.log_and()
        if (self.consume('||')):
            self.log_or_()

    # <Log or_>
    def log_or_(self):
        self.log_and()
        if (self.consume('||')):
            self.log_or_()

    # <Log And>
    def log_and(self):
        self.log_equate()
        if (self.consume('&&')):
            self.log_and_()

    # <Log And_>
    def log_and_(self):
        self.log_equate()
        if (self.consume('&&')):
            self.log_and_()

    # <Log Equate>
    def log_equate(self):
        self.log_compare()
        self.log_equate_()

    # <Log Equate_>
    def log_equate_(self):
        if(self.consume('==')):
            self.log_compare()
            self.log_equate_()
        elif (self.consume('!=')):
            self.log_compare()
            self.log_equate_()

    # <Log Compare>
    def log_compare(self):
        self.log_unary()
        self.log_compare_()

    # <Compare_>
    def log_compare_(self):
        if(self.consume('<')):
            self.log_unary()
            self.log_compare_()
        elif (self.consume('>')):
            self.log_unary()
            self.log_compare_()
        elif (self.consume('<=')):
            self.log_unary()
            self.log_compare_()
        elif (self.consume('>=')):
            self.log_unary()
            self.log_compare_()

    # <Log Unary>
    def log_unary(self):
        if(self.consume('!')):
            self.log_unary()
        else:
            self.log_value()

    # <Log value>
    def log_value(self):
        if (self.consume(Tokens.NUMBER)):
            pass
        elif(self.consume(Tokens.STRING)):
            pass
        elif(self.consume('true') or self.consume('false')):
            pass
        elif(self.consume('local')):
            if(self.consume('.')):
                self.access()
            else:
                self.handle_errorf('.', Follows.LOG_VALUE)
            if(self.consume('.')):
                self.accesses()
        elif(self.consume('global')):
            if(self.consume('.')):
                self.access()
            else:
                self.handle_errorf('.', Follows.LOG_VALUE)
            if(self.consume('.')):
                self.accesses()
        elif(self.consume(Tokens.IDENTIFIER)):
            token_id = self.get_previous_token(1)
            self.semantic.check_identifier(token_id)
            if(self.check_firsts(Firsts.ID_VALUE)):
                self.id_value()
        elif(self.consume('(')):
            if(self.check_firsts(Firsts.LOG_EXPR)):
                self.log_expr()
                if(not self.consume(')')):
                    self.handle_errorf(')', Follows.LOG_VALUE)
            else:
                self.handle_errorf(Firsts.LOG_EXPR, Follows.LOG_VALUE)
        else:
            self.handle_errorf(Firsts.LOG_EXPR, Follows.LOG_VALUE)

    def check_firsts(self, firsts):
        token = self.get_token()
        if (token != None):
            if (token.get_attribute() in firsts.value or token.get_name() in firsts.value):
                return True
            else:
                return False
        else:
            return False

    @ dispatch(str)
    def consume(self, terminal):
        token = self.get_token()
        if (token != None):
            if (token.get_attribute() == terminal):
                self.parser_tokens.append(token)
                self.semantic.get_tokens().append(token)
                self.cursor.forward()
                return True
            else:
                return False
        else:
            return False

    @ dispatch(Tokens)
    def consume(self, token_name):
        token = self.get_token()
        if (token != None):
            if (token.get_name() == token_name.value):
                self.parser_tokens.append(token)
                self.semantic.get_tokens().append(token)
                self.cursor.forward()
                return True
            else:
                return False
        else:
            return False

    @ dispatch(Firsts)
    def consume(self, firsts):
        token = self.get_token()
        if (token != None):
            if (token.get_attribute() in firsts.value or token.get_name() in firsts.value):
                self.parser_tokens.append(token)
                self.semantic.get_tokens().append(token)
                self.cursor.forward()
                return True
            else:
                return False
        else:
            return False

    def handle_errorf(self, expected, follows):
        token = self.get_token()
        if (token != None):
            pos = token.get_pos()
            expected_str = ''
            if (isinstance(expected, str)):
                expected_str = expected
            elif (isinstance(expected, Tokens)):
                expected_str = expected.value
            elif (isinstance(expected, Firsts)):
                expected_str = str(expected.value)

            token_error = Token(Errors.SYNTAX_ERROR.value, 'ESPERAVA: ' +
                                expected_str + ' MAS RECEBEU: ' + token.get_attribute(), pos)
            print('SyntaxError: expected \'' + expected_str + '\', but received \'' +
                  token.get_attribute() + '\' on line ' + str(pos[0] + 1))

            self.parser_tokens.append(token_error)
            while(True):
                if (token != None):
                    if (token.get_attribute() in follows.value or token.get_name() in follows.value):
                        return
                else:
                    return
                self.cursor.forward()
                token = self.get_token()

        else:
            print('SyntaxError: at the end of file expected \'' +
                  expected + '\', but there are no more tokens.')
            return

    def get_token(self):
        pos = self.cursor.get_position()
        if (pos < len(self.tokens)):
            return self.tokens[pos]
        return None

    def get_previous_token(self, n):
        pos = self.cursor.get_position()
        if (pos < len(self.tokens)):
            return self.tokens[pos-n]
        return None

    def get_tokens_parser(self):
        return self.parser_tokens
