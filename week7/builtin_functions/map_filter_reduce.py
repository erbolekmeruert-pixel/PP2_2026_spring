import functools


numbers = [1, 2, 3, 4, 5, 6]

# 1
squared = list(map(lambda x: x**2, numbers))
print("Squared:", squared)

# 2
evens = list(filter(lambda x: x % 2 == 0, numbers))
print("Even numbers:", evens)

# 3
total = functools.reduce(lambda x, y: x + y, numbers)
print("Sum with reduce:", total)

# 4
product = functools.reduce(lambda x, y: x * y, numbers)
print("Product with reduce:", product)

# 5
print("Sum:", sum(numbers))
print("Min:", min(numbers))
print("Max:", max(numbers))
print("Length:", len(numbers))