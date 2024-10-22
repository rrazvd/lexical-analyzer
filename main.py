import os
import re
from lexical_analyzer import LexicalAnalyzer
from compiler import Compiler
from constants import Tokens, Errors

""" 
    Aluno: Rafael Azevedo
    Problema 4: De volta ao novo normal.
    EXA869 - MI - PROCESSADORES DE LINGUAGEM DE PROGRAMAÇÃO -
    2020.1 - Curso de Engenharia de Computação -
    - Universidade Estadual de Feira de Santana. 
"""

inputs = os.listdir('./input')  # get list of input files from input folder

for _input in inputs:  # iterate each input file

    with open('./input/' + _input, 'r') as code:  # open input file and store content in code var

        output_number = re.findall('\d+', _input)[0]
        print('-----------------------Output ' +
              output_number + '----------------------------')

        c = Compiler(code.readlines())
        st = c.get_symbol_table()
        print(st.to_string())
        """ tokens_parser = c.get_tokens_parser()  # get tokens parser """
        tokens_semantic = c.get_tokens_semantic()
        hasError = False
        with open('./output/output' + output_number + '.txt', 'w') as wp:
            if tokens_semantic:
                for token in tokens_semantic:
                    if (token.get_name() == Errors.SEMANTIC_ERROR.value):
                        hasError = True
                    wp.write(token.to_string() + '\n')
                wp.write("\n")
                if (not hasError):
                    wp.write('Semantic analysis completed successfully')
                    print('Semantic analysis completed successfully')
                print('-----------------------------------------------------------')
