import itertools

x = [i for i in range(1,21)]
y = [i for i in range(1,13)]

print(x)
print(y)

print([(a,b) for a,b in itertools.product(x,y)])
