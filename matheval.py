# try to import math module
try:
    import math
# raise exception if module does not exist
except:
    print("")
    print("The math module is required.")
    print("")
    print("")
    raise

# try to import re module
try:
    import re
# raise exception if module does not exist
except:
    print("")
    print("The re module is required.")
    print("")
    print("")
    raise

class matheval:

    def __init__(self):
        # variables
        self.v={'e':math.e, 'pi':math.pi}
        # user defined functions
        self.f={}
        # constants
        self.vb=['e', 'pi']
        # built-in functions
        self.fb=['sin', 'sinh', 'arcsin', 'asin', 'arcsinh', 'asinh',
                 'cos', 'cosh', 'arccos', 'acos', 'arccosh', 'acosh',
                 'tan', 'tanh', 'arctan', 'atan', 'arctanh', 'atanh',
                 'sqrt', 'abs', 'ln', 'log']

    def e(self, expr):
        return self.evaluate(expr)

    def evaluate(self, expr):
        expr=expr.strip()
        matches=re.search(r'^\s*([a-zA-Z]\w*)\s*=\s*(.+)$', str(expr))
        matches2=re.search(r'^\s*([a-zA-Z]\w*)\s*\(\s*([a-zA-Z]\w*(?:\s*,\s*'\
                            '[a-zA-Z]\w*)*)\s*\)\s*=\s*(.+)$', str(expr))
        # is it a variable assignment?
        if matches:
            # make sure we're not assigning to a constant
            if matches.group(1) in self.vb:
                print("Cannot redefined constant.")
                return
            # get the result and make sure it's good
            tmp=self.pfx(self.nfx(matches.group(2)))
            if tmp==None:
                return
            # if so, stick it in the variable dictionary
            self.v[matches.group(1)]=tmp
            # and return the resulting value
            return self.v[matches.group(1)]
        # is it a function assignment?
        elif matches2:
            # get the function name
            fnn=matches2.group(1)
            # make sure it isn't built in
            if fnn in self.fb:
                print('Cannot redefine built-in function '+fnn+'().')
                return
            matches3=re.sub(r'\s+', '', matches2.group(2))
            # get the arguments
            args=matches3.split(',')
            # see if it can be converted to postfix
            stack=self.nfx(matches2.group(3))
            if stack==None:
                return
            # freeze the sate of the non-argument variables
            i=0
            while i<len(stack):
                token=stack[i]
                m=re.search(r'^[a-zA-Z]\w*$', str(token))
                if m and (token not in args):
                    if token in self.v:
                        stack[i]=self.v[token]
                    else:
                        print('Undefined variable '+token+' in function '\
                              'definition.')
                        return
                i+=1
            self.f[fnn]={'args':args, 'func':stack}
            return True
        else:
            # straight up evaluation
            return self.pfx(self.nfx(expr))

    def funcs(self):
        output=[]
        for key, value in self.f.items():
            output.append(key+'('+','.join(value['args'])+')')
        return output

    # for internal use
    def is_numeric(self, var):
        try:
            float(var)
            return True
        except ValueError:
            return False

    # Convert infix to postfix notation
    def nfx(self, expr):
        index=0
        stack=self.stack()
        # postfix form of expression, to be passed to pfx()
        output=[]
        expr=expr.strip()
        ops=['+', '-', '*', '/', '^', '_']
        # right-associative operator?
        ops_r={'+':0, '-':0, '*':0, '/':0, '^':1}
        # operator precedence
        ops_p={'+':0, '-':0, '*':1, '/':1, '_':1, '^':2}
        # we use this in syntax-checking the expression
        # and determining when a - is a negation
        expecting_op=False
        matches=re.search(r'[^\w\s+*^\/()\.,-]', str(expr))
        # make sure the characters are all good
        if matches:
            print('Illegal character '+matches.group(1)+'.')
            return
        # infinite loop
        while True:
            # get the first character at the current index
            op=expr[index:index+1]
            # find out if we're currently at the beginning of a
            # number/variable/function/parenthesis/operand
            match=re.search(r'^([a-zA-Z]\w*\(?|\d+(?:\.\d*)?|\.\d+|\()',
                            str(expr[index:]))
            # is it a negation instead of a minus?
            if op=='-' and not expecting_op:
                # put a negation on the stack
                stack.push('_')
                index+=1
            # we have to explicity deny this, because it's legal on the stack
            elif op=='_':
                # but not in the input expression
                print('Illegal character _.')
                return
            # are we putting an operator on the stack?
            elif ((op in ops) or match) and expecting_op:
                # are we expecting an operator but have a
                # number/variable/function/opening parethesis?
                if match:
                    # it's an implicit multiplication
                    op='*'
                    index-=1
                # heart of the algorithm
                o2=stack.last()
                while (stack.count>0) and o2 and (o2 in ops) and\
                      (ops_p[op]<ops_p[o2] if ops_r[op] else\
                      ops_p[op]<=ops_p[o2]):
                    # pop stuff off the stack into the output
                    output.append(stack.pop())
                    o2=stack.last()
                # finally put OUR operator onto the stack
                stack.push(op)
                index+=1
                expecting_op=False
            # ready to close a parenthesis?
            elif op==')' and expecting_op:
                # pop off the stack back to the last (
                o2=stack.pop()
                while not o2=='(':
                    if not o2:
                        print('Unexpected ).')
                        return
                    else:
                        output.append(o2)
                    o2=stack.pop()
                # did we just close a function?
                if stack.last(2):
                    matches=re.search(r'^([a-zA-Z]\w*)\($', str(stack.last(2)))
                else:
                    matches=False
                if matches:
                    # get the function name
                    fnn=matches.group(1)
                    # see how many arguments there were
                    arg_count=stack.pop()
                    # pop the function and push onto the output
                    output.append(stack.pop())
                    # check the argument count
                    if fnn in self.fb:
                        if arg_count>1:
                            print('Too many arguments.')
                            return
                    elif fnn in self.f:
                        if not arg_count==len(self.f[fnn]['args']):
                            print('Wrong number of arguments.')
                            return
                    # did we somehow push a non-function on the stack?
                    # this should never happen
                    else:
                        print('Internal error 1.')
                        return
                index+=1
            # did we just finish a function argument?
            elif op==',' and expecting_op:
                o2=stack.pop()
                while not o2=='(':
                    # oops, never had a (
                    if o2==None:
                        print('Unexpected ,.')
                        return
                    # pop the argument expression stuff and push onto the output
                    else:
                        output.append(o2)
                    o2=stack.pop()
                # make sure there was a function
                if stack.last(2):
                    matches=re.search(r'^([a-zA-Z]\w*)\($', str(stack.last(2)))
                else:
                    matches=False
                if not matches:
                    print('Unexpected ,.')
                    return
                # increment the argument count
                stack.push(stack.pop()+1)
                # put the ( back on, we'll need to pop back to it again
                stack.push('(')
                index+=1
                expecting_op=False
            elif op=='(' and not expecting_op:
                stack.push('(')
                index+=1
                allow_neg=True
            # do we now have a function/variable/number?
            elif match and not expecting_op:
                expecting_op=True
                val=match.group(1)
                # may be funciton, or variable with implicit multiplication
                matches=re.search(r'^([a-zA-Z]\w*)\($', str(val))
                if matches:
                    # it's a function
                    if (matches.group(1) in self.fb) or\
                       (matches.group(1) in self.f):
                        stack.push(val)
                        stack.push(1)
                        stack.push('(')
                        expecting_op=False
                    # it's a variable with implicit multiplication
                    else:
                        val=matches.group(1)
                        output.append(val)
                # it's a plain old variable or number
                else:
                    output.append(val)
                index+=len(val)
            # miscellaneous error checking
            elif op==')':
                print('Unexpected ).')
                return
            elif (op in ops) and not expecting_op:
                print('Unexpected operator '+str(op)+'.')
                return
            else:
                print('An unexpected error occured.')
            if index==len(expr):
                # did we end with an operator?
                if op in ops:
                    print('Operator '+str(op)+' lacks operand.')
                    return
                else:
                    break
                # step the index past whitespace
            while expr[index:index+1]==' ':
                index+=1
        # pop everything off the stack and push onto output
        op=stack.pop()
        while not op==None:
            # if there are (s on the stack, ()s were unbalanced
            if op=='(':
                print('Expecting )')
                return
            output.append(op)
            op=stack.pop()
        return output

    # evaluate postfix notation
    def pfx(self, tokens, var_list=[]):
        if tokens==False:
            return False
        stack=self.stack()
        for token in tokens:
            # if the token is a binary operator, pop two values off the stack,
            # do the operation, and push the result back on
            matches=re.search(r'^([a-zA-Z]\w*)\($', str(token))
            if token in ['+', '-', '*', '/', '^']:
                op2=stack.pop()
                op1=stack.pop()
                if op2==None:
                    print('Internal error 2.')
                    return
                if op1==None:
                    print('Internal error 3.')
                    return
                if token=='+':
                    stack.push(float(op1)+float(op2))
                elif token=='-':
                    stack.push(float(op1)-float(op2))
                elif token=='*':
                    stack.push(float(op1)*float(op2))
                elif token=='/':
                    if op2==0:
                        print('Division by zero.')
                        return
                    stack.push(float(op1)/float(op2))
                elif token=='^':
                    stack.push(float(op1)**float(op2))
                else:
                    print('How did you get here.')
                    return
            # if the token is a unary operator, pop one value off the stack,
            # do the operation, and push it back on
            elif token=='_':
                stack.push(-1*float(stack.pop()))
            # if the token is a function, pop arguments off the stack,
            # hand them to the function, and push the result back on
            # it's a function
            elif matches:
                fnn=matches.group(1)
                # built-in function
                if fnn in self.fb:
                    op1=stack.pop()
                    if op1==None:
                        print('Internal error 4.')
                        return
                    # for the arc trig synonyms
                    fnn=re.sub(r'^arc', 'a', fnn)
                    if fnn=='ln':
                        fnn='log'
                    # perfectly safe variable function cal
                    exec('stack.push(math.'+str(fnn)+'('+str(op1)+'))')
                elif fnn in self.f:
                    # get args
                    args={}
                    i=len(self.f[fnn]['args'])-1
                    while i>=0:
                        args[self.f[fnn]['args'][i]]=stack.pop()
                        if not args[self.f[fnn]['args'][i]]:
                            print('Internal error 5.')
                            return
                        i-=1
                    stack.push(self.pfx(self.f[fnn]['func'],args))
            # if the token is a number or variable, push it on the stack
            else:
                if self.is_numeric(token):
                    stack.push(token)
                elif token in self.v:
                    stack.push(self.v[token])
                elif token in var_list:
                    stack.push(var_list[token])
                else:
                    print('Undefined variable '+token+'.')
                    return
        # when we're out of tokens, the stack should have a single element
        if not stack.count==1:
            print('Internal error 6.')
            return
        return stack.pop()

    def vars(self):
        output=dict(self.v)
        del output['e']
        del output['pi']
        return output

    # for internal use
    class stack:

        def __init__(self):
            self.stack=[]
            self.count=0

        def last(self, n=1):
            if len(self.stack)>=(self.count-n)>=0:
                return self.stack[self.count-n]

        def pop(self):
            if self.count>0:
                self.count-=1
                return self.stack[self.count]
            return

        def push(self, val):
            self.stack.insert(self.count, val)
            self.count+=1
