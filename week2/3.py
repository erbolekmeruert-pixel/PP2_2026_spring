'''
[] List is a collection which is ordered and changeable. Allows duplicate members.
() Tuple is a collection which is ordered and unchangeable. Allows duplicate members.
{} Set is a collection which is unordered, unchangeable*, and unindexed. No duplicate members.
Dictionary is a collection which is ordered** and changeable. No duplicate members.
'''
# Lists (like 1D arrays in C++)

a = [1, 2, 3, 4, 5]

print(a)      # just prints the list as a string

print(len(a)) # amount of elements in the list
print(a[0])   # first element
print(a[-1])  # last element

# slicing is also applicable to lists
print(a[1:]) 
print(a[1:4])
print(a[::-1])