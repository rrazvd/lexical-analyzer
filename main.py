import os
import re
from lexical_analyzer import LexicalAnalyzer

""" Aluno: Rafael Azevedo
    Problema 1: De volta ao novo normal.
    EXA869 - MI - PROCESSADORES DE LINGUAGEM DE PROGRAMAÇÃO """


"""get list of input files from input folder """
inputs = os.listdir('./input')

""" iterate each input file """
for _input in inputs:

    """ open input file and store content in code var"""
    with open('./input/' + _input, 'r') as code:

        """ creates a LexicalAnalyzer sending code content """
        la = LexicalAnalyzer(code.readlines())

        """ get tokens and errors list """
        tokens, errors = la.get_tokens()
        
        output_number = re.findall('\d+', _input)[0]
        with open('./output/saida' + output_number + '.txt', 'w') as w:
            print ('\n----------------- Output '+str(output_number)+' -----------------')
            if tokens:
                for token in tokens:
                    w.write(token.to_string() + '\n')
                w.write("\n")
            if errors:
                print('Lexical analysis failed! Errors found: ' + str(len(errors)))
                w.write('---------------------------------------------\n')
                w.write('Lexical analysis failed! Errors found: ' + str(len(errors)) + '\n')
                for error in errors: 
                    w.write(error.to_string() + '\n')
                    if(error.get_name() == 'SIB'):
                        print('invalid character \"' + error.get_attribute() + '\": line ' + str(error.get_pos()[0] + 1) +
                                ' column ' + str(error.get_pos()[1]))
                    elif (error.get_name() == 'OpMF'):
                        print('missing character \"' + error.get_attribute() + '\": line ' +
                                str(error.get_pos()[0] + 1) + ' column ' + str(error.get_pos()[1] + 1))
                    elif (error.get_name() == 'CMF'):
                        print('open string: line ' +
                                str(error.get_pos()[0] + 1) + ' column ' + str(error.get_pos()[1]))
                    elif (error.get_name() == 'CoMF'):
                        print('open comment: line ' +
                                str(error.get_pos()[0] + 1) + ' column ' + str(error.get_pos()[1]))
                    elif (error.get_name() == 'NMF'):
                        print('invalid number: line ' +
                                str(error.get_pos()[0] + 1) + ' column ' + str(error.get_pos()[1]))
            else:
                w.write('---------------------------------------------\n')
                w.write('Lexical analysis completed successfully!')
                print('Lexical analysis completed successfully!')

