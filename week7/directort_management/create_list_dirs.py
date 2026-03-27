"""Create a New File
To create a new file in Python, use the open() method, with one of the following parameters:

"x" - Create - will create a file, returns an error if the file exists

"a" - Append - will create a file if the specified file does not exists

"w" - Write - will create a file if the specified file does not exists"""
 
f = open("myfile.txt", "x")

"""In addition you can specify if the file should be handled as binary or text mode

"t" - Text - Default value. Text mode

"b" - Binary - Binary mode (e.g. images)"""

import os

#ex1 создает папку
os.mkdir("test1_fol")

#ex2  создает вложенные папки
os.makedirs("lv1/lv2/lv3")

#or 

os.makedirs("parent/child", exist_ok = True)

#ex3 список папок 

files = os.listdir()
print(files)
#ex 4 открывает папки, ".." выход в папку на уровень выше
os.chdir("parent/child")
os.chdir("..")
#ex5 указывает путь
a = os.getcwd()
print(a)
#ex6 удаление пустой папки, в ином случае ошибка
os.rmdir("child")