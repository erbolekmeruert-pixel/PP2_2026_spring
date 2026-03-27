n = int(input())
san = list(map(int, input().split()))
square = map(lambda x: x**2, san)
print(sum(square))
