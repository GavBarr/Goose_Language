class Evaluator:

    #set a global for conditional blocks
    
    def __init__(self):
        self.environment = {}
        self.conditional_result=False
        #e.g. ('x',("'gavin'",'string')) the data type needs to be defined in the dictionary for type validation OUTDATED but may come back to this!!!

    
    #this is the main function, that will recursively be called
    def evaluate(self,node):
        #try:
            if isinstance(node, list):
                results = []  # Create a list to hold the results
                for n in node:
                    
                    if n == None:
                        return results
                    
                    def_name = 'eval' + n[0]
                    calling_function = getattr(self, def_name, None)
            
                    if calling_function:
                        results.append(calling_function(n))  # Store the result
                    else:
                        print(f'Function {def_name} not found.')
                return results  # Return the list of results after processing all nodes
            else:
                
                if node != None:
                    
                    def_name = 'eval' + node[0]
                    calling_function = getattr(self, def_name, None)
            
                    if calling_function:
                        return calling_function(node)
                    else:
                        print(f'Function {def_name} not found.')
                else:
                    return results
        #except:
            #raise SyntaxError(f'Language Error')
            

        

       
        
    def evalVariable(self,node):
        
        
        var_name =  node[1] #return the name of the variable, for simplicity let's say 'x' is being returned
        #print(f'{var_name}')
        return var_name
        
        

    def evalNumber(self,node):       
        
        return float(node[1]) #returning the value of the LEFT or RIGHT NUMBER node


    def evalString(self,node):       
        not_parsed = str(node[1])
        parsed = not_parsed[1:-1] #removing the outer quotes
        return parsed #returning the value of the LEFT or RIGHT NUMBER node

    def evalOperator(self,node):
        op = node[1]
        #print(f'left: {node[2][1]} right: {node[3][1]}')
        left = self.evaluate(node[2])
        right = self.evaluate(node[3])


        #basically checking to see if the left or right are variables, if they are then we need to evaluate them against the dictionary
        if self.environment.get(left):
            left = self.environment[left]

        if self.environment.get(right):
            right = self.environment[right]

        
        
        if isinstance(left,float) and isinstance(right,float):
            if op == '+':
                return left + right
            elif op == '-':
                return left - right
            elif op == '*':
                return left * right
            elif op == '/':
                return left / right
            
        elif isinstance(left,str) and isinstance(right,str):
            if op == '+':
                #print(f'{left}+{right}')
                return left + right
                
        else:
            raise SyntaxError(f'Mismatched Types')

    def evalAssignOperator(self,node):
        op = node[1] # will be '='      
        left = self.evaluate(node[2])
        right = self.evaluate(node[3])
        #print(f'left: {left} right: {right}')
        #print(f"{left}={right}")
        try:
            if isinstance(right,float):

                self.environment[left]=right#(float(right),'number')
                
                return self.environment[left] #return for testing
            elif isinstance(right, (str, bytes)):               
                self.environment[left]=right#(str(right),'string')
                               
                return self.environment[left] #return for testing
            
        
                
        except:
            try:
                #TODO WILL NEED TO REVISIT
                self.environment[left] = self.environment[right] #try to get the value of the right node within the dictionary, if it is missing then it will fail and the except block will execute
            except:
                raise SyntaxError(f"'{right}' hasn't been initialized")
            

        

    

    #evaluate IF, ELSIF, ELSE, WHILE, FOR etc.
    def evalConditional(self,node):        
        op = node[1] #check for the conditional value, if, else, for etc.

        #print(f"EvalConditional {op}")
       
        if op in('if', 'elf'):
            #print(f'{node[2][0]}')
            left = self.evaluate(node[2]) #this will be the expression to determine if it is true or false            
            if left == True:
                self.conditional_result=True
                #if node[3] != None:
                print(f'Right Node Issue: {node[3]}')
                right = self.evaluate(node[3]) #this is the block of code that will be executed if the statement is true
                
            else:
                #need to check if there is an else clause or not, if None is in the clause it will fail which in turn is why I check to see if the node is None or not
                if node[4] != None:
                    right = self.evaluate(node[4]) #I need to look at the third child node, which will be either None, or the Else/Elf block that needs to be executed
        if op in('el') and self.conditional_result == False:
            right = self.evaluate(node[3]) #this is the block of code that will be executed if the statement is true

        self.conditional_result = False
        

        return
            
    #evalute if the the arguments/condition are true, return true or false
    def evalEqualsOperator(self,node):  
        var = self.evaluate(node[2])     
        try:
            var_value = self.environment[var] #check to see if the variable has been initialized yet or not
        except:
            raise SyntaxError(f"'{var}' is not defined")
        value = self.evaluate(node[3])

        
        if var_value == value:
            return True
        return False

    def evalFunction(self,node):
        
        def_name = node[1] + 'Function'
        calling_function = getattr(self, def_name, None)
        return calling_function(node)
            


            
    #
    def displayFunction(self,node):
        #accounting for any concatentation of strings
        
        if node[3][0]=='Operator':
            #print(f'DisplayOperator {node[3]}')
            arg_node = self.evaluate(node[3])
            #print(f"Arg Node: {arg_node}")
        else:
            arg_node = node[3]

        #print(f"DisplayFunction!{arg_node}")
        
        if arg_node[0] == 'Variable':
                try:
                    
                    var = self.environment[arg_node[1]]
                    print(var) #use the argument child to print out the arguments
                    return
                        
                except:                   
                    raise SyntaxError(f"'{arg_node}' hasn't been initialized")
        else:
            print(arg_node)
            return           
        #print(arg_node[1]) #use the argument child to print out the arguments
        #TODO adding logic to remove any surrounding single or double quotes ' or "