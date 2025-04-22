print("what is the first number")
num1 = float(input())
print("what would you like to do (+, -, *, /).")
type = str(input())
print("what is the second number")
num2 = float(input())


def doMath(num1, num2, type):
    if (type == "+"):
        return str(num1 + num2)
    elif (type == "-"):
        return str(num1 - num2)
    elif (type == "*"):
        return str(num1 * num2)
    elif (type == "/"):
        return str(num1 / num2)
    else:
        print("Invalid")

print("The Result is " + doMath(num1, num2, type))