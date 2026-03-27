"""Delete a File
To delete a file, you must import the OS module, and run its os.remove() function:

ExampleGet your own Python Server
Remove the file "demofile.txt":
"""
import os
os.remove("demofile.txt")

"""Check if File exist:
To avoid getting an error, you might want to check if the file exists before you try to delete it:

Example
Check if file exists, then delete it:
"""

import os
if os.path.exists("demofile.txt"):
  os.remove("demofile.txt")
else:
  print("The file does not exist")


"""Delete Folder
To delete an entire folder, use the os.rmdir() method:

Example
Remove the folder "myfolder":
"""
import os
os.rmdir("myfolder")

import os


f = open("sample.txt", "x")
f.write("Hello")
f.close()
os.remove("sample.txt")


if os.path.exists("sample.txt"):
  os.remove("sample.txt")
else:
  print("The file does not exist") 



os.rmdir("testfolder") 


import shutil
shutil.copy("test.txt", "copy_of_file.txt")   # копирует файл
shutil.copy2("test.txt", "copy_of_file.txt")  # копирует + сохраняет метаданные(время создания и изменения)
