from cursor import Cursor
from constants import Tokens, Firsts, Follows, Errors
from multipledispatch import dispatch
from token2 import Token

"""
This Class implements a syntactic analyzer.
"""


class Parser():

    def __init__(self, tokens):
        self.tokens = tokens
        self.parser_tokens = []
        self.cursor = Cursor()  # create a cursor that will move inside the tokens list
        self.program()  # then the analyze begins

    # <Program>
    def program(self):
        if (self.check_firsts(Firsts.STRUCT_BLOCK)):  # <Structs>
            self.structs()

        if (self.consume('const')):  # <Const Block>
            self.const_block()

        if (self.consume('var')):  # <Var Block>
            self.var_block()

        if (self.consume('procedure')):  # <Start Block>
            self.start_block()
        else:
            self.handle_error('procedure')  # , Follows.START_BLOCK)

        if (self.check_firsts(Firsts.DECLS)):  # <Decls>
            self.decls()

    # <Structs>
    def structs(self):
        self.struct_block()
        if(self.check_firsts(Firsts.STRUCT_BLOCK)):
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
            if(self.check_firsts(Firsts.CONST_DECLS)):
                self.const_decls()

            if (not self.consume('}')):
                self.handle_error('}')
        else:
            self.handle_error('{')

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
                self.const()
                if (self.check_firsts(Firsts.CONST_LIST)):
                    self.const_list()
                else:
                    self.handle_error(Firsts.CONST_LIST)
            else:
                self.handle_error(Tokens.IDENTIFIER)
        elif (self.consume('typedef')):
            self.type_def()
        elif (self.consume(Tokens.IDENTIFIER)):
            if (self.consume(Tokens.IDENTIFIER)):
                self.const()
                if (self.check_firsts(Firsts.CONST_LIST)):
                    self.const_list()
                else:
                    self.handle_error(Firsts.CONST_LIST)
            else:
                self.handle_error(Tokens.IDENTIFIER)

    # <Const>
    def const(self):
        if (self.consume('[')):
            self.arrays()

        if (self.consume('=')):
            if (self.check_firsts(Firsts.DECL_ATRIBUTE)):
                self.decl_atribute()
            else:
                self.handle_error(Firsts.DECL_ATRIBUTE)
        else:
            self.handle_error('=')

    # <Const List>
    def const_list(self):
        if (self.consume(',')):
            if (self.consume(Tokens.IDENTIFIER)):
                self.const()
                if (self.check_firsts(Firsts.CONST_LIST)):
                    self.const_list()
                else:
                    self.handle_error(Firsts.CONST_LIST)
            else:
                self.handle_error(Tokens.IDENTIFIER)
        elif (self.consume(';')):
            pass

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
            if (self.consume(Tokens.IDENTIFIER)):
                self.var()
                if (self.check_firsts(Firsts.VAR_LIST)):
                    self.var_list()
                else:
                    self.handle_error(Firsts.VAR_LIST)
            else:
                self.handle_error(Tokens.IDENTIFIER)

    # <Type>
    def _type(self):
        if (self.consume('struct')):
            if (not self.consume(Tokens.IDENTIFIER)):
                self.handle_error(Tokens.IDENTIFIER)
        else:
            self.consume(Firsts.TYPE)

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
                    self.handle_error(Firsts.VAR_LIST)
            else:
                self.handle_error(Tokens.IDENTIFIER)
        elif (self.consume('=')):
            if (self.check_firsts(Firsts.DECL_ATRIBUTE)):
                self.decl_atribute()
                if (self.check_firsts(Firsts.VAR_LIST)):
                    self.var_list()
                else:
                    self.handle_error(Firsts.VAR_LIST)
            else:
                self.handle_error(Firsts.DECL_ATRIBUTE)
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
                    self.handle_error(';')
            else:
                self.handle_error(Firsts.EXPR)
        elif(self.consume('++')):
            if(not self.consume(';')):
                self.handle_error(';')
        elif(self.consume('--')):
            if(not self.consume(';')):
                self.handle_error(';')

    # <Accesses>
    def accesses(self):
        self.access()
        if (self.consume('.')):
            self.accesses()

    # <Access>
    def access(self):
        if(self.consume(Tokens.IDENTIFIER)):
            if (self.consume('[')):
                self.arrays()
        else:
            self.handle_error(Tokens.IDENTIFIER)

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
            self.handle_error(Firsts.EXPR)

    # <Array>
    def array(self):
        if (self.check_firsts(Firsts.INDEX)):
            self.index()
        if (not self.consume(']')):
            self.handle_error(']')

    # <Index>
    def index(self):
        if (self.consume(Tokens.IDENTIFIER)):
            pass
        elif(self.consume(Tokens.NUMBER)):
            pass

    # <Start Block>
    def start_block(self):
        if(self.consume('start')):
            self.func_block()
        else:
            self.handle_error('start')

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
                self.handle_error('}')
        else:
            self.handle_error(Firsts.ARRAY_DEF)

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
            self.handle_error(Firsts.ARRAY_DEF)

    # <Func decls>
    def func_decl(self):
        if (self.check_firsts(Firsts.PARAM_TYPE)):
            self.param_type()
            if (self.consume(Tokens.IDENTIFIER)):
                if(self.consume('(')):
                    if (self.check_firsts(Firsts.PARAM_TYPE)):
                        self.params()
                    if(self.consume(')')):
                        self.func_block()
                    else:
                        self.handle_error(')')
                else:
                    self.handle_error('(')
            else:
                self.handle_error(Tokens.IDENTIFIER)
        else:
            self.handle_error(Firsts.PARAM_TYPE)

    # <Proc Decl>
    def proc_decl(self):
        if (self.consume(Tokens.IDENTIFIER)):
            if(self.consume('(')):
                if (self.check_firsts(Firsts.PARAM_TYPE)):
                    self.params()
                if(self.consume(')')):
                    self.func_block()
                else:
                    self.handle_error(')')
            else:
                self.handle_error('(')
        else:
            self.handle_error(Tokens.IDENTIFIER)

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
            self.handle_error(Tokens.IDENTIFIER)

    # <Params list>
    def params_list(self):
        if (self.check_firsts(Firsts.PARAM_TYPE)):
            self.param()
            if (self.consume(',')):
                self.params_list()
        else:
            self.handle_error(Firsts.PARAM_TYPE)

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
            self.handle_error(']')

    # <Param Mult Arrays>
    def param_mult_arrays(self):
        if(self.consume(Tokens.NUMBER)):
            if(self.consume(']')):
                if (self.consume('[')):
                    self.param_mult_arrays()
            else:
                self.handle_error(']')
        else:
            self.handle_error(Tokens.NUMBER)

    # <Func Block>
    def func_block(self):
        if (self.consume('{')):
            if (self.consume('var')):
                self.var_block()
            if (self.check_firsts(Firsts.FUNC_STMS)):
                self.func_stms()
            if (not self.consume('}')):
                self.handle_error('}')
        else:
            self.handle_error('{')

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
                    self.handle_error(';')
            else:
                self.handle_error(Firsts.EXPR)

    # <Else Stm>
    def else_stm(self):
        if(self.consume('{')):
            if (self.check_firsts(Firsts.FUNC_STMS)):
                self.func_stms()
            if (not self.consume('}')):
                self.handle_error('}')
        else:
            self.handle_error('{')

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
                                self.handle_error('}')
                        else:
                            self.handle_error('{')
                    else:
                        self.handle_error('then')
                else:
                    self.handle_error(')')
            else:
                self.handle_error(Firsts.LOG_EXPR)

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
                            self.handle_error('}')
                    else:
                        self.handle_error('{')
                else:
                    self.handle_error(')')
            else:
                self.handle_error(Firsts.LOG_EXPR)

    # <Var Stm>
    def var_stm(self):
        if(self.check_firsts(Firsts.STM_SCOPE)):
            self.stm_scope()
        elif(self.consume(Tokens.IDENTIFIER)):
            if(self.check_firsts(Firsts.STM_ID)):
                self.stm_id()
            else:
                self.handle_error(Firsts.STM_ID)
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
                self.handle_error(Firsts.ASSIGN)
        elif(self.consume('.')):
            self.access()
            if (self.consume('.')):
                self.accesses()
            if(self.check_firsts(Firsts.ASSIGN)):
                self.assign()
            else:
                self.handle_error(Firsts.ASSIGN)
        elif(self.consume('(')):
            if(self.check_firsts(Firsts.ARGS)):
                self.args()
            if (self.consume(')')):
                if(not self.consume(';')):
                    self.handle_error(';')
            else:
                self.handle_error(')')

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
                    self.handle_error(Firsts.ASSIGN)
            else:
                self.handle_error('.')
        elif(self.consume('global')):
            if(self.consume('.')):
                self.access()
                if (self.consume('.')):
                    self.accesses()
                if(self.check_firsts(Firsts.ASSIGN)):
                    self.assign()
                else:
                    self.handle_error(Firsts.ASSIGN)
            else:
                self.handle_error('.')

    # <Stm Cmd>
    def stm_cmd(self):
        if(self.consume('print')):
            if(self.consume('(')):
                if(self.check_firsts(Firsts.ARGS)):
                    self.args()
                if(self.consume(')')):
                    if(not self.consume(';')):
                        self.handle_error(';')
                else:
                    self.handle_error(')')
            else:
                self.handle_error('(')
        elif(self.consume('read')):
            if(self.consume('(')):
                if(self.check_firsts(Firsts.ARGS)):
                    self.args()
                if(self.consume(')')):
                    if(not self.consume(';')):
                        self.handle_error(';')
                else:
                    self.handle_error(')')
            else:
                self.handle_error('(')

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
        if self.check_firsts(Firsts.EXPR):
            self._and()
            if (self.consume('||')):
                self._or_()
        else:
            self.handle_error(Firsts.EXPR)

    # <And>
    def _and(self):
        self.equate()
        if (self.consume('&&')):
            self._and_()

    # <And_>
    def _and_(self):
        if self.check_firsts(Firsts.EXPR):
            self.equate()
            if (self.consume('&&')):
                self._and_()
        else:
            self.handle_error(Firsts.EXPR)

    # <Equate>
    def equate(self):
        self.compare()
        if(self.check_firsts(Firsts.EQUATE_)):
            self.equate_()

    # <Equate_>
    def equate_(self):
        if(self.consume('==')):
            if self.check_firsts(Firsts.EXPR):
                self.compare()
                if(self.check_firsts(Firsts.EQUATE_)):
                    self.equate_()
            else:
                self.handle_error(Firsts.EXPR)
        elif (self.consume('!=')):
            if self.check_firsts(Firsts.EXPR):
                self.compare()
                if(self.check_firsts(Firsts.EQUATE_)):
                    self.equate_()
            else:
                self.handle_error(Firsts.EXPR)

    # <Compare>
    def compare(self):
        self.add()
        if(self.check_firsts(Firsts.COMPARE_)):
            self.compare_()

    # <Compare_>
    def compare_(self):
        if(self.consume('<')):
            if self.check_firsts(Firsts.EXPR):
                self.add()
                if(self.check_firsts(Firsts.COMPARE_)):
                    self.compare_()
            else:
                self.handle_error(Firsts.EXPR)
        elif (self.consume('>')):
            if self.check_firsts(Firsts.EXPR):
                self.add()
                if(self.check_firsts(Firsts.COMPARE_)):
                    self.compare_()
            else:
                self.handle_error(Firsts.EXPR)
        elif (self.consume('<=')):
            if self.check_firsts(Firsts.EXPR):
                self.add()
                if(self.check_firsts(Firsts.COMPARE_)):
                    self.compare_()
            else:
                self.handle_error(Firsts.EXPR)
        elif (self.consume('>=')):
            if self.check_firsts(Firsts.EXPR):
                self.add()
                if(self.check_firsts(Firsts.COMPARE_)):
                    self.compare_()
            else:
                self.handle_error(Firsts.EXPR)

    # <Add>
    def add(self):
        self.mult()
        if(self.check_firsts(Firsts.ADD_)):
            self.add_()

    # <Add_>
    def add_(self):
        if(self.consume('+')):
            if self.check_firsts(Firsts.EXPR):
                self.mult()
                if(self.check_firsts(Firsts.ADD_)):
                    self.add_()
            else:
                self.handle_error(Firsts.EXPR)
        elif (self.consume('-')):
            if self.check_firsts(Firsts.EXPR):
                self.mult()
                if(self.check_firsts(Firsts.ADD_)):
                    self.add_()
            else:
                self.handle_error(Firsts.EXPR)

    # <Mult>
    def mult(self):
        self.unary()
        if(self.check_firsts(Firsts.MULT_)):
            self.mult_()

    # <Mult_>
    def mult_(self):
        if(self.consume('*')):
            if self.check_firsts(Firsts.EXPR):
                self.unary()
                if(self.check_firsts(Firsts.MULT_)):
                    self.mult_()
            else:
                self.handle_error(Firsts.EXPR)
        elif (self.consume('/')):
            if self.check_firsts(Firsts.EXPR):
                self.unary()
                if(self.check_firsts(Firsts.MULT_)):
                    self.mult_()
            else:
                self.handle_error(Firsts.EXPR)

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
                self.handle_error(Firsts.VALUE)
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
                self.handle_error('.')
        elif(self.consume('global')):
            if(self.consume('.')):
                self.access()
            else:
                self.handle_error('.')
        elif(self.consume(Tokens.IDENTIFIER)):
            if(self.check_firsts(Firsts.ID_VALUE)):
                self.id_value()
        elif(self.consume('(')):
            if(self.check_firsts(Firsts.EXPR)):
                self.expr()
                if(not self.consume(')')):
                    self.handle_error(')')
            else:
                self.handle_error(Firsts.EXPR)

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
                self.handle_error(')')

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
        if self.check_firsts(Firsts.LOG_EXPR):
            self.log_and()
            if (self.consume('||')):
                self.log_or_()
        else:
            self.handle_error(Firsts.LOG_EXPR)

    # <Log And>
    def log_and(self):
        self.log_equate()
        if (self.consume('&&')):
            self.log_and_()

    # <Log And_>
    def log_and_(self):
        if self.check_firsts(Firsts.LOG_EXPR):
            self.log_equate()
            if (self.consume('&&')):
                self.log_and_()
        else:
            self.handle_error(Firsts.LOG_EXPR)

    # <Log Equate>
    def log_equate(self):
        self.log_compare()
        if(self.check_firsts(Firsts.EQUATE_)):
            self.log_equate_()

    # <Log Equate_>
    def log_equate_(self):
        if(self.consume('==')):
            if self.check_firsts(Firsts.LOG_EXPR):
                self.log_compare()
                if(self.check_firsts(Firsts.EQUATE_)):
                    self.log_equate_()
            else:
                self.handle_error(Firsts.LOG_EXPR)
        elif (self.consume('!=')):
            if self.check_firsts(Firsts.LOG_EXPR):
                self.log_compare()
                if(self.check_firsts(Firsts.EQUATE_)):
                    self.log_equate_()
            else:
                self.handle_error(Firsts.LOG_EXPR)

    # <Log Compare>
    def log_compare(self):
        self.log_unary()
        if(self.check_firsts(Firsts.COMPARE_)):
            self.log_compare_()

    # <Compare_>
    def log_compare_(self):
        if(self.consume('<')):
            if self.check_firsts(Firsts.LOG_EXPR):
                self.log_unary()
                if(self.check_firsts(Firsts.COMPARE_)):
                    self.log_compare_()
            else:
                self.handle_error(Firsts.LOG_EXPR)
        elif (self.consume('>')):
            if self.check_firsts(Firsts.LOG_EXPR):
                self.log_unary()
                if(self.check_firsts(Firsts.COMPARE_)):
                    self.log_compare_()
            else:
                self.handle_error(Firsts.LOG_EXPR)
        elif (self.consume('<=')):
            if self.check_firsts(Firsts.LOG_EXPR):
                self.log_unary()
                if(self.check_firsts(Firsts.COMPARE_)):
                    self.log_compare_()
            else:
                self.handle_error(Firsts.LOG_EXPR)
        elif (self.consume('>=')):
            if self.check_firsts(Firsts.LOG_EXPR):
                self.log_unary()
                if(self.check_firsts(Firsts.COMPARE_)):
                    self.log_compare_()
            else:
                self.handle_error(Firsts.LOG_EXPR)

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
                self.handle_error('.')
        elif(self.consume('global')):
            if(self.consume('.')):
                self.access()
            else:
                self.handle_error('.')
        elif(self.consume(Tokens.IDENTIFIER)):
            if(self.check_firsts(Firsts.ID_VALUE)):
                self.id_value()
        elif(self.consume('(')):
            if(self.check_firsts(Firsts.LOG_EXPR)):
                self.log_expr()
                if(not self.consume(')')):
                    self.handle_error(')')
            else:
                self.handle_error(Firsts.LOG_EXPR)

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
                self.cursor.forward()
                return True
            else:
                return False
        else:
            return False

    @ dispatch(str)
    def handle_error(self, expected):
        token = self.get_token()
        if (token != None):
            pos = token.get_pos()
            token_error = Token(Errors.SYNTAX_ERROR, 'ESPERAVA: ' + expected, pos)
            self.parser_tokens.append(token_error)
            print('SyntaxError: expected \'' + expected + '\', but received \'' +
                  token.get_attribute() + '\' on line ' + str(pos[0] + 1))
            """ while(token not in follow):
                self.cursor.forward()
                token = self.get_token()
                if (token == None):
                    print('End of file')
                    exit() """
        else:
            print('SyntaxError: at the end of file expected \'' +
                  expected + '\', but there are no more tokens.')
            return #exit()

    @ dispatch(Tokens)
    def handle_error(self, expected):
        token = self.get_token()
        if (token != None):
            pos = token.get_pos()
            token_error = Token(Errors.SYNTAX_ERROR, 'ESPERAVA: ' + expected.value, pos)
            self.parser_tokens.append(token_error)
            print('SyntaxError: expected ' + expected.value + ', but received \'' +
                  token.get_attribute() + '\' on line ' + str(pos[0] + 1))
            """ while(token not in follow):
                self.cursor.forward()
                token = self.get_token()
                if (token == None):
                    print('End of file')
                    exit() """
        else:
            print('SyntaxError: at the end of file expected \'' +
                  expected + '\', but there are no more tokens.')
            return #exit()

    @ dispatch(Firsts)
    def handle_error(self, expected):
        token = self.get_token()
        if (token != None):
            pos = token.get_pos()
            token_error = Token(Errors.SYNTAX_ERROR, 'ESPERAVA: ' + str(expected.value), pos)
            self.parser_tokens.append(token_error)
            print('SyntaxError: expected ' + str(expected.value) + ', but received \'' +
                  token.get_attribute() + '\' on line ' + str(pos[0] + 1))
            """ while(token not in follow):
                self.cursor.forward()
                token = self.get_token()
                if (token == None):
                    print('End of file')
                    exit() """
        else:
            print('SyntaxError: at the end of file expected \'' +
                  expected + '\', but there are no more tokens.')
            return #exit()

    def get_token(self):
        pos = self.cursor.get_position()
        if (pos < len(self.tokens)):
            return self.tokens[pos]
        return None

    def get_tokens_parser(self):
        return self.parser_tokens
