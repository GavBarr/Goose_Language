from lexer.lexer import tokenizeCode
from parser.parser import Parser

class Evaluator:

    def __init__(self):
        self.environment = {}

    
    #this is the main function, that will recursively be called
    def evaluate(self,node):
        def_name = 'eval'+ node[0]
        calling_function = getattr(self, def_name, None)
        return calling_function(node) #recursively find the correct function for the type of node being traversed through
        

        

       
        
    def evalVariable(self,node):
        
        return node[1] #return the name of the variable, for simplicity let's say 'x' is being returned

    def evalNumber(self,node):       
        print('found')
        return float(node[1]) #returning the value of the LEFT or RIGHT NUMBER node

    def evalOperator(self,node):
        op = node[1]
        left = self.evaluate(node[2])
        right = self.evaluate(node[3])
        if op == '+':
            return left + right
        elif op == '-':
            return left - right
        elif op == '*':
            return left * right
        elif op == '/':
            return left / right

    def evalAssignOperator(self,node):
        op = node[1] # will be '='      
        left = self.evaluate(node[2])
        right = self.evaluate(node[3])
        try:

            self.environment[left]=float(right)
                
        except:
            try:
                test = self.environment[right]
            except:
                raise SyntaxError(f"'{right}' hasn't been initialized")

    def evalConditional(self,node):
        pass
        #elif node[0] == 'KEYWORD':
        #op = node[1]
        #left = evaluate(node[2]) #left child node
        #right = evaluate(node[3]) #right child node
        #if op == 'if':
            #if left 
            

        

code = '''

        display();
        
        '''

tokens = tokenizeCode(code)
for token in tokens:
    print(token)

#print(type(tokens))
token_list = iter(tokens) #make the token_list an iterator so then I can use the next function within the Parser object
#print(type(tokens))
p = Parser(token_list)
result = p.parseAssignmentExpression()
print(result)
eval = Evaluator()
eval.evaluate(result)
#print(eval)
