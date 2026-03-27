"""import re
a = input()
x = re.findall(r"\w+\.\w+@\w+\.\w+", a)
#y = re.findall()
#rgrz = re.search()
#f = re.match()

if x:
    print(x)
else:
    print("No email")"""
import re
a = input()
d = re.sub(r"[ ,\.]", ":", a)
print(d)