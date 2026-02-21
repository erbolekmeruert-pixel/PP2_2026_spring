"""Using Lambda with sorted()
The sorted() function can use a lambda as a key for custom sorting:
"""

students = [("Emil", 25), ("Tobias", 22), ("Linus", 28)]
sorted_students = sorted(students, key=lambda x: x[1])
print(sorted_students)

#output sort a list of tuples by the second element:
#[('Tobias', 22), ('Emil', 25), ('Linus', 28)]

words = ["apple", "pie", "banana", "cherry"]
sorted_words = sorted(words, key=lambda x: len(x))
print(sorted_words)

#output sort strings by length: 
#['pie', 'apple', 'banana', 'cherry']