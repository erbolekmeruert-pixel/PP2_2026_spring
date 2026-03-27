# enumerate_zip_examples.py


names = ["Alice", "Bob", "Charlie"]
ages = [25, 30, 35]

#1
paired = list(zip(names, ages))
print("Paired names and ages:",paired)

# 2
for index, name in enumerate(names):
    print(f"{index}: {name}")

# 3
value = "123"
print("Type of value:", type(value))
int_v = int(value)
float_v = float(value)
str_v = str(456)
print("Converted to int:", int_v)
print("Converted to float:", float_v)
print("Converted to str:", str_v)

# 4
unsorted_numbers = [5, 2, 9, 1]
sorted_numbers = sorted(unsorted_numbers)
print("Sorted numbers:", sorted_numbers)