# raw string для того, чтобы при указании пути не сработали \t, \n и т.д.
#EX1
f = open(r"test.txt")
print(f.read())
f.close()


#EX2 
with open(r"test.txt") as f:
    print(f.read())
# при использовании with open, close не требуется

#EX3
with open(r"test.txt") as f:
    print(f.read(5))

#EX4
with open(r"test.txt") as f:
    print(f.readline())
    print(f.readline())

#EX5
with open(r"test.txt") as f:
    for x in f:
        print(x) 
