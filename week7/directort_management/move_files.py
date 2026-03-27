import shutil 
import os


os.mkdir("folder")
with open ("file.txt","x") as f:
    pass 

# 1. Переместить один файл
shutil.move("file.txt", "folder/file.txt")

# 2. Переименовать файл
with open ("old_name.txt","x") as f:
    pass 
shutil.move("old_name.txt", "new_name.txt")

# 3. Переместить все файлы из одной папки в другую
source = "source_folder"
destination = "dest_folder"

os.mkdir("source_folder")
os.mkdir("dest_folder")
with open(os.path.join(source, "file1.txt"), "w") as f:
    f.write("Текст файла 1")
with open(os.path.join(source, "file2.json"), "w") as f:
    f.write("Текст файла 2")
with open(os.path.join(source, "file3.txt"), "w") as f:
    f.write("Текст файла 3")

for file in os.listdir(source):
        full_path = os.path.join(source, file)
        
        if os.path.isfile(full_path):
            shutil.move(full_path, destination)

# 4. Переместить только .txt файлы
with open(os.path.join(source, "a.txt"), "w") as f:
    f.write("Текст 1")
with open(os.path.join(source, "b.doc"), "w") as f:
    f.write("Текст 2")
with open(os.path.join(source, "c.txt"), "w") as f:
    f.write("Текст 3")

for file in os.listdir(source):
    if file.endswith(".txt"):
        shutil.move(os.path.join(source, file), destination)
        