import os
import re
from lexical_analyzer import LexicalAnalyzer

"""get list of input files from input folder """
inputs = os.listdir('./input')

""" iterate each input file """
for _input in inputs:

    """ open input file and store content in code var"""
    with open('./input/' + _input, 'r') as code:

        """ creates a LexicalAnalyzer sending code content and start analyze """
        la = LexicalAnalyzer(code.readlines())

        """ get tokens & symbol table and write them to the output file """
        tokens = la.get_tokens()
        with open('./output/saida' + re.findall('\d+', _input)[0] + '.txt', 'w') as w:
            """  w.write(la.get_symbol_table().to_string() + '\n') """
            for token in tokens:
                w.write(token.to_string()+'\n')
                if(token.get_name() == 'SIB'):
                    print('invalid character \"' + token.get_attribute() + '\": line ' + str(token.get_pos()[0] + 1) +
                          ' column ' + str(token.get_pos()[1]))
                elif (token.get_name() == 'OpMF'):
                    print('missing character \"' + token.get_attribute() + '\": line ' +
                          str(token.get_pos()[0] + 1) + ' column ' + str(token.get_pos()[1] + 1))
                elif (token.get_name() == 'CMF'):
                    print('open string: line ' +
                          str(token.get_pos()[0] + 1) + ' column ' + str(token.get_pos()[1]))
                elif (token.get_name() == 'CoMF'):
                    print('open comment: line ' +
                          str(token.get_pos()[0] + 1) + ' column ' + str(token.get_pos()[1]))
