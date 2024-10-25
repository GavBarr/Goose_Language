class Evaluator:

    def __init__(self):
        self.environment = {}

    
    #this is the main function, that will recursively be called
    def evaluate(self,node):
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

            

        

       
        
    def evalVariable(self,node):
        
        
        var_name =  node[1] #return the name of the variable, for simplicity let's say 'x' is being returned
        return var_name
        
        

    def evalNumber(self,node):       
        
        return float(node[1]) #returning the value of the LEFT or RIGHT NUMBER node


    def evalString(self,node):       
        
        return str(node[1]) #returning the value of the LEFT or RIGHT NUMBER node

    def evalOperator(self,node):
        op = node[1]
        #print(f'left: {node[2][]} right: {node[3][1]}')
        left = self.evaluate(node[2])
        right = self.evaluate(node[3])
        if not isinstance(left,float):
            try:
                left = self.environment[left] #basically checking against the dictiorany if for some reason the left or right node returns as a string, if not found in dictionary then fail for syntax
            except:
                raise SyntaxError(f"'{left}' invalid type")
        if not isinstance(right,float):
            try:
                right = self.environment[right] #basically checking against the dictiorany if for some reason the left or right node returns as a string, if not found in dictionary then fail for syntax
            except:
                raise SyntaxError(f"'{right}' invalid type")
        
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
            if isinstance(right,float):

                self.environment[left]=float(right)
                return self.environment[left] #return for testing
            elif isinstance(right, (str, bytes)):               
                self.environment[left]=str(right)               
                return self.environment[left] #return for testing
                
        except:
            try:
                
                self.environment[left] = self.environment[right] #try to get the value of the right node within the dictionary, if it is missing then it will fail and the except block will execute
            except:
                raise SyntaxError(f"'{right}' hasn't been initialized")

    

    #evaluate IF, ELSIF, ELSE, WHILE, FOR etc.
    def evalConditional(self,node):        
        op = node[1] #check for the conditional value, if, else, for etc.
        print(f'IMPORTANT NODE: {node}')
        if op=='if':
            #print(f'{node[2][0]}')
            left = self.evaluate(node[2]) #this will be the expression to determine if it is true or false            
            if left == True:
                right = self.evaluate(node[3]) #this is the block of code that will be executed if the statement is true
            else:
                right = self.evaluate(node[4]) #I need to look at the third child node, which will be either None, or the Else/Elf block that needs to be executed

            
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
        arg_node = node[3]
        
        if arg_node[0] == 'Variable':
                try:
                    
                    var = self.environment[arg_node[1]]
                    print(var) #use the argument child to print out the arguments
                    return
                        
                except:                   
                    raise SyntaxError(f"'{arg_node}' hasn't been initialized")
                    
        print(arg_node[1]) #use the argument child to print out the arguments
        #TODO adding logic to remove any surrounding single or double quotes ' or "