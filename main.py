from lexer.lexer import tokenizeCode
from parser.parser import Parser


code = '''
        1+1
        '''

tokens = tokenizeCode(code)
#for token in tokens:
   # print(token)

#print(type(tokens))
token_list = iter(tokens) #make the token_list an iterator so then I can use the next function within the Parser object
#print(type(tokens))
p = Parser(token_list)
result = p.parseExpression()
#print(result)
