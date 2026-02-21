"""The __init__() Method

All classes have a built-in method called __init__(), 
which is always executed when the class is being initiated.

The __init__() method is used to assign values to object
 properties, or to perform operations that are necessary 
 when the object is being created."""

class Person:
  def __init__(self, name, age):
    self.name = name
    self.age = age

p1 = Person("Emil", 36)

print(p1.name)
print(p1.age)
#output:
#Emil 
#36

"""The __init__() method is called automatically every 
time the class is being used to create a new object.

Why Use __init__()?
Without the __init__() method, you would need to set 
properties manually for each object:
"""
#without init
class Person:
  pass

p1 = Person()
p1.name = "Tobias"
p1.age = 25

print(p1.name)
print(p1.age)
#output: Tobias/n 25

#using init
class Person:
  def __init__(self, name, age):
    self.name = name
    self.age = age

p1 = Person("Linus", 28)

print(p1.name)
print(p1.age)

