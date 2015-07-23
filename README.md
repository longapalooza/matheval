# matheval
Python class to evaluate basic ASCII math syntax.

# Description
This class is intended to be used to evaluate math expressions provided in an
ASCII math format. It is particularly useful when creating an application that
accepts user provided math expressions. The user simply provides a math
expression in a commonly written format (i.e. sin(x) or 2*sqrt(x^3.5)) and the
class evaluates the expression. The advantage of doing this is that it does not
require the user to be familiar with python's math notation (i.e. math.sin(x)
or 2*math.sqrt(math.pow(x,3.5))). The class allows for variable and function
assignment. Methods included in the class are:
  evaluate(expr)
    Evaluates the expr and returns the result. If the expression is a function
    assignment, returns true on success.
  e(expr)
    A synonym for evalaute().
  vars()
    Returns a dictionary of all user-defined variables and their values.
  funcs()
    Returns a list of all user-defined functions.

# Installation
Place matheval.py in your python working directory and import matheval in your
python module. Requires math and re module.

# Examples
All examples can be found in examples.py.

```python
# import matheval module
import matheval
# initialize new mathevel object
m=matheval.matheval()
# basic evaluation
result=m.evaluate('2+2')
print(result) # returns 4
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
```
