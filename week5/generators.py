# Iterator and generator exercises
"""A generator function 
is a special type of function that returns an iterator object. 
Instead of using return to send back a single value, generator functions 
use yield to produce a series of results over time. The function pauses 
its execution after yield, maintaining its state between iterations.



"""


#yield saves the point , use less memory
#yield works slow than list
def nums():
    start = 1
    while(start < 10):
        yield start
        start +=1

for num in nums():
    print(num)

"""Why Do We Need Generators?
Memory Efficient : Handle large or infinite data without loading everything into memory.
No List Overhead : Yield items one by one, avoiding full list creation.
Lazy Evaluation : Compute values only when needed, improving performance.
Support Infinite Sequences : Ideal for generating unbounded data like Fibonacci series.
Pipeline Processing : Chain generators to process data in stages efficiently."""


#Creating Generators
def generator_function_name(parameterss):
    # your code here
    yield expression
    # additional code can follow

def fun():
    yield 1            
    yield 2            
    yield 3            
 
# Driver code to check above generator function
for val in fun(): 
    print(val)

"""Generator Expression
Generator expressions are a concise way to create generators. They are similar to list comprehensions but use parentheses instead of square brackets and are more memory efficient.

Syntax:

(expression for item in iterable)"""   
sq = (x*x for x in range(1, 6))
for i in sq:
    print(i)

#1
def square_generator(n):
    for i in range(n + 1):
        yield i ** 2

#2
def even_numbers(n):
    for i in range(n + 1):
        if i % 2 == 0:
            yield i


n = int(input("Enter number: "))

print(",".join(str(num) for num in even_numbers(n)))

#3
def divisible_by_3_and_4(n):
    for i in range(n + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i


for num in divisible_by_3_and_4(100):
    print(num)

#4
def squares(a, b):
    for i in range(a, b + 1):
        yield i ** 2

for value in squares(3, 7):
    print(value)

#5
def countdown(n):
    while n >= 0:
        yield n
        n -= 1


for number in countdown(5):
    print(number)    