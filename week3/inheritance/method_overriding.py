"""Add the __init__() Function
So far we have created a child class that inherits the properties and methods from its parent.

We want to add the __init__() function to the child class (instead of the pass keyword).

Note: The __init__() function is called automatically every time the class is being used to create a new object."""
class Student(Person):
  def __init__(self, fname, lname):
    #add properties etc.

"""The child's __init__() function overrides 
the inheritance of the parent's __init__() function."""

#To keep the inheritance of the parent's __init__() function, add a call to the parent's __init__() function:

class Student(Person):
  def __init__(self, fname, lname):
    Person.__init__(self, fname, lname)
