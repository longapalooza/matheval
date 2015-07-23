"""
        METHODS

evaluate(expr)
    Evaluates the expression, expr, and returns the result. If the expression is
    a function assignment, returns true on success.

e(expr)
    A synonym for evaluate().

vars()
    Returns a dictionary of all user-defined variables and values.

funcs()
    Returns a list of all user-defined functions.

"""

# import matheval module
import matheval
# initialize new mathevel object
m=matheval.matheval()
# basic evaluation
result=m.evaluate('2+2') # returns 4
print(result)
# supports: order of operation, parenthese, negation, and built-in functions
result=m.evaluate('-8(5/2)^2*(1-sqrt(4))-8')
print(result) # returns 42
# create your own variables and use built-in constants
result=m.evaluate('a = e^(ln(pi))')
print(result) # returns 3.141592653589793
# create your own functions
result=m.evaluate('f(x,y) = x^2 + y^2 - 2x*y + 1')
# and then use them
result=m.evaluate('3*f(42,a)')
print(result) # returns 4532.92746449864
# get all user-defined variables
result=m.vars()
print(result) # returns {'a': 3.141592653589793}
# get all user-defined functions
result=m.funcs()
print(result) # returns ['f(x,y)']
