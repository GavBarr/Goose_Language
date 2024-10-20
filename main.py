from lexer.lexer import tokenizeCode
from parser.parser import Parser


def evaluate(node):
    #print(node)
    if node[0] == 'NUMBER': #check for the type and then return the value of the NUMBER node
        print('found')
        return float(node[1]) #returning the value of the LEFT or RIGHT NUMBER node
    elif node[0] == 'Operator':
        op = node[1]
        left = evaluate(node[2])
        right = evaluate(node[3])
        if op == '+':
            return left + right
        elif op == '-':
            return left - right
        elif op == '*':
            return left * right
        elif op == '/':
            return left / right


code = '''
        1+1*10
        '''

tokens = tokenizeCode(code)
#efor token in tokens:
   # print(token)

#print(type(tokens))
token_list = iter(tokens) #make the token_list an iterator so then I can use the next function within the Parser object
#print(type(tokens))
p = Parser(token_list)
result = p.parseExpression()
#print(result)
eval = evaluate(result)
print(eval)
