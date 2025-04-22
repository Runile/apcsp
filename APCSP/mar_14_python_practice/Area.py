import math

def calc(shape, dimension):
    if shape == "rectangle":
        return (dimension[0] * dimension[1])
    else:
        return (math.pi * (dimension ** 2))
    
print("give me your shape")
shape = str(input())
print("give me your first dimension")
d1 = float(input())
d2 = 1

if shape == 'rectangle':
    print("give me your second dimension")
    d2 = float(input())
    print("the area is " + str(calc(shape, [d1, d2])))
elif shape == "circle":
    print("the area is " + str(calc(shape, d1)))
else:
    print("invalid shape")