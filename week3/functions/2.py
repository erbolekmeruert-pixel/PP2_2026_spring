#arguments
def my_func(fname):
    print(fname + " refsnes")
my_func("email")
my_func("Mikasa")
my_func("Akerman")

#fname is a parameter
#"email" is a argument

#You can assign default values to parameters. If the function is called without an argument, it uses the default value:

def my_function(fname = "icloude", lname = "abab"):
  print(fname + " " + lname)

my_function("email", "Refsnes")
my_function()

#Mixing Positional and Keyword Arguments
def my_function(animal, name):
  print("I have a", animal)
  print("My", animal + "'s name is", name)

my_function(name = "Buddy", animal = "dog")

#Sending a list as an argument
def func(fruits):
   for fruit in fruits:
      print(fruit)
my_fruits = ["apple", "banana"]
func(my_fruits)

#Sending a dictionary as an argument:

def my_function(person):
  print("Name:", person["name"])
  print("Age:", person["age"])

my_person = {"name": "Emil", "age": 25}
my_function(my_person)