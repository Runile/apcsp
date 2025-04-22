print("What is your X coord?")
x = float(input())
print("What is your Y coord?")
y = float(input())

if (x == 0 and y == 0):
    print("on origin")
elif (x == 0 and y != 0):
    print("on y axis")
elif (x != 0 and y == 0):
    print("on x axis")
elif (x > 0 and y > 0):
    print("quadrant 1")
elif (x < 0 and y > 0):
    print("quadrant 2")
elif (x < 0 and y < 0):
    print("quadrant 3")
elif (x > 0 and y < 0):
    print("quadrant 4")