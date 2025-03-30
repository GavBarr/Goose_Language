#Author: Gavin Barrett
from lexer.lexer import tokenizeCode
from parser.parser import Parser
from interpreter.interpreter import Evaluator
import sys


code = '''
            
                /*this is my langauge I am engineering
                	first='gavin';
                    last='barrett';
                    full_name=first+' '+last;
                    x=1;
                    y=21;
                    z=3;

                    if(z==2)
                    {
                        display(full_name);
                    }

                    z=4;

                    
                 




                
            
        
            '''



#def main():

   # if len(sys.argv) < 2:
        #print("Please provide a .mylang file to execute.")
        #sys.exit(1)

    # Load the .mylang file
    #filename = sys.argv[1]
    #print(f'{filename}')
    #with open(filename, 'r') as f:
        #code = f.read()

        
    #tokens = tokenizeCode(code)
    #for token in tokens:
        #print(token)

    #print(type(tokens))
    #token_list = iter(tokens) #make the token_list an iterator so then I can use the next function within the Parser object
    #print(type(tokens))
    #p = Parser(token_list)
    #result = p.parseStatements()
    #print(result)
    #separated_statement_node = result[1] #I want to get the value of the statements tuple, the tuple contains the statement AST tree essentially
    #print (separated_statement_node)
    #eval = Evaluator()
    #eval.evaluate(separated_statement_node)
    #print(eval)


#main()
tokens = tokenizeCode(code)
for token in tokens:
    print(token)

#print(type(tokens))
token_list = iter(tokens) #make the token_list an iterator so then I can use the next function within the Parser object
#print(type(tokens))
p = Parser(token_list)
result = p.parseStatements()
print(result)
separated_statement_node = result[1] #I want to get the value of the statements tuple, the tuple contains the statement AST tree essentially
print (separated_statement_node)
eval = Evaluator()
eval.evaluate(separated_statement_node)
#print(eval)