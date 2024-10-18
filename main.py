from lexer.lexer import tokenizeCode


code = '''
        int x = 10;
         float y = 3.14;
        bool is_valid = True;
        string name = "John";
        '''

tokens = tokenizeCode(code)
for token in tokens:
    print(token)
    