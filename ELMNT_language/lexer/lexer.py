#Lexer Class
#Author: Gavin Barrett
import re



class Lexer():


    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value})"
    

    def checkNumber(input):
        length = len(input)    
        pattern = "\d{"+str(length)+"}"
        matching = re.match(pattern,input)
                
        return matching

    def checkOperator(input):
        pattern = "^[\+\*\-=\/]$"
        matching = re.match(pattern,input)

        return matching


    def checkType(input):
        matching = None
        match input:
            case "num":#numeric
                return input
            case "str":#string
                return input
            case "bool":#boolean
                return input
                

        return matching


    def tokenizeString(input):

        pass
    

    test = checkType("num")
    if test == None:
        print("No Match")
    else:
        print(test)