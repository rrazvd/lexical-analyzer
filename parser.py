""" 
This Class implements a syntactic analyzer. 
"""
class Parser():
    def __init__(self, tokens):
        self.tokens = tokens
        self.parser_tokens = []
        self.start_analyze()

    def start_analyze(self):
        for token in self.tokens:
            print(token.to_string())
        print('-----------------------------')

    def get_parser_tokens(self):
        return self.parser_tokens