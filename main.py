import os
import re
from lexical_analyzer import LexicalAnalyzer

""" get list of input files from input folder """
inputs = os.listdir('./input')

""" iterate each input file """
for _input in inputs:

    """ open input file and store content in code var"""
    with open('./input/' + _input, 'r') as code:

        """ creates a LexicalAnalyzer sending code content and start analyze """
        la = LexicalAnalyzer(code.readlines()).start_analyze()

        """ get tokens & symbol table and write them to the output file """
        tokens = la.get_tokens()
        with open('./output/saida' + re.findall('\d+', _input)[0] + '.txt', 'w') as w:
            w.write(la.get_symbol_table().to_string() + '\n')
            for token in tokens:
                if (token.get_name() == ';'):
                    w.write(token.to_string()+'\n')
                else:
                    w.write(token.to_string() + ' ')
