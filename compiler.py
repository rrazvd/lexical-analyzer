from lexical_analyzer import LexicalAnalyzer
from parser import Parser
from symbol_table import SymbolTable
from constants import reserved_words
from semantic import Semantic


class Compiler():
    def __init__(self, code):
        self.code = code
        self.symbol_table = SymbolTable(reserved_words)
        self.lexical_analyzer = LexicalAnalyzer(self.code, self.symbol_table)
        tokens, errors = self.lexical_analyzer.get_tokens()
        self.semantic = Semantic(self.symbol_table)
        self.parser = Parser(tokens, self.semantic, self.symbol_table)

    """
    This method returns symbol table dict.
    """

    def get_symbol_table(self):
        return self.symbol_table

    def get_tokens_lexer(self):
        return self.lexical_analyzer.get_tokens()

    def get_tokens_parser(self):
        return self.parser.get_tokens_parser()

    def get_tokens_semantic(self):
        return self.semantic.get_tokens()
