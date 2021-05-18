import os
import re
from lexical_analyzer import LexicalAnalyzer
from compiler import Compiler
from constants import Tokens, Errors

""" 
    Aluno: Rafael Azevedo
    Problema 2: De volta ao novo normal.
    EXA869 - MI - PROCESSADORES DE LINGUAGEM DE PROGRAMAÇÃO -
    2020.1 - Curso de Engenharia de Computação -
    - Universidade Estadual de Feira de Santana. 
"""

inputs = os.listdir('./input') # get list of input files from input folder

for _input in inputs: # iterate each input file
    
    with open('./input/' + _input, 'r') as code: # open input file and store content in code var

        c = Compiler(code.readlines())
        tokens_parser = c.get_tokens_parser() # get tokens parser
            
        output_number = re.findall('\d+', _input)[0]

        hasError = False
        with open('./output/output' + output_number + '.txt', 'w') as wp:
            if tokens_parser:
                for token in tokens_parser:
                    if (token.get_name() == Errors.SYNTAX_ERROR.value):
                        hasError = True
                    wp.write(token.to_string() + '\n')
                wp.write("\n")
                if (not hasError):
                    wp.write('Syntax analysis completed successfully')