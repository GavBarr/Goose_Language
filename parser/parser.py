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



class Parser:
    
    def __init__(self, token_list):
        self.token_list = token_list
        self.current_token = next(self.token_list, None)


    #I want to grab the current type of the token being processed and then go to the next token of from the token list
    def consumeToken(self, token_type):
        if self.current_token and self.current_token.type == token_type:
            self.current_token = next(self.token_list, None)

    

    #looking for any + or - operators, to set as the root of the tree
    def parseExpression(self):
        #initialize by looking for the potential left child node, which would could be a Term or Factor, needs to look at 
        #parseTerm() first becuase of the syntax heirarchy
        node = self.parseTerm()
        #while there is a valid token and a valid type of + or - we will evaluate the token and assign a node
        while self.current_token and self.current_token.type in ('MINUS','ADD'):
            
            #set the operator node to the current node, becuse the type matches + or -
            operator = self.current_token

            #we want to then consume the token and move to the next in the list
            self.consumeToken(operator.type)

            #assign the node as a tuple, with the type, value, left child and right child
            node = ('Operator', operator.value, node, self.parseTerm())#node inside of the tuple, is the node from looking at self.parseTerm()
            #                                       left  right
        print(f'Node {node}')
        return node

    #very similar to the parseExpression, but now we are looking at and comparing for the next node as a Factor rather than a Term
    def parseTerm(self):
        #look for the Factor as the node
        node = self.parseFactor()

        #check for a different operator, in this case for any multiplication or division. if nothing is found, then only return the factor valule as a node
        while self.current_token and self.current_token.type in ('MULTIPLY','DIVIDE'):
            operator = self.current_token
            self.consumeToken(operator.type)

            node = ('Operator', operator.value, node, self.parseFactor())

        return node

    
    def parseFactor(self):
        
        if self.current_token and self.current_token.type == "INTEGER_LITERAL":
            token = ("NUMBER", self.current_token.value)#we store the type and the value as a token and then proceed to the next token
            self.consumeToken(self.current_token.type)
            return token
        #else if check for parantheses
        #else:
            #raise SyntaxError(f"Syntax Issue on line {self.current_token.line}")

        