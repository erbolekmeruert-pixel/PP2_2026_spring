"""Why Use Lambda Functions?
The power of lambda is better shown when you use them as an anonymous function inside another function.

Say you have a function definition that takes one argument, and that argument will be multiplied with an unknown number:"""
def myfunc(n):
  return lambda a : a * n

"""Syntax
lambda arguments : expression
"""
x = lambda a : a + 10
print(x(5))
#output add 10 to argument a and return the result:
# 15

x = lambda a, b : a * b
print(x(5, 6))
#30

def myfunc(n):
  return lambda a : a * n

mydoubler = myfunc(2)

print(mydoubler(11))
# 22

"""Use lambda functions when an anonymous function 
is required for a short period of time."""

"""
Lambda with Built-in Functions
Lambda functions are commonly used with built-in functions like map(), filter(), and sorted().
"""