from lexer.lexer import tokenizeCode
from parser.parser import Parser
from interpreter.interpreter import Evaluator

code = '''
        
           
            display('test');
           
    
        '''



def process_node(node, depth=0):
    # Base case: If node is not a tuple, simply print it with indentation
    if not isinstance(node, tuple):
        print("  " * depth + str(node))
        return
    
    # Recursive case: Process each element in the tuple
    for element in node:
        process_node(element, depth + 1)
        
tokens = tokenizeCode(code)
for token in tokens:
    print(token)

#print(type(tokens))
token_list = iter(tokens) #make the token_list an iterator so then I can use the next function within the Parser object
#print(type(tokens))
p = Parser(token_list)
result = p.parseStatements()
#print(result)
separated_statement_node = result[1] #I want to get the value of the statements tuple, the tuple contains the statement AST tree essentially
print (separated_statement_node)
eval = Evaluator()
eval.evaluate(separated_statement_node)
#print(eval)
