import pdb
class Node:
    def __init__(self, value):
        self.value = value  
        self.next = None
    
    def __str__(self):
        return "Node({})".format(self.value) 

    __repr__ = __str__

class Stack:
    def __init__(self):
        self.top = None
        self.count = 0
    
    def __str__(self):
        temp = self.top
        out = []
        while temp:
            out.append(str(temp.value))
            temp=temp.next
        out = '\n'.join(out)
        return ('Top:{}\nStack:\n{}'.format(self.top,out))

    __repr__=__str__

    def isEmpty(self):
        return self.top == None

    def __len__(self): 
        return self.count

    def push(self,value):
        newNode = Node(value)
        if self.isEmpty(): 
            self.top = newNode
        else:
            newNode.next = self.top 
            self.top = newNode
        self.count += 1
     
    def pop(self):
        if self.isEmpty():
            return None
        else:
            top_node_value = self.top.value
            self.top = self.top.next
        self.count -= 1
        return top_node_value

    def peek(self):
        return self.top.value

class Calculator:

    operators = '+-*/^'
    parentheses = '()'

    def __init__(self):
        self.__expr = None

    @property
    def getExpr(self):
        return self.__expr

    def setExpr(self, new_expr):
        if isinstance(new_expr, str) and len(new_expr.strip())>0:
            self.__expr = new_expr
        else:
            print('setExpr error: Invalid expression')
            return None

    def isNumber(self, txt):
        if not isinstance(txt,str):
            print("Argument error in isNumber")
            return False
        try:
            float_num = float(txt)
            return True
        except:
            return False

    def _getPostfix(self, txt):
        '''
            Required: _getPostfix must create and use a Stack for expression processing. Follow PEMDAS
        '''
        if not isinstance(txt,str) or len(txt.strip())==0:
            print("Argument error in _getPostfix")
            return None

        postfix_expr= []
        postfixStack = Stack()

        expr = self.__exprList(txt)

        for elem in expr:
            if self.isNumber(elem):
                floated_elem = float(elem)
                postfix_expr.append(f'{floated_elem}')
            elif elem == '(':
                postfixStack.push(elem)
            elif elem == ')':
                while not postfixStack.isEmpty() and postfixStack.peek() != '(':
                    if postfixStack.peek() != '(':
                        postfix_expr.append(postfixStack.pop())
                    else:
                        postfixStack.pop()
                postfixStack.pop()
            elif elem in self.operators:
                if postfixStack.isEmpty():
                    postfixStack.push(elem)
                else:
                    while not postfixStack.isEmpty() and not self.__greaterPrecedence(elem, postfixStack.peek()):
                        if postfixStack.peek() != '(':
                            postfix_expr.append(postfixStack.pop())
                        else:
                            postfixStack.pop()
                    postfixStack.push(elem)
        while not postfixStack.isEmpty():
            postfix_expr.append(postfixStack.pop())
        return ' '.join(postfix_expr)

    def __greaterPrecedence(self, curr_operator, top_operator):
        '''
            All operators (and opening parenthesis) have a precedence that determines if another operator
            can be added to the postfixStack.
        '''
        operator_precendence = {'(': 0, '+': 1, '-': 1, '*': 2, '/': 2, '^': 3}

        if operator_precendence.get(curr_operator) > operator_precendence.get(top_operator):
            return True
        return False


    @property
    def calculate(self):
        if not isinstance(self.__expr,str) or len(self.__expr.strip())==0:
            print("Argument error in calculate")
            return None

        if not self.__validExpression(self.__expr):
            print('Invalid Expression')
            return None

        expr = self.__exprList(self._getPostfix(self.__expr))
        calculatorStack = Stack()

        for elem in expr:
            if self.isNumber(elem):
                calculatorStack.push(elem)
            else:
                second_operand = calculatorStack.pop()
                first_operand = calculatorStack.pop()
                if elem == '+':
                    final_operand = float(first_operand) + float(second_operand)
                    calculatorStack.push(final_operand)
                elif elem == '-':
                    final_operand = float(first_operand) - float(second_operand)
                    calculatorStack.push(final_operand)
                elif elem == '*':
                    final_operand = float(first_operand) * float(second_operand)
                    calculatorStack.push(final_operand)
                elif elem == '/':
                    final_operand = float(first_operand) / float(second_operand)
                    calculatorStack.push(final_operand)
                else:
                    final_operand = float(first_operand) ** float(second_operand)
                    calculatorStack.push(final_operand)

        return calculatorStack.peek()

    def __exprList(self, expr):
        '''
            Space out all valid operators and paretheses in a string expression in order to create a list of unique -- floats, operators or paretheses -- elements to iterate through.
        '''
        for elem in self.operators + self.parentheses:
            expr = expr.replace(elem, f' {elem} ')

        return expr.split()


    def __validExpression(self, expr):
        '''
            A valid infix epxression must pass the following methods...
                __validCharacters()
                __validConsecution()
                __balancedParentheses()
        '''
        expr = self.__exprList(expr)

        if not self.__validCharacters(expr):
            return False

        if not self.__validConsecution(expr):
            return False

        if not self.__balancedParentheses(expr):
            return False

        return True

    def __validCharacters(self, expr):
        '''
            A valid infix expression...
                cannot have any character that is not a float, operator, parenthesis, or space
        '''
        valid_characters = self.operators + self.parentheses + ' .'

        for char in expr:
            if char not in valid_characters and not self.isNumber(char):
                return False
        return True

    def __validConsecution(self, expr):
        '''
            Does not account for negation.

            A valid infix expression (without negation)...
                cannot have an operator at the start and end of an expression
                cannot have back-to-back operators
                cannot have two unique numbers back-to-back without an operator between them
                cannot have a float and an opening '(' parenthesis back-to-back (as if for multiplication)
        '''
        if expr[0] in self.operators or expr[-1] in self.operators:
            return False
        for idx, elem in enumerate(expr):
            if elem in self.operators and idx != (len(expr) - 1):
                if expr[idx + 1] in self.operators:
                    return False
                elif elem == '*':
                    if not self.isNumber(expr[idx + 1]) and expr[idx + 1] not in '()':
                        return False
            elif self.isNumber(elem) and idx != (len(expr) - 1):
                if self.isNumber(expr[idx + 1]) or expr[idx + 1] == '(':
                    return False
        return True

    def __balancedParentheses(self, expr):
        '''
            A valid infix expression...
                cannot start with an closing ')' parenthesis
                cannot end with an opening '(' parenthesis
                must have an equal amount of parentheses: each opening '(' parenthesis has a matching closing ')' parenthesis
        '''
        parenthesesStack = Stack()
        for elem in expr:
            if elem == '(':
                parenthesesStack.push(elem)
            elif elem == ')':
                if parenthesesStack.isEmpty():
                    return False
                parenthesesStack.pop()

        if parenthesesStack.isEmpty():
            return True
        return False
