t = int(input())
n = list(map(int, input().split()))
s = list(filter(lambda x: x%2==0, n))
print(len(s))