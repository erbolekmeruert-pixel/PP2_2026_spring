# basic functions
def my_function():
    print("hello from a function")
my_function()

#Valid function names:
calculate_sum()
_private_function()
myFunction2()

#With functions - reusable code:

def fahrenheit_to_celsius(fahrenheit):
  return (fahrenheit - 32) * 5 / 9

print(fahrenheit_to_celsius(77))
print(fahrenheit_to_celsius(95))
print(fahrenheit_to_celsius(50))

#A function that returns a value:

def get_greeting():
  return "Hello from a function"

message = get_greeting()
print(message)

#Function definitions cannot be empty. If you need to create a function placeholder without any code, use the pass statement:

def my_function():
  pass

#The pass statement is often used when developing, allowing you to define the structure first and implement details later.