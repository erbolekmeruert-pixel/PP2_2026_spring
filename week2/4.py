a = 33
b = 200

if b > a:
  print("b is greater than a")

#using a boolean
is_logged_in = True
if is_logged_in:
  print("Welcome back!") 

# elif
score = 75

if score >= 90:
  print("Grade: A")
elif score >= 80:
  print("Grade: B")
elif score >= 70:
  print("Grade: C")
elif score >= 60:
  print("Grade: D")

# else
number = 7

if number % 2 == 0:
  print("The number is even")
else:
  print("The number is odd")


# short hand if
a = 5
b = 2
if a > b: print("a is greater than b")

# short hand if else
a = 10
b = 20
bigger = a if a > b else b
print("Bigger is", bigger)

#Finding the maximum of two numbers:
x = 15
y = 20
max_value = x if x > y else y
print("Maximum value:", max_value)

#test if a is NOT greater than b:
a = 33
b = 200
if not a > b:
  print("a is NOT greater than b")

#Placeholder for future implementation:
age = 16

if age < 18:
  pass # TODO: Add underage logic later
else:
  print("Access granted")
