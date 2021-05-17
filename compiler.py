from lexical_analyzer import LexicalAnalyzer
from parser import Parser
from symbol_table import SymbolTable
from constants import reserved_words


class Compiler():
    def __init__(self, code):
        self.code = code
        self.symbol_table = SymbolTable(reserved_words)
        self.lexical_analyzer = LexicalAnalyzer(self.code, self.symbol_table)
        tokens, errors = self.lexical_analyzer.get_tokens()
        self.parser = Parser(tokens)

    """
    This method returns symbol table dict.
    """

    def get_symbol_table(self):
        return self.symbol_table

    def get_tokens_lexer(self):
        return self.lexical_analyzer.get_tokens()

    def get_tokens_parser(self):
        return self.parser.get_tokens_parser()