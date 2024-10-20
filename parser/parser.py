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


    #Basically just going to the next token in the list and then processing it
    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = next(self.token_list, None)
            #print(f"Current Token:{self.current_token}")
        else:
            raise SyntaxError(f"Expected {token_type}")


    def parseExpression(self):
        #Looking for an operator of plus or minus of two TERMS
        print(f"Expression Current Token {self.current_token}\n")
        node = self.parseTerm() # this is finding the first term of the expression, to basically initialize the tree etc
        print(f'2nd Expression Current Token {self.current_token}/n')
        while self.current_token and self.current_token.type in ('MINUS','ADD'):# we need to check for self.current_token, to see if there is a valid token or not
            token = self.current_token
            operator_node = token
            self.eat(operator_node.type)
            print(f"Before Expression Node Found Token {self.current_token}")
            node = ('operator', operator_node.value, node, self.parseTerm()) #the last two tuple fields, are the left and right nodes connected to the node
            print(f"After Expression Node Found Token {self.current_token}\n")
            #                                        left  right
            #print(node[1])
        return node

            


    def parseTerm(self):
        print(f"Term Current Token {self.current_token}\n")
        node = self.parseFactor()
        print(f"2nd Term Current Token {self.current_token}")
       # print(self.current_token.type)
        
        while self.current_token and self.current_token.type in ('MULTIPLY','DIVIDE'):
            token = self.current_token
            operator_node = token
            self.eat(operator_node.type)
            node = ('operatory', operator_node.value, node, self.parseFactor())
            #print(f"Term Node {node}")
        return node

    def parseFactor(self):
        print(f"Factor Current Token {self.current_token}\n")
        token = self.current_token
        if self.current_token and self.current_token.type == "INTEGER_LITERAL":
            self.eat("INTEGER_LITERAL")

            return ("INTEGER_LITERAL", token.value) #return the value so then it can be stored into the tree/node correctly
        else:
            return "Syntax Error"

            


class NumberNode:
    def __init__(self):
        self.type_ = type_
        self.value = value
        self.line = line
        self.column = column


class OperatorNode:
    def __init__(self):
        self.type_ = type_
        self.value = value
        self.line = line
        self.column = column

class ExpressionNode:
    def __init__(self):
        self.type_ = type_
        self.value = value
        self.line = line
        self.column = column