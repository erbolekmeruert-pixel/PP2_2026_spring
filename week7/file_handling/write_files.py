"""Write to an Existing File
To write to an existing file, you must add a parameter to the open() function:

"a" - Append - will append to the end of the file

"w" - Write - will overwrite any existing content"""

#EX1 если файл не существует, то создаст новый
with open(r"test.txt", "a") as f:
    f.write("Now the file has more content!\n")

with open(r"test.txt") as f:
    print(f.read())


#EX2 Если не существует, то создается новый и записывается
with open(r"test.txt", "w") as f:
    f.write("the content\n")

with open(r"test.txt") as f:
    print(f.read())

#EX 3 проверка 
try:
    with open(r"newfile.txt", "x") as f:
        f.write("This is a new file")
    print("newfile.txt")
except FileExistsError:
    print("file already exists")