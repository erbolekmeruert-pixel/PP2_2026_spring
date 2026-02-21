"""Python Classes/Objects
Python is an object oriented programming language.

Almost everything in Python is an object, with its properties and methods.

A Class is like an object constructor, or a "blueprint" for creating objects."""

#Create a class named MyClass, with a property named x:

class MyClass:
  x = 5

#Create an object named p1, and print the value of x:

p1 = MyClass()
print(p1.x)

#Delete the p1 object:

del p1

#You can create multiple objects from the same class:

#Create three objects from the MyClass class:

p1 = MyClass()
p2 = MyClass()
p3 = MyClass()

print(p1.x)
print(p2.x)
print(p3.x)
#Each object is independent and has its own copy of the class properties.

"""The pass Statement
class definitions cannot be empty,
 but if you for some reason have a 
 class definition with no content, 
 put in the pass statement to avoid 
 getting an error."""
class Person:
  pass

