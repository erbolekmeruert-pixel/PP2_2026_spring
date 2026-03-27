import os
import shutil
# 1
file_path = "sample.txt"
with open(file_path, "w") as f:
    f.write("Hello, this is first line\n")
    f.write("This is second line\n")
print(f"file {file_path} was crated and filled with data")

# 2
with open(file_path, "r") as f:
    content = f.read()
print("File content: \n")
print(content)

# 3 adding data
with open(file_path, "a") as f:
    f.write("This is an appended line 3.\n")
    f.write("This is an appended line 4.\n")

with open(file_path, "r") as f:
    content = f.read()
print("File content")
print(content)

# 4 copy
b_path = "backup_sample.txt"
shutil.copy(file_path, b_path)
print(f"Файл скопирован как {b_path}")

# 5 deleting data
for path in [file_path, b_path]:
    if os.path.exists(path):
        os.remove(path)
        print(f"file {path} deleted")
    else:
        print(f"file {path} not found")