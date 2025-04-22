fruitList = ["tomato", "cucumber", "avocado"]

def check(choice):
    for x in fruitList:
        if (x == choice):
            return True
    return False

print('give me fruit name')

if check(str(input())):
    print("isss inn listtt")
else:
    print("nuhhh uhhhh")