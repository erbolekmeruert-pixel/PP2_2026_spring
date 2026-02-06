#1
print(10>9)
print(10==9)
print(10<9)

#2
a = 200
b = 33
if b > a:
    print("b is greater than a")
else:
    print("b is not greater than a")

#3 True
print(bool("hello"))
print(bool(15))
print(bool(["apple","cherry"]))

#4 False
print(bool(False))
print(bool(None))
print(bool(0))
print(bool(""))
print(bool(()))
print(bool([]))
print(bool({}))

#5
class myclass():
  def __len__(self):
    return 0

myobj = myclass()
print(bool(myobj))

#6
def myFunction():
   return True
print(myFunction())

#7
def myFunction() :
  return True

if myFunction():
  print("YES!")
else:
  print("NO!")

#8
x = 200
print(isinstance(x, int))