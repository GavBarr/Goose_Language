#Lexer Class
#Author: Gavin Barrett
import re


        
TOKENS = [
    ('DATATYPE',   r'\b(num|dec|bool|str)\b'),
    ('FLOAT',      r'\b\d+\.\d+\b'),       # Floating-point number
    ('INTEGER',    r'\b\d+\b'),            # Integer number
    ('BOOLEAN',    r'\b(T|F)\b'),          # Boolean literals
    ('STRING',     r'\".*?\"|\'.*?\''),    # String literals (single or double quotes)
    ('ASSIGN',     r'='),                  # Assignment operator
    ('END',        r';'),                  # Statement terminator
    ('ID',         r'[A-Za-z_]\w*'),       # Identifiers (variables/functions)
    ('OP',         r'[+\-*/%]'),           # Arithmetic operators
    ('NEWLINE',    r'\n'),                 # Line breaks
    ('SKIP',       r'[ \t]+'),             # Skip over spaces and tabs
    ('MISMATCH',   r'.'),                  # Any other character
]

KEYWORDS = {'if', 'elf', 'el', 'while', 'for', 'step', 'break', 'done', 'exit', 'continue'}

class Token:

    def __init__(self, type_, value, line, column):
        self.type = type_
        self.value = value
        self.line = line
        self.column = column
    
    def __repr__(self):
        return f'Token({self.type}, {self.value}, line={self.line}, column={self.column})'
        
        

def tokenizeCode(code):

        line=1
        token_list=[]
        start = 0
        regex_list = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in TOKENS) #compiling all of the regex for each token type etc.

        for match in re.finditer(regex_list, code):
            type = match.lastgroup # grags the type of value etc.
            value = match.group() # grabs the actual value assocated
            column = match.start() - start # this grabs the starting index for the match of whatever we're looking at


            
            if type == 'DATATYPE':
                token_list.append(Token('DATATYPE', value, line, column))
            elif type == 'FLOAT':
                token_list.append(Token('FLOAT_LITERAL', float(value), line, column))
            elif type == 'INTEGER':
                token_list.append(Token('INTEGER_LITERAL', int(value), line, column))
            elif type == 'BOOLEAN':
                token_list.append(Token('BOOLEAN_LITERAL', value == 'True', line, column))
            elif type == 'STRING':
                token_list.append(Token('STRING_LITERAL', value, line, column))
            elif type == 'ID' and value in KEYWORDS:
                token_list.append(Token('KEYWORD', value, line, column))
            elif type == 'ID':
                token_list.append(Token('IDENTIFIER', value, line, column))
            elif type == 'ASSIGN':
                token_list.append(Token('ASSIGN', value, line, column))
            elif type == 'OP':
                token_list.append(Token('OPERATOR', value, line, column))
            elif type == 'END':
                token_list.append(Token('END', value, line, column))
            elif type == 'NEWLINE':
                line += 1
                start = match.end()
            elif type == 'SKIP':
                continue
            elif type == 'MISMATCH':
                raise SyntaxError(f'Unexpected character {value} on line {line}')


        return token_list

       
code = '''
        int x = 10;
         float y = 3.14;
        bool is_valid = True;
        string name = "John";
        '''

tokens = tokenizeCode(code)
for token in tokens:
    print(token)
    
    