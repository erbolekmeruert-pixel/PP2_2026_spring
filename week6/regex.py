"""Python RegEx exercises"""

#Write a Python program that matches a string that has an 'a' followed by zero or more 'b''s.
import re
a = input()
x = re.match(r"ab*", a)
if x:
    print("Match")
else:
    print("No match")

#Write a Python program that matches a string that has an 'a' followed by two to three 'b'.
y = re.match(r"ab{2,3}", a)
if y:
    print("m")
else:
    print("n")

#Write a Python program to find sequences of lowercase letters joined with a underscore.
z = re.search(r"[a-z]+_[a-z]+", a)

#Write a Python program to find the sequences of one upper case letter followed by lower case letters.
e = re.search(r"[A-Z][a-z]+", a)

#Write a Python program that matches a string that has an 'a' followed by anything, ending in 'b'.
f = re.match(r"a.*b$", a)

#Write a Python program to replace all occurrences of space, comma, or dot with a colon.
g = re.sub(r"[ ,\.]", ":", a)

#Write a python program to convert snake case string to camel case string.
h = a.split('_')
c = h[0] + ''.join(w.capitalize() for w in h[1:])
print(c)

#Write a Python program to split a string at uppercase letters.
j = re.split(r'(?=[A-Z])', a)

#Write a Python program to insert spaces between words starting with capital letters.
k = re.sub(r'(?<!^)(?=[A-Z])', ' ', a)

#Write a Python program to convert a given camel case string to snake case.
l = re.sub(r'(?<!^)(?=[A-Z])', '_', a).lower()
print(l)