#NOTES
# expression is the top of the heirarchy, could be adding/subtracting or any other logical operation
#   expression ::= term (('+' | '-') term)*
# 
# term is a subunit of an expression typically involving multiplication or division, terms get evaluated before + or -
#   term ::= factor (('*' | '/') factor)*
#
# factor is the most basic element in an expression, could be a number, variable or an expression enclosed in parthenses
# typically cannot be broken down any further
#   factor ::= NUMBER | VARIABLE | '(' expression ')'


#My Thoughts:
# I first need to checkExpression -> checkTerm -> checkFactor, because the checking needs to stay in the order of precedence
# Nodes/Creating the Tree. Check for the expression, and then establish the root of the tree.

#Conditional Statements/Expressions
#   if (<condition>){ <trueblock> } elf (<condition>){ <falseblock> } el{ <falseblock> }

#Comments /* for individual lines

class Parser:
    
    def __init__(self, token_list):
        self.token_list = token_list
        self.current_token = next(self.token_list, None)



    def parseStatement(self): #single
    
        # Check for assignment expression
        
        node = self.parseExpression()
        
        if self.current_token and self.current_token.type == 'ASSIGN':
            operator = self.current_token
            self.consumeToken(operator.type)  # Consume the assignment operator
            # Recursively parse the right-hand side expression
            rhs = self.parseExpression()  # Handle the expression on the right side of the assignment
            node = ('AssignOperator', operator.value, node, rhs)

        ##print(f'{self.current_token.type}')
        # After parsing an assignment, we expect a semicolon to terminate the statement
        #if self.current_token and self.current_token.type in ('END','BLOCKEND','LPAREN','RPAREN'): #TODO fix the logic to handle assignments, im thinking it will have to be nested within the above IF condition
        if self.current_token:
            self.consumeToken(self.current_token.type)
        #else:
            #raise SyntaxError("Expected ';' at the end of the statement.")
        
        return node

    def parseStatements(self): #multiple
        statements = []

        try:
            while self.current_token:
                statement = self.parseStatement()
                statements.append(statement)
                
            return ('Statements', statements)
        except:
            raise SyntaxError(f'Error on Line: {self.current_token.line}')

        

    #I want to grab the current type of the token being processed and then go to the next token of from the token list
    def consumeToken(self, token_type):
        if self.current_token and self.current_token.type == token_type:
            self.current_token = next(self.token_list, None)




    def parseFunctionCall(self):
        self.parseLineComments()
        name = self.current_token
        self.consumeToken(self.current_token.type) # we want to then move past the "function name" and determine if there are () afterwards, with or without arguments. this defines a function or a variable

        if self.current_token and self.current_token.type == 'LPAREN':
            self.consumeToken(self.current_token.type)
            #define the arguments for the function
            args = self.parseFunctionArguments()
            
            if self.current_token and self.current_token.type == 'RPAREN':
                    self.consumeToken(self.current_token.type)
                    if self.current_token.type=='END':
                        node = ('Function', name.value, None, args) #it is only necessary to have on child node for a function node, because only the arguments are assocaited to the root node of the function name
                        return node
                    else:
                        raise SyntaxError(f"';' missing")
            else:
                raise SyntaxError(f"'{name.value}' is not a valid function")
        

    def parseFunctionArguments(self):
        self.parseLineComments()
        node = self.parseExpression()

        
        return node

    def parseIfCondition(self):
        self.parseLineComments()
        
        #if tis isn't the start of a conditional block, then bail
        if self.current_token.type != ('KEYWORD'):
            return None
        
        
        
        #look though the token list then for the if/while/for root node
        while self.current_token and self.current_token.type in ('KEYWORD'): #using keyword this will group all fo the keywords, could be problematic becuase of step, continue etc. 
            if self.current_token.value == "if":
                ##print(f'ENTERED IF CONDITINOAL: {self.current_token}')
                operator = self.current_token
                self.consumeToken(operator.type)
                ##print(f'ENTERED IF CONDITINOAL 2: {self.current_token}')
                ##print(f'{self.current_token.type}')
                if self.current_token and self.current_token.type in ('LPAREN'):
                    self.consumeToken(self.current_token.type)
                    left_node = self.parseEqualsExpression()#                                        this far right child node will be the else/elf node
                    #print(f'Left Node {left_node}')
                    middle_node = self.parseIfBlockExpression()     
                    #print(f'Middle Node{middle_node}')
                              
                    node = ('Conditional', operator.value, left_node, middle_node, self.parseElfCondition()) #the left child will be the TRUE/FALSE statement, and then the right child will be corresponding expression IF TRUE
                else:
                    raise SyntaxError(f"Syntax Error '(' Missing")
            
            
            
            
        return node
    
    def parseElfCondition(self):
        self.parseLineComments()
       # #print(f'{self.current_token.type}')
        node = None #set node to None, so if there is no else block, we can return a valid value
        
        print(f'ELF CONDITION: {self.current_token}')
        if self.current_token.type != ('KEYWORD'): # this is to catch the infinite loop that happens if there are more than one elf conditions
            self.consumeToken(self.current_token.type) #consume ;
            ##print(f'{self.current_token.type}')
            self.consumeToken(self.current_token.type) #consume }
            ##print(f'{self.current_token.type}')
        if self.current_token != None:     
            if self.current_token and self.current_token.type != ('KEYWORD'):           
                return None
            if self.current_token.value == 'el':
                return self.parseElseCondition()
        if self.current_token == None:
            return node
        
        
        while self.current_token  and self.current_token.type in ('KEYWORD'):
            if self.current_token.value == 'elf':                
                operator = self.current_token
                self.consumeToken(operator.type)
                if self.current_token and self.current_token.type in ('LPAREN'):
                    self.consumeToken(self.current_token.type)
                    left_node = self.parseEqualsExpression()#                                        this far right child node will be the else/elf node
                    middle_node = self.parseIfBlockExpression()
                    self.consumeToken(self.current_token.type) #we consume two more tokens to address the while infinite loop issue
                    self.consumeToken(self.current_token.type)                   
                    node = ('Conditional', operator.value, left_node, middle_node, self.parseElseCondition()) #the left child will be the TRUE/FALSE statement, and then the right child will be corresponding expression IF TRUE
                else:
                    raise SyntaxError(f"Syntax Error '(' Missing")
            
                

        return node
        
    

    def parseElseCondition(self):

        
        self.parseLineComments()
        #not sure why I was consuming two tokens before entering this function, but I did find some issues when parsing the AST tree. The node that is created isn't correct 12/7/24
        #i figured out why there are two consumptions, becuase of an infinite loop issue in a while loop


        #self.consumeToken(self.current_token.type)       
        #self.consumeToken(self.current_token.type)   
        #print(f"else conditional: {self.current_token.type}")
        
          
       
        if self.current_token and self.current_token.type=='KEYWORD':
            if self.current_token.value == 'elf': #check to see if there is an elf if so go back to the routine                
                return self.parseElfCondition()
            if self.current_token.value=='el':#TODO add logic as well for the elf value
                
                operator = self.current_token.value
                self.consumeToken(self.current_token.type)
                node = ('Conditional', operator ,None, self.parseElseBlockExpression()) #this should handle any logic for conditional blocks, for specifically { expression }
                
                ##print(f'Type: {self.current_token.type}')
                self.consumeToken(self.current_token.type)      
                ##print(f'Type: {self.current_token.type}') 
                #self.consumeToken(self.current_token.type)  
                ##print(f'Type: {self.current_token.type}')
                return node
        return None
    
    #this is exclusive for comparing for conditionals, not assigning
    def parseEqualsExpression(self):
        node = self.parseTerm()
        while self.current_token and self.current_token.type in ('EQUALS'):

            operator = self.current_token
            self.consumeToken(operator.type)
            node = ('EqualsOperator', operator.value, node, self.parseTerm())

        return node

   
    
    def parseAssignmentExpression(self):
        self.parseLineComments()
        node = self.parseTerm()
        

        while self.current_token and self.current_token.type in ('ASSIGN'):

            operator = self.current_token
            self.consumeToken(operator.type)
            node = ('AssignOperator', operator.value, node, self.parseTerm())

        return node
    
    def parseElseBlockExpression(self):
        #I want to identify "{" so then I can consume the token, and start the expression correctly
        self.parseLineComments()
        #print(f'Entered ElseBlockExpression')
        
        
        if self.current_token and self.current_token.type in ('BLOCKSTART'):
                self.consumeToken(self.current_token.type) #consume and move to the next token in the list, so then we can evalutate the expression correctly
        else:
            raise SyntaxError(f"Syntax Issue on line {self.current_token.line}") #simple syntax error
            
        node = self.parseExpression()
        

        return node

    def parseIfBlockExpression(self):
        #I want to identify "{" so then I can consume the token, and start the expression correctly
        self.parseLineComments()
        
        if self.current_token and self.current_token.type in ('RPAREN'):
                self.consumeToken(self.current_token.type) #consume and move to the next token in the list, so then we can evalutate the expression correctly
        else:
            raise SyntaxError(f"Syntax Issue on line {self.current_token.line}") #simple syntax error
        
        
        if self.current_token and self.current_token.type in ('BLOCKSTART'):
                self.consumeToken(self.current_token.type) #consume and move to the next token in the list, so then we can evalutate the expression correctly
        else:
            raise SyntaxError(f"Syntax Issue on line {self.current_token.line}") #simple syntax error
        while self.current_token and self.current_token.type not in ('BLOCKEND'):  
            print(f'ParseIfBlockExpression: {self.current_token}')
            #self.consumeToken(self.current_token.type) #this was causing an issue with the conditional statments and consuming a token to early, specifally in a case for a function etc.
            
            node = self.parseExpression()
            #print(f'NODE: {node}')

        #self.consumeToken(self.current_token.type) #consume this to get rid of the ;
        
        

        return node
    
    def parseElfBlockExpression(self):
        #I want to identify "{" so then I can consume the token, and start the expression correctly
        self.parseLineComments()
           
        if self.current_token and self.current_token.type in ('RPAREN'):
                self.consumeToken(self.current_token.type) #consume and move to the next token in the list, so then we can evalutate the expression correctly
        else:
            raise SyntaxError(f"Syntax Issue on line {self.current_token.line}") #simple syntax error
        
        ##print(f'{self.current_token.type}')
        if self.current_token and self.current_token.type in ('BLOCKSTART'):
                self.consumeToken(self.current_token.type) #consume and move to the next token in the list, so then we can evalutate the expression correctly
        else:
            raise SyntaxError(f"Syntax Issue on line {self.current_token.line}") #simple syntax error
            
        node = self.parseExpression()
        

        return node
    

    def parseLineComments(self):
        current_line_number = self.current_token.line
        if self.current_token and self.current_token.type == 'COMMENT':
            while self.current_token.line == current_line_number:           
                
                self.consumeToken(self.current_token.type) #go through the token list until the next line, then we can start to look for syntax again

        return


    #looking for any + or - operators, to set as the root of the tree
    def parseExpression(self):
        #initialize by looking for the potential left child node, which would could be a Term or Factor, needs to look at 
        #node = self.parseTerm() #first becuase of the syntax heirarchy
        self.parseLineComments()
        print(f'TESTING FOR DISPLAY: {self.current_token.value}')
        if self.current_token.type=='KEYWORD':
            node = self.parseIfCondition()
        elif self.current_token.type=='IDENTIFIER' and self.current_token.value=='display': #this should eventually have a list of all of the language functions, this will be defined at the beginning/ global list
            node = self.parseFunctionCall()
            ##print(f'ParseExpressionFunction: {node}')
            return node
        else:
            ###print(f'parseTerm(){self.current_token.type}')
            node = self.parseTerm()
        
       
        # Check for assignment operator first
        if self.current_token and self.current_token.type == 'ASSIGN':
            operator = self.current_token
            self.consumeToken(operator.type)  # Consume the assignment operator
            # Parse the right-hand side expression
            
            
            # Return an AST node for assignment
            node = ('AssignOperator', operator.value, node, self.parseExpression()) #recursively go back to the parseExpression and now grab the + or - as the right child root


        
        #while there is a valid token and a valid type of + or - we will evaluate the token and assign a node
        while self.current_token and self.current_token.type in ('MINUS','ADD' ):
            
            #set the operator node to the current node, becuse the type matches + or -
            operator = self.current_token

            #we want to then consume the token and move to the next in the list
            self.consumeToken(operator.type)
            ###print(f'{node}')
            #assign the node as a tuple, with the type, value, left child and right child
            node = ('Operator', operator.value, node, self.parseTerm())#node inside of the tuple, is the node from looking at self.parseTerm()
            #                                       left  right
            
       
        return node

    #very similar to the parseExpression, but now we are looking at and comparing for the next node as a Factor rather than a Term
    def parseTerm(self):
        #look for the Factor as the node
        self.parseLineComments()
        node = self.parseFactor()

        #check for a different operator, in this case for any multiplication or division. if nothing is found, then only return the factor valule as a node
        while self.current_token and self.current_token.type in ('MULTIPLY','DIVIDE'):
            operator = self.current_token
            self.consumeToken(operator.type)

            node = ('Operator', operator.value, node, self.parseFactor())

        return node

    
    def parseFactor(self):
        self.parseLineComments()
       # ##print(f'factor {self.current_token.type}')
        if self.current_token and self.current_token.type == "INTEGER_LITERAL":
            token = ("Number", self.current_token.value)#we store the type and the value as a token and then proceed to the next token
            self.consumeToken(self.current_token.type)
            return token
        if self.current_token and self.current_token.type == "IDENTIFIER":
            token = ('Variable', self.current_token.value)
            self.consumeToken(self.current_token.type)
            ##print(f'token')
            return token
        if self.current_token and self.current_token.type == "STRING_LITERAL":
            token = ('String', self.current_token.value)
            self.consumeToken(self.current_token.type)
            ##print(f'token')
            return token
        #else if check for parantheses
        #else:
            #raise SyntaxError(f"Syntax Issue on line {self.current_token.line}")

        