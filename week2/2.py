x = 5
x+=3
# x = x + 3 = 8
print(x)

x-=3
#x = x - 3

x *= 3
# x = x * 3

a = 4
a &= 3
print(a)
# a = a & 3 = 4 & 3 = 0
 
b = 2
b|=3
print(b)
# b = b|3 = 2|3 = 3

c = 5
c ^= 3
print(c)
# xor c = c ^ 3 = 5 ^ 3 = 6

print( x := 3)

# the walrus operator
numbers = [1, 2, 3, 4, 5]

if (count := len(numbers)) > 3:
    print(f"List has {count} elements")
# output : List has 5 elements

# identity operators
x = ["apple", "banana"]
y = ["apple", "banana"]
z = x

print(x is z)
print(x is y)
print(x == y)
# True False True 

#membership operators
text = "Hello World"

print("H" in text)
print("hello" in text)
print("z" not in text)
# True False True
