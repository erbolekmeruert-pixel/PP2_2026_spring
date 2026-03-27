import os
import shutil

# 1 Creating nested dirs
a = "a/b/c"
os.makedirs(a, exist_ok=True)
print(f"Created nested folders: {a}")


#filling folder with data
os.chdir("a/b")
with open("ice.txt", "w") as f:
    f.write("This file is inside b")
with open("cream.txt", "w") as f:
    f.write("This file is inside b")
os.chdir("..")
os.chdir("..")


# 2 List of folders and files
print("Folder content a/b:")
for item in os.listdir("a/b"):
    print(item)

# 3 finding files by extension
txt_files = [f for f in os.listdir("a/b") if f.endswith(".txt")]
print("file with .txt extension:", txt_files)

# 4. move files to another folder
dest_folder = "a/d"
os.makedirs(dest_folder, exist_ok=True)

for file_name in txt_files:
    src_path = os.path.join("a/b", file_name)
    dst_path = os.path.join(dest_folder, file_name)
    shutil.move(src_path, dst_path)
    print(f"files was moved {file_name} -> {dest_folder}")

# 5. copy files by .png extension
os.chdir("a/b")
with open("test1.txt", "x") as f:
    pass
with open("test2.txt", "x") as f:
    pass

os.chdir("..")
os.chdir("..")

png_files = [f for f in os.listdir("a/b") if f.endswith(".txt")]
copy_folder = "copied_files"
os.makedirs(copy_folder, exist_ok=True)

for file_name in png_files:
    shutil.copy(os.path.join("a/b", file_name),
                os.path.join(copy_folder, file_name))
    print(f"file was copied: {file_name} -> {copy_folder}")