# Math and random operations
# Math Functions that need import math
import math
m = math.sqrt(64) # returns 8.0
c = math.ceil(1.4) # returns 2
f = math.floor(1.3) # returns 1
x = math.pi #returns 3.141592653589793
print(math.ceil(1.2))
# Functions that dont need it
x = min(5, 10, 25) # returns 5
y = max(5, 10, 25) # returns 25
a = abs(-7.34) # returns 7.34
p = pow(4, 3) # returns 64

#1
import math

degree = float(input("Input degree: "))
radian = degree * math.pi / 180

print("Output radian:", round(radian, 6))

#2
height = float(input("Height: "))
base1 = float(input("Base, first value: "))
base2 = float(input("Base, second value: "))

area = (base1 + base2) * height / 2

print("Expected Output:", area)

#3
import math

n = int(input("Input number of sides: "))
s = float(input("Input the length of a side: "))

area = (n * s ** 2) / (4 * math.tan(math.pi / n))

print("The area of the polygon is:", round(area))

#4
base = float(input("Length of base: "))
height = float(input("Height of parallelogram: "))

area = base * height

print("Expected Output:", float(area))